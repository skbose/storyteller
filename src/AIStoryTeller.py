from TextToSpeech import TextToSpeech
from BackgroundScoreGenerator import BackgroundScoreGenerator
from TextStoryGenerator import TextStoryGenerator
import logging
from pydub import AudioSegment
import os


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class AIStoryTeller():
    def __init__(self, wavs_dir) -> None:
        self.tts = TextToSpeech()
        self.bsg = BackgroundScoreGenerator()
        self.tsg = TextStoryGenerator(model_name="gpt-3.5-turbo", key=None)
        self.wavs_dir = wavs_dir
        

    def tell_a_story(self, description: str, music_description: str):
        story = self.tsg.generate(description)
        logger.info(story)

        story_audio_path = os.path.join(self.wavs_dir, "story.wav")
        story_audio = self.tts.generate_audio_and_save_to_file(
            text=story, output_path=story_audio_path)

        bg_music_path = os.path.join(self.wavs_dir, "music.wav")
        music_audio = self.bsg.generate_and_save_to_file(music_description, bg_music_path)

        story_audio = AudioSegment.from_file(story_audio_path)
        music_audio = AudioSegment.from_file(bg_music_path)

        music_audio = music_audio.apply_gain(-15)
        overlayed_sound = story_audio.overlay(music_audio, loop=True)

        # save the result
        final_story_audio = os.path.join(self.wavs_dir, "final_story.wav")
        overlayed_sound.export(final_story_audio, format='wav')
        logger.info("Done!")


if __name__ == '__main__':
    ai_story_teller = AIStoryTeller()
    ai_story_teller.tell_a_story("Write a story about a lion and mouse in less than 100 words.", "happy piano for moral story")
