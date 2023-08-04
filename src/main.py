from TextStoryGenerator import TextStoryGenerator
from tts import TTS
from BackgroundScoreGenerator import BackgroundScoreGenerator
import argparse

argparser = argparse.ArgumentParser(description='Generate a story from a prompt.')
argparser.add_argument('--prompt', type=str, help='The prompt to generate the story from.')
argparser.add_argument('--music', type=str, help='Description of the music to generate.')

args = argparser.parse_args()

tsg = TextStoryGenerator()
story = tsg.generate(args.prompt)
print (story)

tts = TTS()
audio_sample = tts.generate_speech_for_paragraph(paragraph=story)
tts.save(audio_sample, "story.wav")

bsg = BackgroundScoreGenerator()
audio_values = bsg.generate(args.music)
bsg.save(audio_values, 'music.wav')

# overlay wav files
from pydub import AudioSegment

story_audio = AudioSegment.from_file("story.wav")
music_audio = AudioSegment.from_file("music.wav")

music_audio = music_audio.apply_gain(-15)
overlayed_sound = story_audio.overlay(music_audio, loop=True)

# save the result
overlayed_sound.export("result.wav", format='wav')

