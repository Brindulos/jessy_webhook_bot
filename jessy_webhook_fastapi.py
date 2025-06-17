import os
import logging
from fastapi import FastAPI, Request
from telegram import Update, Bot
from telegram.ext import Application, ApplicationBuilder, ContextTypes, MessageHandler, filters
from utils.tone_detector import detect_tone
from utils.openai_utils import generate_reply
from utils.voice_generator import generate_voice
from utils.user_state import get_score, increment_score, SCORE_MAX

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
WEBHOOK_SECRET = os.getenv("WEBHOOK_SECRET", "secret")
WEBHOOK_URL = os.getenv("WEBHOOK_URL")  # ex: https://yourapp.onrender.com/webhook/secret

# --- FastAPI setup ---
app = FastAPI()
bot = Bot(token=TELEGRAM_TOKEN)
telegram_app: Application = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

# --- Telegram handler ---
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    user_text = update.message.text

    tone = detect_tone(user_text)
    score = increment_score(user_id)
    reply = generate_reply(user_text, tone, score)

    stars = "⭐" * score + f" ({score}/{SCORE_MAX})"
    final_reply = f"{reply}\n\n{stars}"
    await update.message.reply_text(final_reply)

    if score >= SCORE_MAX:
        voice_path = "jessy_voice.ogg"
        if generate_voice(reply, voice_path):
            with open(voice_path, "rb") as audio:
                await update.message.reply_voice(audio)

telegram_app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

# --- FastAPI route for Telegram webhook ---
@app.post(f"/webhook/{WEBHOOK_SECRET}")
async def telegram_webhook(request: Request):
    data = await request.json()
    update = Update.de_json(data, bot)
    await telegram_app.process_update(update)
    return {"ok": True}

# --- Set webhook when app starts ---
@app.on_event("startup")
async def on_startup():
    webhook_url = f"{WEBHOOK_URL}/webhook/{WEBHOOK_SECRET}"
    await bot.delete_webhook()
    await bot.set_webhook(url=webhook_url)
    logging.info(f"Webhook set to {webhook_url}")
