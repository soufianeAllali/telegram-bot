from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes, ConversationHandler
import requests

from states import *
from keyboards import reply_markup

reply_markup_prices = InlineKeyboardMarkup(
    [
        [InlineKeyboardButton("USD", callback_data="USD")],
        [InlineKeyboardButton("EUR", callback_data="EUR")],
        [InlineKeyboardButton("GBP", callback_data="GBP")],
    ]
)

async def prices(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "💰 اختر العملة لمعرفة أسعارها:",
        reply_markup=reply_markup_prices
    )
    return PRICE

async def get_prices(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    currency = query.data

    url = f"https://v6.exchangerate-api.com/v6/7e624c2f01fa7d6dcd18cc8c/latest/{currency}"
    response = requests.get(url)
    data = response.json()

    mad = data["conversion_rates"]["MAD"]

    await query.message.reply_text(
        f"💰 1 {currency} = {mad} MAD"
    )
    return ConversationHandler.END