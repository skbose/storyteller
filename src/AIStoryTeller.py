from TextToSpeech import TextToSpeech
from BackgroundScoreGenerator import BackgroundScoreGenerator
from TextStoryGenerator import TextStoryGenerator
import logging
from pydub import AudioSegment


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class AIStoryTeller():
    def __init__(self) -> None:
        self.tts = TextToSpeech()
        self.bsg = BackgroundScoreGenerator()
        self.tsg = TextStoryGenerator()

    def tell_a_story(self, description: str, music_description: str):
        story = self.tsg.generate(description)
        logger.info(story)

        story_audio = self.tts.generate_audio_and_save_to_file(
            text=story, output_path='../wavs/story.wav')

        music_audio = self.bsg.generate_and_save_to_file(music_description, '../wavs/music.wav')

        story_audio = AudioSegment.from_file("../wavs/story.wav")
        music_audio = AudioSegment.from_file("../wavs/music.wav")

        music_audio = music_audio.apply_gain(-15)
        overlayed_sound = story_audio.overlay(music_audio, loop=True)

        # save the result
        overlayed_sound.export("../wavs/final_story.wav", format='wav')
        logger.info("Done!")


if __name__ == '__main__':
    ai_story_teller = AIStoryTeller()
    ai_story_teller.tell_a_story("moral story of the monkey and the goat", "happy piano for moral story")
