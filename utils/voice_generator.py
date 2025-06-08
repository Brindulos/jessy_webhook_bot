import os
import requests

def generate_voice(text, filename):
    api_key = os.getenv("ELEVEN_API_KEY")
    voice_id = "axGsyNadHjtfNCJqysRT"
    url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"

    headers = {
        "xi-api-key": api_key,
        "Content-Type": "application/json"
    }

    payload = {
        "text": text,
        "model_id": "eleven_multilingual_v2",
        "voice_settings": {
            "stability": 0.5,
            "similarity_boost": 0.8
        }
    }

    response = requests.post(url, headers=headers, json=payload)
    if response.status_code == 200:
        with open(filename, "wb") as f:
            f.write(response.content)
        return True
    else:
        print("Erreur vocal:", response.status_code, response.text)
        return False
