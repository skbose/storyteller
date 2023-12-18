from openai import OpenAI
import json
import os


CONTEXT = '''
You are StoryGPT. Your job is to create short moral panchatantra stories for kids with age less than four.
'''

TEMPLATE_PROMPT = '''
### Instructions ###
Start writing a story in a visual manner, like being written by a famous author. Tailor the story towards famous Indian folk tales like Panchatantra. You should also refrain from making the book too vulgar. The story should be in a conversational format following a template. The template comprises of the narration, and the dialogues of the different characters in double quotes. Each line should either begin with a narration or the character name inside <>. Each character should have an Indian name which signifies the traits of the character.

Template:

<narration>: Some narration of the story
<character_1>: Dialogue of the character 1 in double quotes
<character_2>: Dialogue of character 2 in double quotes

The story should be flesch-kincaid grade level less than one. Return the names of characters at begining in a json format, along with the voice of the character. 
The story should follow a moral theme and you should provide a moral or a quote at the end. All the names of places should be Indian.
Create a short and simple story for kids aged 3-6.
Keep the language and plot easy to understand for young children.

### Examples ###

Human: Story of the cow and the lion

AI:
{
  "characters": {
    "Gopal": "The Kind Cow",
    "Raj": "The Smart Lion"
  },
  "voices": {
    "Gopal": "male",
    "Raj": "male"
  },
  "pitch": {
    "Gopal": "MEDIUM",
    "Raj": "MEDIUM"
  }
}
Once upon a time, in a happy village called Anandgram, there were two friends - Gopal, the kind cow, and Raj, the smart lion.

<Gopal>: "Hello, Raj! Let's sit under the big tree and tell happy stories today."
<Raj>: "Good idea, Gopal! I love happy stories."
One day, a not-so-nice person came to the village. Gopal, being kind, went to Raj for help.

<Gopal>: "Raj, our village needs help. What do we do?"
<Raj>: "Don't worry, Gopal. We can use our smarts to keep everyone safe."
Raj had a plan. He told the villagers to hide, and Gopal helped everyone find good hiding spots.
The not-so-nice person looked for people but couldn't find anyone. Confused, he left the village and never came back.

<Gopal>: "Raj, your smart plan saved us! Thank you!"
<Raj>: "Being strong is not just about muscles, Gopal. It's also about using our brains to solve problems."

After that day, Gopal and Raj continued telling happy stories under the big tree. They taught everyone in the village about being kind and smart.

Moral of the Story:
"Being strong means using your heart and brain to help others and solve problems."

Human: '''

class TextStoryGenerator:
    '''
    A class that generates a story given a prompt and model.
    '''

    def __init__(self, key, model_name="gpt-3.5-turbo"):
        
        self.model_name = model_name
        if(model_name.startswith("gpt-3.5-turbo")):
            if(key == None):
                raise Exception("Open AI key is required.")
            self.client = OpenAI(api_key=key)

    def generate(self, prompt):
        if(prompt==""):
            return "Please provide the prompt."
        print (prompt)
        if(self.model_name.startswith("gpt-3.5-turbo")):
            completion = self.client.chat.completions.create(
                model=self.model_name,
                messages=[
                    {"role": "system", "content": CONTEXT},
                    {"role": "user", "content": TEMPLATE_PROMPT + prompt + '\nAI:'}
                ]
            )
            return completion.choices[0].message.content

        return "Model name is not correct."    

if __name__ == "__main__":
    tts = TextStoryGenerator(key="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")
    print (tts.generate(prompt='The story of a lion and the tiger'))
