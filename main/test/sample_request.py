import requests

# url = "http://localhost:5000/generate_story"
url = "http://74.235.105.189:5000/generate_story"

data = {
    "prompt": "Write a story about a lion and rabbit in 100 words.",
    "music": "happy piano for moral story."
}

response = requests.post(url, json=data)
print (response)

if response.status_code == 200:
    download_speed = len(response.content) / (response.elapsed.total_seconds() * 1024 * 1024)
    print(f"Download speed: {round(download_speed, 2)} mb/s")
    with open("story.wav", "wb") as f:
        f.write(response.content)
        print("Story audio saved successfully!")
else:
    print("Failed to generate story audio.")
