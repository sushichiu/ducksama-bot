import os
import logging
import urllib.request
from datetime import time
from telegram.ext import Application, ContextTypes
import pytz

BOT_TOKEN = "8949309984:AAEpvbV6-_pY9xWRqZ8lC1LUS_RlkLCfNzo"
GROUP_CHAT_ID = -1003935793897
TIMEZONE = pytz.timezone("Asia/Tehran")

IMAGES_DIR = "images"
STATE_FILE = "state.txt"
GITHUB_REPO = "https://github.com/sushichiu/ducksama-bot/tree/main/images"
GITHUB_RAW = "https://raw.githubusercontent.com/sushichiu/ducksama-bot/main/images/"

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(message)s")
logger = logging.getLogger(__name__)

IMAGE_NAMES = [
    "00d94539e1fe593f28a461241b5ba6df.jpg",
    "04461dd0aa9a27e931184ae3e3d4742e.jpg",
    "0b30e345e16ab97a6374a1614bcbb2c9.jpg",
    "0bde944df293382056d656be2a62a7ae.jpg",
    "1382e4182300da26cfaa172bdd7b1f95.jpg",
    "153ed727f804378f43d9695869ad5e5e.jpg",
    "161f0d1bec4982d1d201494c234396f5.jpg",
    "17af9e35a5b88b51e145c4a920bd6c7f.jpg",
    "18720c4e67ec06df493af4bcd0877860.jpg",
    "18ed02a0bf0a84db18345129035adbf6.jpg",
    "193bad99837416e066212770529803d7.jpg",
    "1b35715b0246183ae620bb2798a256d3.jpg",
    "1d2c013a7744239637e816ada4fe6daf.jpg",
    "1dd5f917fc3986aad04f69a04dfdc97b.jpg",
    "1de134d625ed38f368a14b87685cf7dd.jpg",
    "1f1cc50c4ed754bfd4a60830bf55b6b7.jpg",
    "288a67b6f2d5ebbf57215a1712d66c3c.jpg",
    "290e6221aacc3862d1bc58a0d224b3cc.jpg",
    "2c24b147131a7a3b705479d7abd859c9.jpg",
    "2cc033b0b11c3570b7e77d830fe86772.jpg",
    "301b85804b014d9757d518cfb25db2f3.jpg",
    "310752c890e1f1b9bfb8ff96d998a258.jpg",
    "310853d56f715e8d50e9820c1e27a090.jpg",
    "3225c48f26e6591eae048f25ad32507e.jpg",
    "36772aac84d681d0ed76f6dce3b4819f.jpg",
    "3a3f3f8db4ae49fc80dcd27a452e1818.jpg",
    "3c323d0606f3ba5e31f9c217fc9e3bc5.jpg",
    "450fd2be76a996a6c3ab1c431b35be99.jpg",
    "455802825fea7b8e3c8096f3f8d8013f.jpg",
    "4c14288e0ec7647360531baa1c498011.jpg",
    "4de51c62c00196b7abacd8be38a8c69b.jpg",
    "51baa853e5aad0224031f56c1d4679bd.jpg",
    "53dfa03195154261dfaadd1116adc48d.jpg",
    "56181cbe72daef29cc73c6b629a5fd90.jpg",
    "5afd997338875a0a0252860d54dc7a21.jpg",
    "5ee2aa33419c325b54552c7bfcce3051.jpg",
    "5f41f61874b0597ca49f39b5c37db0a3.jpg",
    "64ae6c2c3caaa2cac025bda3c119d9b6.jpg",
    "79b9b0580cb42bd6df51af9697c57eb5.jpg",
    "7a91431c19203868cdc5d7ed3881057f.jpg",
    "81690f8338d1ce5284706833f6ba8e2f.jpg",
    "8629a79651d10dc513badc7bd4a74146.jpg",
    "88b4a2dbcf94ae5e5c1ccac2a77c656d.jpg",
    "8b4b9d07732fe57144c3cd7a10923842.jpg",
    "8bf89cf1a1949404df335a3821d0fb9f.jpg",
    "8c687c7323bbebe2053f95bd8522ae5c.jpg",
    "8d23f5d170ecba837ccc315760804a82.jpg",
    "8dfc3b77fd38df2d6905d568e868bc31.jpg",
    "933a52fa3411929f065358091f91d79c.jpg",
    "93e7cab3e327075da05472594daae1ef.jpg",
    "958c0bf5b5fbecb3c58edf8b97a28154.jpg",
    "96f220ebbf7c4046ced521fa79d12d21.jpg",
    "978f62a54aa3dbc2308d150ca2b341f7.jpg",
    "98109cf3ce8310d1ef19187d0787e60e.jpg",
    "a00f2e4a2c2c13d441eb0c9b58ea5d40.jpg",
    "a472e8b42d7b147564064168207d0869.jpg",
    "a5630e17e21b58f7656b81eeb88828b0.jpg",
    "af74eea135b8048f9ccabef18ae84897.jpg",
    "b045f72d1cb1d86e3e1d3c03e26081e0.jpg",
    "b17471cc6382fdec7393c4d6c56b7e4c.jpg",
    "b2d7b2604ae77b303f05d4d75ec6a057.jpg",
    "bc41c003f063d3a94136567be322dcf3.jpg",
    "bc7c3838aff5873a3feeb90acb948cd7.jpg",
    "bf622d6da9522fb639a54bc6961fbba1.jpg",
    "c0c56846e667bd92d239197e4df1adcb.jpg",
    "c43cdcde551078e18b76392890fdc441.jpg",
    "c54bdf1e28a38f45c2bd2bc96515418a.jpg",
    "c6d3b453ee9b4204c80e59a78d4cbb6d.jpg",
    "c90269f1478e080463f89dfa3ba8d0ed.jpg",
    "cf09bf0ea14f35ea4de509ecc816c3ae.jpg",
    "d71988bd484cf086c173f663be568dd0.jpg",
    "d8137a0ac813f2d714719626f4f49417.jpg",
    "d8c33fdb7956cda8ed88a5858506b6db.jpg",
    "da93364e5a4913805eb7b2cf2d317096.jpg",
    "db287d5acf3ac3bc907a12bd45d28cbd.jpg",
    "dcd241d10dfaec010fddf001c9372e43.jpg",
    "e443b37d852297d89f702e53063a9288.jpg",
    "e84f8c3dd23b2d8ce2d5fbc9b72aa9d6.jpg",
    "ec8a40d69b91a7cac4bca750d9a8f2f1.jpg",
    "f378139e6e5d7e93ff64701e57fc9395.jpg",
    "f6256c56b6e9ab37940e6cbefc3dac11.jpg",
    "f7853b8694ef9e609e6af6152514a541.jpg",
    "fb4e63445d93f66becc5069722a5920c.jpg",
    "fcc3f35b5659b014d85da111d805a8a7.jpg",
    "fcecc86910df910bb359778aa9734021.jpg",
    "fdc240d54659ed71bf724e54600806db.jpg",
]


def get_images():
    if not os.path.exists(IMAGES_DIR):
        os.makedirs(IMAGES_DIR)
    return IMAGE_NAMES


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
        logger.warning("No images!")
        return

    index = get_index()
    if index >= len(images):
        index = 0

    image_name = images[index]
    image_url = GITHUB_RAW + image_name
    temp_path = os.path.join(IMAGES_DIR, image_name)

    logger.info(f"Downloading: {image_name}")
    try:
        urllib.request.urlretrieve(image_url, temp_path)
        logger.info(f"Sending: {image_name}")
        with open(temp_path, "rb") as photo:
          await context.bot.send_photo(chat_id=GROUP_CHAT_ID, photo=photo)
        save_index(index + 1)
        logger.info("Sent!")
        os.remove(temp_path)
    except Exception as e:
        logger.error(f"Failed: {e}")



def main():
    app = Application.builder().token(BOT_TOKEN).build()
    app.job_queue.run_daily(
        send_daily_image,
        time=time(hour=6, minute=30, tzinfo=TIMEZONE),
        name="daily_image"
    )
    app.run_polling(drop_pending_updates=True)


if __name__ == "__main__":
    main()
