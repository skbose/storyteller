from TextStoryGenerator import TextStoryGenerator
if __name__ == '__main__':
    sample_prompt = "Write a story about a lion and mouse in less than 100 words."
    tsg = TextStoryGenerator(model_name="gpt-3.5-turbo", key="")
    print(tsg.generate(sample_prompt))