from flask import Flask, request
from flask import send_file
from AIStoryTeller import AIStoryTeller


app = Flask(__name__)
story_teller = AIStoryTeller(wavs_dir="../wavs/")


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
    path_to_file = "../wavs/final_story.wav"
    
    return send_file(
         path_to_file, 
         mimetype="audio/wav", 
         as_attachment=True, 
         download_name="story.wav")  


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
