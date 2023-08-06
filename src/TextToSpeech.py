from TTS.api import TTS


class TextToSpeech:
    def __init__(self) -> None:
        '''
        Initialize the TTS model
        '''
        self.api = TTS(model_name="tts_models/eng/fairseq/vits", gpu=True)

    def generate_audio_and_save_to_file(self, text: str, output_path: str):
        '''
        Generate audio for text and save to file
        @param text: text to generate audio for
        @param output_path: path to save audio file
        '''
        self.api.tts_to_file(text, file_path=output_path)
        print (f"Saved to {output_path}")


if __name__ == "__main__":
    paragraph = '''
    The sun was shining brightly on the green meadow where the race was to take place. The rabbit, with its fluffy tail and fast little legs, was feeling particularly confident. "I will surely win this race," it said to itself. "No one can beat me!" 
    Just then, a slow and steady tortoise came hopping along the path. "I will win this race," it said to itself. "I am much slower than you, but I will not stop until I reach the finish line."
    The race began, and the rabbit took off like a shot. It zipped and zapped along the meadow, its little legs moving as fast as they could. But the tortoise didn't give up. It plodded along slowly but surely, never stopping or resting.
    The rabbit was getting tired, but it didn't want to give up. It pushed itself harder and harder, but no matter how fast it ran, the tortoise was always right behind it.
    In the end, the tortoise crossed the finish line first! The rabbit was amazed and a bit sad. "I should have taken it easier," it said to itself.
    From that day on, the rabbit learned a valuable lesson: you should never underestimate someone just because they are slow and steady. Because sometimes, slow and steady can win the race!
    '''
    tts = TextToSpeech()
    tts.generate_audio_and_save_to_file(paragraph)