from flask import Flask, request, Response
from flask import send_file
from modules.AIStoryTeller import AIStoryTeller
import os


app = Flask(__name__)

DEBUG = True

if DEBUG:
    OUTPUT_DIR = "wavs/"
else:
    OUTPUT_DIR = "/wavs/"

os.makedirs(OUTPUT_DIR, exist_ok=True)
story_teller = AIStoryTeller(wavs_dir=OUTPUT_DIR)


@app.route("/generate_story", methods=['POST'])
def generate_story():
    # read request
    request_data = request.get_json()

    prompt = request_data.get('prompt', None)
    music = request_data.get('music', None)
    
    if (prompt is None or music is None):
        return "Bad Request", 400
    
    story_teller.tell_a_story(prompt, music)
    path_to_file = os.path.join(OUTPUT_DIR, "final_story.wav")
    
    return send_file(
         path_to_file, 
         mimetype="audio/wav", 
         as_attachment=True, 
         download_name="story.wav")  
