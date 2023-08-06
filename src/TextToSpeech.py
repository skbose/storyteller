from TTS.api import TTS
import numpy as np
from typing import List
import scipy
from Utils import Utils


class TextToSpeech:
    def __init__(self) -> None:
        '''
        Initialize the TTS model
        '''
        self.api = TTS(model_name="tts_models/eng/fairseq/vits", gpu=True)

    def generate_audio(self, text: str) -> np.ndarray:
        '''
        Generate audio for text
        @param text: text to generate audio for
        @return: numpy array of audio
        '''
        lines = text.split(".")
        audios = []
        for line in lines:
            line = line.strip()
            if line == "":
                continue
            print ("processing line: ", line)
            audio = self.api.tts(text=line)
            audios.append(audio)
        return audios

    def combined_audio_to_file(self, text: str, output_path: str):
        '''
        Generate audio for text and save to file
        @param text: text to generate audio for
        @param output_path: path to save audio file
        '''
        audios = self.generate_audio(text)
        # merge audios with pauses
        PAUSE = 1.5
        audios = [(audio, PAUSE) for audio in audios]
        combined_audio = Utils.merge_wav_audios(audios)
        # save audio to file using scipy
        scipy.io.wavfile.write(output_path, self.api.synthesizer.output_sample_rate, combined_audio)
        
        print (f"Saved to {output_path}")

    def part_audios_to_files(self, text: str):
        '''
        Generate audio for text and save to file
        @param text: text to generate audio for
        @param output_path: path to save audio file
        '''
        audios = self.generate_audio(text)
        paths = []
        for i, audio in enumerate(audios):
            scipy.io.wavfile.write(f"tts_{i}.wav", rate=self.api.synthesizer.output_sample_rate, data=np.array(audio))
            print (f"Saved to tts_{i}.wav")
            paths.append(f"tts_{i}.wav")
        return paths



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
    # tts.combined_audio_to_file(paragraph, "sample_tts.wav")
    tts.part_audios_to_files(paragraph)