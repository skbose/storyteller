from TextToSpeech import TextToSpeech
from BackgroundScoreGenerator import BackgroundScoreGenerator
from TextStoryGenerator import TextStoryGenerator
import logging
from pydub import AudioSegment
from Utils import Utils
from AudioGenerator import AudioGenerator


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class AIStoryTeller():
    def __init__(self) -> None:
        self.tts = TextToSpeech()
        self.bsg = BackgroundScoreGenerator()
        self.tsg = TextStoryGenerator()
        self.ag = AudioGenerator()

    def tell_a_story(self, description: str, music_description: str):
        story = self.tsg.generate(description)
        logger.info(story)

        story_audio_paths = self.tts.part_audios_to_files(text=story)
        bg_audio_paths = self.ag.part_audios_to_files(paragraph=story)

        bg_and_speech_audio_paths = Utils.overlay_speech_with_audios(
            bg_audio_paths=bg_audio_paths, story_audio_paths=story_audio_paths)
        
        # add pauses audios
        merged_story_audio = Utils.merge_wav_audios(bg_and_speech_audio_paths)
        merged_story_audio.export('../wavs/story.wav', format='wav')
        
        music_audio = self.bsg.generate_and_save_to_file(music_description, '../wavs/music.wav')

        story_audio = merged_story_audio
        music_audio = AudioSegment.from_file("../wavs/music.wav")

        music_audio = music_audio.apply_gain(-15)
        overlayed_sound = story_audio.overlay(music_audio, loop=True)

        # save the result
        overlayed_sound.export("../wavs/final_story.wav", format='wav')
        logger.info("Done!")


if __name__ == '__main__':
    ai_story_teller = AIStoryTeller()
    ai_story_teller.tell_a_story("moral story of the monkey and the goat", "happy piano for moral story")
