import os
from fastapi import FastAPI, Request
from telegram import Update
from telegram.ext import Application, ContextTypes, MessageHandler, filters
from telegram.ext import Dispatcher
from utils.tone_detector import detect_tone
from utils.openai_utils import generate_reply
from utils.voice_generator import generate_voice
import logging
import telegram

app = FastAPI()
BOT_TOKEN = os.getenv("TELEGRAM_TOKEN")
bot = telegram.Bot(token=BOT_TOKEN)
application = Application.builder().token(BOT_TOKEN).build()

async def handle(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text
    tone = detect_tone(user_text)
    reply = generate_reply(user_text, tone)
    await update.message.reply_text(reply)

    voice_path = "jessy_reply.ogg"
    if generate_voice(reply, voice_path):
        with open(voice_path, "rb") as voice_file:
            await update.message.reply_voice(voice_file)

application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle))

@app.post("/")
async def webhook(request: Request):
    data = await request.json()
    update = Update.de_json(data, bot)
    await application.process_update(update)
    return "ok"