from transformers import AutoProcessor, MusicgenForConditionalGeneration
import scipy


class BackgroundScoreGenerator:
    DEFAULT_MODEL_ID = "facebook/musicgen-small"
    def __init__(self, model_id=DEFAULT_MODEL_ID) -> None:
        self.processor = AutoProcessor.from_pretrained(model_id)
        self.model = MusicgenForConditionalGeneration.from_pretrained(model_id)

    def generate(self, prompt: str) -> str:
        '''
        Generates a background score based on the prompt.
        @param prompt: The prompt to generate the background score from.
        @return: The generated background score.
        '''
        inputs = self.processor(
            text=[prompt],
            padding=True,
            return_tensors="pt",
        )

        audio_values = self.model.generate(**inputs, max_new_tokens=256)
        return audio_values
        
    def save(self, audio_values, filename):
        '''
        Saves the audio values to a file.
        @param audio_values: The audio values to save.
        @param filename: The filename to save the audio values to.
        '''
        sampling_rate = self.model.config.audio_encoder.sampling_rate
        scipy.io.wavfile.write(filename, rate=sampling_rate, data=audio_values[0, 0].numpy())

    def generate_and_save_to_file(self, prompt: str, filename: str):
        '''
        Generates a background score based on the prompt and saves it to a file.
        @param prompt: The prompt to generate the background score from.
        @param filename: The filename to save the audio values to.
        '''
        audio_values = self.generate(prompt)
        self.save(audio_values, filename)

if __name__ == '__main__':
    bsg = BackgroundScoreGenerator()
    audio_values = bsg.generate('happy piano for moral story')
    bsg.save(audio_values, 'test.wav')
