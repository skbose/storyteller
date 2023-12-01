import gradio as gr


import requests

headers = {
    'Content-type':'application/json', 
    'Accept':'application/json'
}

def generate_story(prompt, music):
    url = "http://localhost:5000/generate_story"
    data = {
        "prompt": prompt,
        "music": music
    }
    response = requests.post(url, json=data, headers=headers)
    if response.status_code == 200:
        with open("final_story.wav", "wb") as f:
            f.write(response.content)
        return "final_story.wav"
    else:
        return None

iface = gr.Interface(fn=generate_story, 
                     inputs=["text", "text"], 
                     outputs=gr.Audio(type="filepath", label="Story Audio"))

iface.launch(share=True, server_name="0.0.0.0")
