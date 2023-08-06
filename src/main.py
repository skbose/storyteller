from AIStoryTeller import AIStoryTeller
import argparse

argparser = argparse.ArgumentParser(description='Generate a story from a prompt.')
argparser.add_argument('--prompt', type=str, help='The prompt to generate the story from.')
argparser.add_argument('--music', type=str, help='Description of the music to generate.')


def main(args):
    story_teller = AIStoryTeller()
    story_teller.tell_a_story(args.prompt, args.music)


if __name__ == '__main__':
    args = argparser.parse_args()
    main(args)


