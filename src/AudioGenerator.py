import torchaudio
from audiocraft.models import AudioGen
from audiocraft.data.audio import audio_write
from Utils import Utils
from typing import List
import numpy as np
import scipy


class AudioGenerator:
    '''
    Generates audio from text.
    '''
    def __init__(self) -> None:
        '''
        Initializes the audio generator.
        '''
        self.model = AudioGen.get_pretrained('facebook/audiogen-medium')
        self.model.set_generation_params(duration=5)

    def generate_audios(self, prompts: List[str]) -> List[np.array]:
        '''
        Generates audio from the prompts.
        @param prompts: The prompts to generate the audio from.
        @return: The generated audio.
        '''
        wavs = self.model.generate(prompts)  # generates 3 samples.
        return wavs
    
    def generate_audio(self, paragraph: str) -> np.array:
        '''
        Generates audio from the paragraph.
        @param paragraph: The paragraph to generate the audio from.
        @return: The generated audio.
        '''
        # split into sentences
        sentences = paragraph.split('.')
        sentences = [sentence.strip() for sentence in sentences if sentence.strip() != '']
        audios = self.generate_audios(sentences)
        return audios

    def part_audios_to_files(self, paragraph: str) -> None:
        '''
        Generates audio from the prompts and saves it to a file.
        @param prompts: The prompts to generate the audio from.
        @param filenames: The filenames to save the audio to.
        '''
        wavs = self.generate_audio(paragraph=paragraph)
        paths = []
        for idx, one_wav in enumerate(wavs):
            # Will save under {idx}.wav, with loudness normalization at -14 db LUFS.
            audio_write(f'{idx}', one_wav.cpu(), self.model.sample_rate, strategy="loudness", loudness_compressor=True)
            print(f"Saved to {idx}.wav")
            paths.append(f"{idx}.wav")
        return paths


if __name__ == '__main__':
    story = '''Of course, I'd be happy to tell you a story! Here's a moral story about a cow and a goat:
         Once upon a time, there was a cow named Bessie and a goat named Billy. They lived on a small farm together, and they were the best of friends.
         Every day, Bessie would happily spend her time grazing in the green pastures, while Billy would bound around, playing and jumping with joy. They would spend their evenings together, resting under the shade of a big tree.
         One day, a terrible storm hit the farm, and the rain poured down, causing the river to overflow. The water began to rise, and it looked like the farm was going to be flooded.
         Billy, being the brave goat that he was, didn't hesitate for a moment. He stood tall and strong, and with a fierce determination in his eyes, he brayed loudly, "We must help the farm!"
         Bessie, who had always been a bit more cautious, looked at Billy with surprise and admiration. She knew that Billy was right, but she was scared of the danger.
         Billy didn't give up on Bessie. He kept braying and urging her to come and help. And slowly but surely, Bessie began to see that Billy was right. Together, they worked tirelessly to save the farm, using their unique skills and strengths to move rocks and debris, and lift heavy objects out of the way.
         As the sun began to set, the storm finally began to subside, and the water started to recede. The farm was safe, and the animals were exhausted but proud of their hard work.
         The moral of the story, my dear child, is that when we work together, we can achieve great things. Billy and Bessie's friendship and teamwork saved the farm, and they proved that even the smallest and bravest creatures can make a big difference.
         Do you have any questions, my dear?
    '''
    audio_generator = AudioGenerator()
    audio_generator.generate_and_save_to_file(paragraph=story)
