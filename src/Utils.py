from typing import List
import numpy as np
import scipy
from pydub import AudioSegment


class Utils:
    @staticmethod
    def merge_wav_audios(audio_paths: List[str]):
        '''
        Merge wav audios with pauses
        @param audios: list of audio arrays with pauses
        @return: merged audio array
        '''
        # read paths in audio segments
        audio_segments = [AudioSegment.from_wav(audio_path) for audio_path in audio_paths]
        # merge audio segments with 1s silence
        audio = audio_segments[0]
        for i in range(1, len(audio_segments)):
            audio = audio.append(audio_segments[i], crossfade=1000)
        return audio
    
    def overlay_speech_with_audios(story_audio_paths, bg_audio_paths):
        '''
        Overlay speech with audio
        @param audios: list of audios to overlay with speech
        @param speech: speech array
        @return: overlayed audio array
        '''
        paths = []
        idx = 0
        for audio_path, story_path in zip(bg_audio_paths, story_audio_paths):
            audio = AudioSegment.from_file(audio_path)
            audio = audio.apply_gain(-10)

            story = AudioSegment.from_file(story_path)

            overlaid_audio = story.overlay(audio, loop=False)
            overlaid_audio.export(f"overlaid_{idx}.wav", format='wav')
            paths.append(f"overlaid_{idx}.wav")
            idx += 1
        
        return paths
    
    def save_wav_file(audio, filename, sampling_rate):
        '''
        Saves the audio values to a file.
        @param audio_values: The audio values to save.
        @param filename: The filename to save the audio values to.
        '''
        scipy.io.wavfile.write(filename, sampling_rate, audio)
        print (f"Saved to file {filename}")


if __name__ == "__main__":
    bg_audio_paths = ["0.wav", "1.wav", "2.wav"]
    story_audio_paths = ["tts_0.wav", "tts_1.wav", "tts_2.wav"]

    Utils.overlay_speech_with_audios(story_audio_paths, bg_audio_paths)