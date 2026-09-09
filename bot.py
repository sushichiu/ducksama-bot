import os
import logging
from datetime import time
from telegram.ext import Application, ContextTypes
import pytz

BOT_TOKEN = "8949309984:AAEpvbV6-_pY9xWRqZ8lC1LUS_RlkLCfNzo"
GROUP_CHAT_ID = -1003935793897
TIMEZONE = pytz.timezone("Asia/Tehran")

IMAGES_DIR = "images"
STATE_FILE = "state.txt"

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(message)s")
logger = logging.getLogger(__name__)

def get_images():
    if not os.path.exists(IMAGES_DIR):
        os.makedirs(IMAGES_DIR)
        return []
    supported = (".jpg", ".jpeg", ".png", ".gif", ".webp")
    return sorted([f for f in os.listdir(IMAGES_DIR) if f.lower().endswith(supported)])


def get_index():
    if not os.path.exists(STATE_FILE):
        return 0
    try:
        with open(STATE_FILE, "r") as f:
            return int(f.read().strip())
    except:
        return 0


def save_index(index):
    with open(STATE_FILE, "w") as f:
        f.write(str(index))


async def send_daily_image(context: ContextTypes.DEFAULT_TYPE):
    images = get_images()
    if not images:
        logger.warning("No images in 'images' folder!")
        return

    index = get_index()
    if index >= len(images):
        index = 0

    image_path = os.path.join(IMAGES_DIR, images[index])
    logger.info(f"Sending: {images[index]}")

    try:
        with open(image_path, "rb") as photo:
           await context.bot.send_photo(chat_id=GROUP_CHAT_ID, photo=photo, message_thread_id=1)
        save_index(index + 1)
        logger.info("Sent!")
    except Exception as e:
        logger.error(f"Failed: {e}")


async def post_init(application: Application):
    logger.info("Bot started! Sending 1 pic daily at 6:00 AM Iran time.")
    await send_daily_image(application)


def main():
    app = Application.builder().token(BOT_TOKEN).post_init(post_init).build()
    app.job_queue.run_daily(
        send_daily_image,
       time=time(hour=7, minute=20, tzinfo=TIMEZONE),
        name="daily_image"
    )
    app.run_polling()


if __name__ == "__main__":
    main()
