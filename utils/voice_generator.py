import os
import requests

ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY")
VOICE_ID = os.getenv("ELEVENLABS_VOICE_ID")  # Mets ton ID de voix ici ou via Render

def generate_voice(text, output_path):
    url = f"https://api.elevenlabs.io/v1/text-to-speech/{VOICE_ID}"

    headers = {
        "xi-api-key": ELEVENLABS_API_KEY,
        "Content-Type": "application/json"
    }

    payload = {
        "text": text,
        "model_id": "eleven_turbo_v2",  # Modèle performant, expressif et multilingue
        "voice_settings": {
            "stability": 0.4,
            "similarity_boost": 0.85,
            "style": 0.7,
            "use_speaker_boost": True
        }
    }

    response = requests.post(url, headers=headers, json=payload)

    if response.status_code == 200:
        with open(output_path, "wb") as f:
            f.write(response.content)
        return True
    else:
        print(f"[Erreur ElevenLabs] {response.status_code} : {response.text}")
        return False
