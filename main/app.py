from flask import Flask, request, Response
from flask import send_file
from modules.AIStoryTeller import AIStoryTeller
import os
from flask_cors import CORS


app = Flask(__name__)

CORS(app)

OUTPUT_DIR = "/wavs/"
os.makedirs(OUTPUT_DIR, exist_ok=True)
story_teller = AIStoryTeller(wavs_dir=OUTPUT_DIR)


@app.before_request
def handle_preflight():
    if request.method == "OPTIONS":
        res = Response()
        res.headers['X-Content-Type-Options'] = '*'
        res.headers['Access-Control-Allow-Origin'] = '*'
        return res


@app.route("/generate_story", methods=['POST'])
def generate_story():
    # read request
    request_data = request.get_json()
    # read request
    prompt = request_data.get('prompt', None)
    music = request_data.get('music', None)
    
    if (prompt is None or music is None):
        return "Bad Request", 400
    
    story_teller.tell_a_story(prompt, music)
    path_to_file = "/wavs/final_story.wav"
    
    return send_file(
         path_to_file, 
         mimetype="audio/wav", 
         as_attachment=True, 
         download_name="story.wav")  

