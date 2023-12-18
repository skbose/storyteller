import re
import json
from dataclasses import dataclass
from tqdm import tqdm
from openai import OpenAI
from pydub import AudioSegment


@dataclass
class StoryChunk:
    """
    A data class that represents a chunk of the story.
    """
    text: str
    openai_voice: str
    speed: float = 1.0


class OpenAITTS:
    """
    A class that uses OpenAI's Text-to-Speech (TTS) API to generate speech from text.
    """
    MALE_OPENAI_VOICES = ['echo', 'fable']
    FEMALE_OPENAI_VOICES = ['nova', 'shimmer']

    def __init__(self, key: str):
        """
        Initialize the OpenAI client with the provided API key.
        """
        self.client = OpenAI(api_key=key)

    def _parse_text_input(self, text: str) -> list[StoryChunk]:
        """
        Parse the input text, extracting character voices and story lines.
        """
        # parse the json string present in the header
        json_str = re.search(r'\{(.+?)\}\n}', text, re.DOTALL).group(0)
        json_data = json.loads(json_str)

        # read the character names and voices
        self.character_to_voice = {'narration': 'onyx'}
        voices = json_data.get('voices')
        
        male_idx = 0
        female_idx = 0

        # assign character voices
        for character_name in voices:
            voice = voices.get(character_name)
            if 'male' in voice:
                self.character_to_voice[character_name] = self.MALE_OPENAI_VOICES[male_idx]
                male_idx = (male_idx + 1) % 2
            elif 'female' in voice:
                self.character_to_voice[character_name] = self.FEMALE_OPENAI_VOICES[female_idx]
                female_idx = (female_idx + 1) % 2

        story_text = re.sub(json_str, '', text)
        story_lines = story_text.split('\n')

        self.parsed_story: list[StoryChunk] = []
        for _, line in enumerate(story_lines):
            line = line.strip()
            if line == "":
                continue
            
            if '<' in line and '>' in line:
                # Extract character name from the line
                character_name = re.search('<(.*)>', line).group(1)
            else:
                character_name = 'narration'
            
            # add stories to separate lists
            self.parsed_story.append(StoryChunk(
                text=line, 
                openai_voice=self.character_to_voice.get(character_name))
            )
        
        return self.parsed_story
    
    def generate_speech(self, client: OpenAI, model: str, voice: str, text: str, speed: float, output_path: str) -> None:
        """
        Generate speech from text using the OpenAI API and save it to a file.
        """
        response = client.audio.speech.create(
            model=model,
            voice=voice,
            input=text,
            speed=speed
        )
        response.stream_to_file(output_path)

    def generate_audio_and_save_to_file(self, text: str, output_path: str) -> None:
        """
        Generate audio from text and save it to a file.
        """
        self._parse_text_input(text=text)
        
        audio_segments = []
        print (self.parsed_story)
        for chunk in tqdm(self.parsed_story, total=len(self.parsed_story), desc="total lines"):
             # Generate speech for the line
            speech_file_path = f"tmp.mp3"
            self.generate_speech(
                self.client, 
                "tts-1",
                chunk.openai_voice, 
                chunk.text, 
                chunk.speed, 
                speech_file_path
            )
            
            # Load the generated speech audio into an AudioSegment
            audio_segment = AudioSegment.from_mp3(speech_file_path)
            audio_segments.append(audio_segment)

        # Create a one second silence audio segment
        one_sec_silence = AudioSegment.silent(duration=500)  # duration in milliseconds

        # Concatenate all audio segments with a one second delay between each
        combined_audio = audio_segments[0]
        for segment in audio_segments[1:]:
            combined_audio += one_sec_silence + segment

        # Export the combined audio to a single mp3 file
        combined_audio.export(output_path, format="mp3")


if __name__ == '__main__':
    text = '''
{
"characters": {
    "Lakshman": "The Mighty Lion",
    "Chintu": "The Coward Fox"
},
"voices": {
    "Lakshman": "male",
    "Chintu": "male"
}
}

Once upon a time, in the heart of the lush jungles of Sundarban, there lived two friends named Lakshman, the mighty lion, and Chintu, the coward fox.

<Lakshman>: "Greetings, Chintu! How about we explore the jungle today?"

<Chintu>: "Oh, Lakshman, my dear friend, I'm afraid. The jungle is full of dangers. I'd rather stay here where it's safe."

Moral of the Story:
"True strength is not just in physical might but also in the courage to face one's fears and help others in need."	
    '''

    openai_tts = OpenAITTS(key="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")
    openai_tts.generate_audio_and_save_to_file(text=text, output_path="story.mp3")
