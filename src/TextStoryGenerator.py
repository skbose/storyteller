import openai
import json
import os

class TextStoryGenerator:
    '''
    A class that generates a story given a prompt and model.
    '''

    def __init__(self, model_name="gpt-3.5-turbo", key=None):
        
        self.model = None
        self.model_name = model_name
        if(model_name.startswith("gpt-3.5-turbo")):
            if(key == None):
                raise Exception("Open AI key is required.")
            openai.api_key=key
            self.model = openai.ChatCompletion()
        # Default is chatGPT
        else:
            self.model = openai.ChatCompletion()

    def generate(self, prompt, max_length=200, num_return_sequences=1, temperature=None):
        if(prompt==""):
            return "Please provide the prompt."
        if(self.model_name.startswith("gpt-3.5-turbo")):
            if(temperature == None):
                temperature = 1
            completion = self.model.create(
                model=self.model_name,
                messages=[
                    {"role": "system", "content": prompt}
                ],
                temperature=temperature,
                n=num_return_sequences,
                max_tokens=max_length
            )

            return completion.choices[0].message.content



        return "Model name is not correct."    


