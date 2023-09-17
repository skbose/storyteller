from AIStoryTeller import AIStoryTeller
import argparse
import os


argparser = argparse.ArgumentParser(description='Generate a story from a prompt.')
argparser.add_argument('--prompt', type=str, help='The prompt to generate the story from.', default="Write a story about a lion and rabbit in 100 words.")
argparser.add_argument('--music', type=str, help='Description of the music to generate.', default="happy piano for moral story.")
argparser.add_argument("--output_dir", type=str, help="Output audios will be stored here", default="../wavs/")


def main(args):
    # make directory
    os.makedirs(args.output_dir, exist_ok=True)
    story_teller = AIStoryTeller(wavs_dir=args.output_dir)
    story_teller.tell_a_story(args.prompt, args.music)


if __name__ == '__main__':
    args = argparser.parse_args()
    main(args)
