import requests
from pyrogram import Client, filters

# Replace these with your own values
API_ID = 'your_api_id'
API_HASH = 'your_api_hash'
BOT_TOKEN = 'your_bot_token'
IMGGEN_API_URL = 'https://api.imggen.com/v1/generate'

app = Client("imggen_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

@app.on_message(filters.command("start"))
async def start(client, message):
    await message.reply("Hello! Send me a text prompt and I will generate an image for you using ImgGen AI.")

@app.on_message(filters.text & ~filters.command)
async def generate_image(client, message):
    prompt = message.text
    response = requests.post(IMGGEN_API_URL, json={"prompt": prompt})
    
    if response.status_code == 200:
        image_url = response.json().get("image_url")
        if image_url:
            await message.reply_photo(photo=image_url, caption="Here is your generated image!")
        else:
            await message.reply("Sorry, I couldn't generate an image. Please try again.")
    else:
        await message.reply("There was an error with the image generation service. Please try again later.")

app.run()