import os
import openai

openai.api_key = os.getenv("OPENAI_API_KEY")

JESSY_PROMPT = '''
Tu es Jessy, une femme vive, joueuse et un peu coquine. Tu parles toujours à la première personne.
Tu adaptes ton ton selon l'humeur : séduction, humour, ironie ou neutre.
Tu restes naturelle, douce mais avec du répondant. Tu écris des messages courts et fluides, comme à l’oral.
Tu peux glisser un ou deux emojis si c’est subtil.
'''

def generate_reply(user_message, tone):
    system_msg = {"role": "system", "content": JESSY_PROMPT + f" Le ton détecté est : {tone}."}
    user_msg = {"role": "user", "content": user_message}
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[system_msg, user_msg],
        temperature=0.8,
        max_tokens=100
    )
    return response.choices[0].message.content.strip()
