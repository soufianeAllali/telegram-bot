from telegram import Update, ReplyKeyboardRemove
from telegram.ext import ContextTypes, ConversationHandler
from states import *

import os
import io
import cv2
import numpy as np

from PIL import Image, ImageEnhance, ImageFilter, ImageOps
from rembg import remove

from states import *
from keyboards import reply_markup


async def cv_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "📷 أرسل صورتك لتحسينها وجعلها مناسبة للسيرة الذاتية"
    )
    return CV_PHOTO



OUTPUT_WIDTH = 1200
OUTPUT_HEIGHT = 1500

OUTPUT_SIZE = (
    OUTPUT_WIDTH,
    OUTPUT_HEIGHT
)

JPEG_QUALITY = 95


def improve_sharpness(image):
    return image.filter(
        ImageFilter.UnsharpMask(
            radius=0.8,
            percent=70,
            threshold=4
        )
    )



def remove_background(image):

    result = remove(image)

    if isinstance(result, bytes):

        result = Image.open(
            io.BytesIO(result)
        )

    return result.convert("RGBA")


def create_white_background(image_rgba):

    background = Image.new(
        "RGBA",
        image_rgba.size,
        (255, 255, 255, 255)
    )

    background.alpha_composite(
        image_rgba
    )

    return background.convert("RGB")




def detect_faces(image):
    cv_image = cv2.cvtColor(
        np.array(image),
        cv2.COLOR_RGB2BGR
    )

    gray = cv2.cvtColor(
        cv_image,
        cv2.COLOR_BGR2GRAY
    )

    cascade_path = (
        cv2.data.haarcascades +
        "haarcascade_frontalface_default.xml"
    )

    detector = cv2.CascadeClassifier(
        cascade_path
    )

    if detector.empty():
        return []

    faces = detector.detectMultiScale(
        gray,

        scaleFactor=1.08,

        minNeighbors=5,

        minSize=(80, 80)
    )

    return faces




def get_largest_face(faces):

    if len(faces) == 0:
        return None

    return max(
        faces,
        key=lambda face: face[2] * face[3]
    )



def crop_around_person(
    image,
    face
):


    width, height = image.size

    if face is None:

        target_ratio = 4 / 5

        current_ratio = width / height

        if current_ratio > target_ratio:

            new_width = int(
                height * target_ratio
            )

            left = (
                width - new_width
            ) // 2

            right = (
                left + new_width
            )

            return image.crop(
                (
                    left,
                    0,
                    right,
                    height
                )
            )

        else:

            new_height = int(
                width / target_ratio
            )

            top = (
                height - new_height
            ) // 2

            bottom = (
                top + new_height
            )

            return image.crop(
                (
                    0,
                    top,
                    width,
                    bottom
                )
            )


    x, y, w, h = face

    side_margin = int(
        w * 1.10
    )

    top_margin = int(
        h * 1.30
    )

    bottom_margin = int(
        h * 2.60
    )

    left = max(
        0,
        x - side_margin
    )

    right = min(
        width,
        x + w + side_margin
    )

    top = max(
        0,
        y - top_margin
    )

    bottom = min(
        height,
        y + h + bottom_margin
    )

    return image.crop(
        (
            left,
            top,
            right,
            bottom
        )
    )


def crop_to_ratio(
    image,
    target_ratio=4 / 5
):


    width, height = image.size

    current_ratio = width / height


    if current_ratio > target_ratio:

        new_width = int(
            height * target_ratio
        )

        left = (
            width - new_width
        ) // 2

        right = (
            left + new_width
        )

        image = image.crop(
            (
                left,
                0,
                right,
                height
            )
        )

    elif current_ratio < target_ratio:

        new_height = int(
            width / target_ratio
        )

        top = (
            height - new_height
        ) // 2

        bottom = (
            top + new_height
        )

        image = image.crop(
            (
                0,
                top,
                width,
                bottom
            )
        )

    return image



async def cv_start(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    await update.message.reply_text(
        "📷 أرسل صورتك لتحسينها وجعلها مناسبة للسيرة الذاتية.\n\n"

        "💡 للحصول على أفضل نتيجة:\n"

        "• استخدم صورة بجودة جيدة\n"
        "• اجعل الوجه واضحًا\n"
        "• واجه الكاميرا قدر الإمكان\n"
        "• تجنب الصور الجماعية\n"
        "• يفضل أن تكون الرأس والكتفين ظاهرين"
    )

    return CV_PHOTO




async def improve_cv_photo(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    original_path = None
    final_path = None

    try:


        if not update.message.photo:

            await update.message.reply_text(
                "❌ المرجو إرسال صورة."
            )

            return CV_PHOTO



        photo = update.message.photo[-1]


        file = await context.bot.get_file(
            photo.file_id
        )



        os.makedirs(
            "uploads",
            exist_ok=True
        )

        os.makedirs(
            "converted",
            exist_ok=True
        )

        original_path = (
            "uploads/cv_original.jpg"
        )

        final_path = (
            "converted/cv_photo.jpg"
        )



        await file.download_to_drive(
            original_path
        )

        await update.message.reply_text(
            "⏳ جاري تجهيز الصورة..."
        )



        image = Image.open(
            original_path
        )



        image = ImageOps.exif_transpose(
            image
        )

        # ====================================================
        # 8. تحويل إلى RGB
        # ====================================================

        image = image.convert(
            "RGB"
        )

        # ====================================================
        # 9. التحقق من جودة الصورة
        # ====================================================

        if image.width < 200 or image.height < 200:

            await update.message.reply_text(
                "❌ الصورة صغيرة جدًا.\n"
                "المرجو إرسال صورة بجودة أعلى."
            )

            return ConversationHandler.END

        # ====================================================
        # 10. إزالة الخلفية
        # ====================================================

        await update.message.reply_text(
            "🪄 جاري إزالة الخلفية..."
        )

        image_no_bg = remove_background(
            image
        )

        # ====================================================
        # 11. إنشاء خلفية بيضاء
        # ====================================================

        image = create_white_background(
            image_no_bg
        )

        # ====================================================
        # مهم جدًا:
        #
        # لا نقوم هنا بـ:
        #
        # ❌ White Balance
        # ❌ تغيير Brightness
        # ❌ تغيير Contrast
        # ❌ تغيير Color
        # ❌ CLAHE
        # ❌ تغيير Saturation
        #
        # وبالتالي نحافظ على ألوان الوجه الأصلية.
        # ====================================================

        # ====================================================
        # 12. اكتشاف الوجه
        # ====================================================

        await update.message.reply_text(
            "👤 جاري ضبط إطار الصورة..."
        )

        faces = detect_faces(
            image
        )

        face = get_largest_face(
            faces
        )

        # ====================================================
        # 13. قص حول الوجه والكتفين
        # ====================================================

        image = crop_around_person(
            image,
            face
        )

        # ====================================================
        # 14. ضبط نسبة 4:5
        # ====================================================

        image = crop_to_ratio(
            image,
            4 / 5
        )

        # ====================================================
        # 15. تغيير الحجم بجودة عالية
        # ====================================================

        image = image.resize(
            OUTPUT_SIZE,
            Image.Resampling.LANCZOS
        )

        # ====================================================
        # 16. تحسين حدة خفيف جدًا
        #
        # لا يغير لون البشرة.
        # ====================================================

        image = improve_sharpness(
            image
        )

        # ====================================================
        # 17. إنشاء Canvas أبيض نهائي
        # ====================================================

        canvas = Image.new(
            "RGB",
            OUTPUT_SIZE,
            (255, 255, 255)
        )

        canvas.paste(
            image,
            (0, 0)
        )

        # ====================================================
        # 18. حفظ الصورة
        # ====================================================

        canvas.save(
            final_path,

            "JPEG",

            quality=JPEG_QUALITY,

            optimize=True,

            progressive=True
        )

        # ====================================================
        # 19. إرسال الصورة
        # ====================================================

        with open(
            final_path,
            "rb"
        ) as photo_file:

            await update.message.reply_photo(

                photo=photo_file,

                caption=(
                    "✅ تم تجهيز الصورة بنجاح!\n\n"

                    "🧑‍💼 مناسبة للسيرة الذاتية\n"
                    "⬜ خلفية بيضاء\n"
                    "👤 قص احترافي\n"
                    "📐 أبعاد 4:5\n"
                    "✨ تحسين خفيف للجودة\n"
                    "🎨 الحفاظ على لون الوجه الطبيعي"
                )
            )

        # ====================================================
        # 20. إظهار القائمة
        # ====================================================

        await update.message.reply_text(
            "اختر خدمة أخرى:",
            reply_markup=reply_markup
        )

    # ========================================================
    # معالجة الأخطاء
    # ========================================================

    except Exception as e:

        print(
            "ERROR improve_cv_photo:",
            repr(e)
        )

        await update.message.reply_text(
            "❌ حدث خطأ أثناء تحسين الصورة.\n"
            "حاول إرسال صورة أخرى."
        )

    # ========================================================
    # حذف الملفات المؤقتة
    # ========================================================

    finally:

        if (
            original_path
            and os.path.exists(original_path)
        ):

            try:
                os.remove(
                    original_path
                )

            except Exception:
                pass

        if (
            final_path
            and os.path.exists(final_path)
        ):

            try:
                os.remove(
                    final_path
                )

            except Exception:
                pass

    return ConversationHandler.END

