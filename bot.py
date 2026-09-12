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
    logger.info(f"Looking for images in: {os.getcwd()}/{IMAGES_DIR}")
    if not os.path.exists(IMAGES_DIR):
        logger.info("Images folder does not exist, creating it...")
        os.makedirs(IMAGES_DIR)
        return []
    
    all_files = os.listdir(IMAGES_DIR)
    logger.info(f"All files in images folder: {all_files}")
    
    supported = (".jpg", ".jpeg", ".png", ".gif", ".webp")
    images = sorted([f for f in all_files if f.lower().endswith(supported)])
    logger.info(f"Found {len(images)} images: {images}")
    return images


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
        logger.warning("No images found!")
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
    logger.info("Bot started!")
    await send_daily_image(application)


def main():
    app = Application.builder().token(BOT_TOKEN).post_init(post_init).build()
    app.job_queue.run_daily(
        send_daily_image,
        time=time(hour=14, minute=25, tzinfo=TIMEZONE),
        name="daily_image"
    )
    app.run_polling(drop_pending_updates=True)


if __name__ == "__main__":
    main()
