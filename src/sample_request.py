import requests

url = "http://localhost:5000/generate_story"

data = {
    "prompt": "Write a story about a lion and rabbit in 100 words.",
    "music": "happy piano for moral story."
}

response = requests.post(url, json=data)

if response.status_code == 200:
    with open("story.wav", "wb") as f:
        f.write(response.content)
        print("Story audio saved successfully!")
else:
    print("Failed to generate story audio.")
