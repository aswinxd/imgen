
import requests
from pyrogram import Client, filters

# Replace these with your own values
API_ID = '12799559'
API_HASH = '077254e69d93d08357f25bb5f4504580'
BOT_TOKEN = '6721122074:AAG-rzdsXUm9HP4BHXod-jclqukFmIw2CY8'
CRAIYON_API_URL = 'https://api.craiyon.com/generate'
LOCAL_SD_API_URL = 'http://localhost:7860/sdapi/v1/txt2img'

app = Client("imggen_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

@app.on_message(filters.command(["start"]))
async def start(client, message):
    await message.reply("Hello! Send me a text prompt and I will generate an image for you using Stable Diffusion.")

@app.on_message(filters.text & ~filters.command(["start"]))
async def generate_image(client, message):
    prompt = message.text
    response = requests.post(
        LOCAL_SD_API_URL,
        json={"prompt": prompt}
    )
    
    if response.status_code == 200:
        response_data = response.json()
        print("Response Data:", response_data)  # Log the response data for debugging
        images = response_data.get("images")
        if images:
            # Save the image locally and send it to the user
            image_data = images[0]
            with open("generated_image.png", "wb") as f:
                f.write(image_data.encode("latin1"))
            await message.reply_photo(photo="generated_image.png", caption="Here is your generated image!")
        else:
            await message.reply("Sorry, I couldn't generate an image. Please try again.")
    else:
        print("Error Response:", response.status_code, response.text)  # Log the error response for debugging
        await message.reply("There was an error with the image generation service. Please try again later.")

app.run()
