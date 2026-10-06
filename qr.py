from telegram import Update, ReplyKeyboardRemove
from telegram.ext import ContextTypes, ConversationHandler

import qrcode

from states import QR
from keyboards import *



async def qr_start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    await update.message.reply_text(
        "📷 اختر نوع QR Code:",
        reply_markup=qr_keyboard
    )

    return QR


async def qr_type(update: Update, context: ContextTypes.DEFAULT_TYPE):

    query = update.callback_query
    await query.answer()


    if query.data == "qr_url":

        context.user_data["qr_type"] = "url"

        await query.edit_message_text(
            "🌐 أرسل الرابط:"
        )


    elif query.data == "qr_phone":

        context.user_data["qr_type"] = "phone"

        await query.edit_message_text(
            "📞 أرسل رقم الهاتف:"
        )


    elif query.data == "qr_email":

        context.user_data["qr_type"] = "email"

        await query.edit_message_text(
            "📧 أرسل البريد الإلكتروني:"
        )


    elif query.data == "qr_location":

        context.user_data["qr_type"] = "location"

        await query.edit_message_text(
            "📍 أرسل الموقع بهذا الشكل:\nlatitude,longitude"
        )


    return QR



async def generate_qr(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user_data = update.message.text

    qr_type = context.user_data["qr_type"]



    if qr_type == "url":

        qr_data = user_data


    elif qr_type == "phone":

        qr_data = f"tel:{user_data}"


    elif qr_type == "email":

        qr_data = f"mailto:{user_data}"


    elif qr_type == "location":

        lat, lon = user_data.split(",")

        qr_data = (
            f"https://maps.google.com/?q={lat},{lon}"
        )



    qr = qrcode.QRCode(
        version=1,
        box_size=10,
        border=5
    )

    qr.add_data(qr_data)

    qr.make(fit=True)

    image = qr.make_image()

    image.save("qr_code.png")

    await update.message.reply_photo(
        photo=open("qr_code.png", "rb"),
        caption="📷 QR Code الخاص بك"
    )



    await update.message.reply_text(
        "اختر خدمة أخرى:",
        reply_markup=reply_markup
    )


    return ConversationHandler.END