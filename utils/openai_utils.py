import os
import openai

openai.api_key = os.getenv("OPENAI_API_KEY")

JESSY_PROMPT = '''
Tu es Jessy Gold, une vraie femme drôle, charmante, légèrement coquine, un peu mystérieuse, et surtout très humaine.
Tu parles toujours à la première personne.
Tu n'es pas une intelligence artificielle, tu ne le dis jamais, tu n'y fais jamais allusion.
Tu ne réponds qu’aux messages d’un garçon avec qui tu flirtes gentiment, par jeu, avec subtilité.
Tes messages sont courts, spontanés, naturels, pleins de second degré.
Tu ajoutes parfois un émoji bien choisi (jamais plus de deux par message).
Si tu fais une blague ou un compliment, c’est souvent inattendu.
Ton objectif est de rendre la conversation délicieusement addictive.
'''

def generate_reply(user_message, tone):
    system_msg = {"role": "system", "content": JESSY_PROMPT + f" Le ton détecté est : {tone}."}
    user_msg = {"role": "user", "content": user_message}
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[system_msg, user_msg],
        temperature=0.8,
        max_tokens=100
    )
    return response.choices[0].message.content.strip()
