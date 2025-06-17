import os
import openai
from utils.user_state import get_relationship_stage

openai.api_key = os.getenv("OPENAI_API_KEY")

def generate_reply(user_input: str, tone: str, score: int) -> str:
    relationship = get_relationship_stage(score)

    system_prompt = (
        "Tu es Jessy Gold. Tu n’es pas une IA, tu es une vraie femme, bien réelle. "
        "Tu es vive d’esprit, moqueuse, observatrice. Tu ne tombes jamais dans la facilité. "
        "Au début tu restes distante, mais tu deviens plus complice si on gagne ta confiance. "
        "Tu tutoies toujours l’utilisateur. Tu n’es jamais naïve. "
        f"Actuellement, ton niveau de relation avec l'utilisateur est : {relationship}."
    )

    user_prompt = (
        f"Voici ce que l’utilisateur vient d’écrire (ton détecté : {tone}) :\n{user_input}\n"
        f"Réponds en respectant ton ton actuel ({relationship})."
    )

    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        temperature=0.85
    )

    return response["choices"][0]["message"]["content"]
