# Storyteller
Storyteller from Fables.ai is an AI powered story teller that lets you create beautiful and engaging audio stories in less than few seconds.

## Requirements
Create a conda environment

`conda create -n fables python=3.10`

Install the python requirements using pip

`pip install -r <repo_root>/requirements.txt`

Install FFmpeg

`wget https://johnvansickle.com/ffmpeg/builds/ffmpeg-git-amd64-static.tar.xz`

`tar xvf ffmpeg-git-amd64-static.tar.xz`

Adding to PATH

`vi ~/.bashrc`

`export PATH="/path/to/ffmpeg-git-DATE-amd64-static:$PATH"`

`source ~/.bashrc`

## Usage
To generate a story, think of a prompt and a background music you would like to hear.

`python main.py --prompt "A story of a lion and rabbit.' --music 'happy piano' --output_dir '../wavs'`

Wait and watch as your story is generated in seconds. Hope you like it!
