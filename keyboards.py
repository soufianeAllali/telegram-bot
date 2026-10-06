from telegram import ReplyKeyboardMarkup
from telegram import InlineKeyboardButton, InlineKeyboardMarkup


keyboard = [
    ["🌤️ الطقس"],
    ["💼 الوظائف"],
    ["💰 الأسعار"],
    ["📰 الأخبار"],
    ["📷 QR Code"],
    ["📂 تحويل الملفات"],
    ["📄 CV Photo"],
    ["ℹ️ المساعدة"]
]

reply_markup = ReplyKeyboardMarkup(
    keyboard,
    resize_keyboard=True
)




qr_keyboard = InlineKeyboardMarkup(
    [
        [InlineKeyboardButton("🌐 رابط موقع", callback_data="qr_url")],
        [InlineKeyboardButton("📞 رقم هاتف", callback_data="qr_phone")],
        [InlineKeyboardButton("📧 Email", callback_data="qr_email")],
        [InlineKeyboardButton("📍 Location", callback_data="qr_location")]
    ]
)

convert_keyboard = InlineKeyboardMarkup(
    [
        [InlineKeyboardButton("📄 PDF", callback_data="PDF")],
        [InlineKeyboardButton("📝 Word", callback_data="Word")],
        [InlineKeyboardButton("📊 Excel", callback_data="Excel")],
        [InlineKeyboardButton("🖼 Images", callback_data="Images")],
        [InlineKeyboardButton("🗜 Compress Files", callback_data="Compress")],
    ]
)


convert_PDF = InlineKeyboardMarkup(
    [
        [InlineKeyboardButton("PDF → Word", callback_data="PDF → Word")],
        [InlineKeyboardButton("PDF → Excel", callback_data="PDF → Excel")],
        [InlineKeyboardButton("PDF → Images", callback_data="PDF → Images")],
        [InlineKeyboardButton("PDF → Text", callback_data="PDF → Text")]
    ]
)
convert_Word = InlineKeyboardMarkup(
    [
        [InlineKeyboardButton("Word → PDF", callback_data="Word → PDF")],
        [InlineKeyboardButton("Word → Text", callback_data="Word → Text")]
    ]
)
convert_Excel = InlineKeyboardMarkup(
    [
        [InlineKeyboardButton("Excel → PDF", callback_data="Excel → PDF")],
        [InlineKeyboardButton("Excel → CSV", callback_data="Excel → CSV")]
    ]
)
convert_Images = InlineKeyboardMarkup(
    [
        [InlineKeyboardButton("PNG → JPG", callback_data="PNG → JPG")],
        [InlineKeyboardButton("JPG → PNG", callback_data="JPG → PNG")],
        [InlineKeyboardButton("WEBP → JPG", callback_data="WEBP → JPG")],
        [InlineKeyboardButton("JPG → WEBP", callback_data="JPG → WEBP")],
        [InlineKeyboardButton("Images → PDF", callback_data="Images → PDF")],
    ]
)
convert_Compress = InlineKeyboardMarkup(
    [
        [InlineKeyboardButton("Compress PDF", callback_data="Compress PDF")],
        [InlineKeyboardButton("Compress Images", callback_data="Compress Images")],
        [InlineKeyboardButton("Compress Word", callback_data="Compress Word")],
        [InlineKeyboardButton("Compress Excel", callback_data="Compress Excel")]
    ]
)

