from telegram import Update, ReplyKeyboardRemove
from telegram.ext import ContextTypes
from states import *
import requests
from keyboards import reply_markup
from telegram.ext import ConversationHandler

async def news(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "ما الموضوع الذي تريد البحث عنه؟",
        reply_markup=ReplyKeyboardRemove()
    )
    return NEWS

async def get_news(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.message.text
    API_KEY = "bf37f28f9c6d4c1d8bb2f9882feb5a2d"

    url = "https://newsapi.org/v2/everything"

    params = {
        "q": query,
        "language": "ar",
        "apiKey": API_KEY,
        "pageSize": 5
    }

    response = requests.get(url, params=params)

    data = response.json()
    if not data["articles"]:
        await update.message.reply_text(
            "لم أجد أخبارًا عن هذا الموضوع.",
            reply_markup=reply_markup
        )
        return ConversationHandler.END
    

    for article in data["articles"]:

        message = (
            f"📰 {article['title']}\n\n"
            f"📄 {article['description']}\n\n"
            f"📰 المصدر: {article['source']['name']}\n"
            f"📅 {article['publishedAt']}\n\n"
            f"🔗 {article['url']}"
        )

        await update.message.reply_text(message)
    await update.message.reply_text(reply_markup=reply_markup)
    return ConversationHandler.END

    