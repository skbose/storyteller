from transformers import AutoTokenizer
import transformers
import torch
import json


class TextStoryGenerator:
    '''
    A class that generates a story based on a prompt.
    '''

    # The default model to use for the generator.
    # facebook chat-llamav2 model from hugging face.
    DEFAULT_CHAT_MODEL = "daryl149/llama-2-7b-chat-hf"

    def __init__(self, model_id=DEFAULT_CHAT_MODEL) -> None:
        '''
        Initializes the TextStoryGenerator.
        @param model_id: The model id to use for the generator.
        '''

        self.model = model_id

        self.tokenizer = AutoTokenizer.from_pretrained(self.model)
        self.pipeline = transformers.pipeline(
            "text-generation",
            model=self.model,
            torch_dtype=torch.float16,
            device_map="auto",
        )

    def generate(self, prompt: str, top_k=10, num_return_sequences=1, max_length=1000):
        '''
        Generates a story based on the prompt.
        @param prompt: The prompt to generate the story from.
        @param top_k: The number of top k tokens to consider.
        @param num_return_sequences: The number of sequences to return.
        @param max_length: The maximum length of the generated text.
        @return: The generated text.
        '''
        prompt = '''
            SYSTEM: You are a helpful, respectful and honest assistant who tells stories to children.
            USER: {prompt}
            ASSISTANT:
        '''.format(prompt=prompt)

        sequences = self.pipeline(
            prompt,
            do_sample=True,
            top_k=top_k,
            num_return_sequences=num_return_sequences,
            eos_token_id=self.tokenizer.eos_token_id,
            max_length=max_length,
        )
        generated_text = sequences[0]['generated_text']
        assistant_index = generated_text.find('ASSISTANT:')
        generated_text = generated_text[assistant_index + len('ASSISTANT:'):]

        return generated_text


if __name__ == '__main__':
    sample_prompt = '''A moral story of a cow and goat.
    '''
    tsg = TextStoryGenerator()
    print(tsg.generate(sample_prompt))

