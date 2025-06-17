import os
import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, filters

from utils.tone_detector import detect_tone
from utils.openai_utils import generate_reply
from utils.voice_generator import generate_voice
from utils.user_state import get_score, increment_score, SCORE_MAX

logging.basicConfig(level=logging.INFO)

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    user_text = update.message.text

    tone = detect_tone(user_text)
    score = increment_score(user_id)
    reply = generate_reply(user_text, tone, score)

    # Affichage du score sous forme d'étoiles
    stars = "⭐" * score + f" ({score}/{SCORE_MAX})"
    final_reply = f"{reply}\n\n{stars}"

    await update.message.reply_text(final_reply)

    # Envoie la voix uniquement si le score max est atteint
    if score >= SCORE_MAX:
        voice_path = "jessy_voice.ogg"
        if generate_voice(reply, voice_path):
            with open(voice_path, "rb") as audio:
                await update.message.reply_voice(audio)

if __name__ == "__main__":
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.run_polling()
