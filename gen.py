import requests
from pyrogram import Client, filters

# Replace these with your own values
API_ID = '12799559'
API_HASH = '077254e69d93d08357f25bb5f4504580'
BOT_TOKEN = '6721122074:AAG-rzdsXUm9HP4BHXod-jclqukFmIw2CY8'
DEEPAI_API_KEY = '3958016b-fcf8-4ee8-be29-5c68a1e18791'
DEEPAI_API_URL = 'https://api.deepai.org/api/text2img'

app = Client("imggen_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

@app.on_message(filters.command(["start"]))
async def start(client, message):
    await message.reply("Hello! Send me a text prompt and I will generate an image for you using DeepAI.")

@app.on_message(filters.text & ~filters.command(["start"]))
async def generate_image(client, message):
    prompt = message.text
    response = requests.post(
        DEEPAI_API_URL,
        data={'text': prompt},
        headers={'api-key': DEEPAI_API_KEY}
    )
    
    if response.status_code == 200:
        image_url = response.json().get("output_url")
        if image_url:
            await message.reply_photo(photo=image_url, caption="Here is your generated image!")
        else:
            await message.reply("Sorry, I couldn't generate an image. Please try again.")
    else:
        await message.reply("There was an error with the image generation service. Please try again later.")

app.run()
