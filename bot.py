import discord
import os
from dotenv import load_dotenv
import requests

# Load environment variables from Railway
load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")
CHANNEL_ID = int(os.getenv("CHANNEL_ID"))
CURRENT_CHAPTER = int(os.getenv("CURRENT_CHAPTER", 1))

# Load chapters
def load_chapters(filename="dao_de_jing.txt"):
    with open(filename, "r", encoding="utf-8") as f:
        return f.read().split("\\n\\n")

chapters = load_chapters()

intents = discord.Intents.default()
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'Logged in as {client.user}')
    channel = client.get_channel(CHANNEL_ID)

    if not channel:
        print("Error: Could not find channel.")
        await client.close()
        return

    # Post the current chapter
    if 1 <= CURRENT_CHAPTER <= len(chapters):
        await channel.send(f"**Dao De Jing - Chapter {CURRENT_CHAPTER}**\n{chapters[CURRENT_CHAPTER - 1]}")
        print(f"Posted Chapter {CURRENT_CHAPTER}")

        # Increment CURRENT_CHAPTER using Railway API
        new_chapter = CURRENT_CHAPTER + 1
        update_env_variable("CURRENT_CHAPTER", str(new_chapter))

    await client.close()


def update_env_variable(key, value):
    """ Update Railway environment variable using Railway API """
    RAILWAY_API_URL = os.getenv("RAILWAY_API_URL")
    RAILWAY_API_TOKEN = os.getenv("RAILWAY_API_TOKEN")

    if RAILWAY_API_URL and RAILWAY_API_TOKEN:
        headers = {
            "Authorization": f"Bearer {RAILWAY_API_TOKEN}",
            "Content-Type": "application/json"
        }
        
        data = {
            "variables": [
                {"key": key, "value": value}
            ]
        }

        try:
            response = requests.patch(f"{RAILWAY_API_URL}/variables", json=data, headers=headers)
            
            if response.status_code == 200:
                print(f"✅ Updated environment variable: {key} = {value}")
            else:
                print(f"❌ Failed to update variable: {response.status_code} - {response.text}")

        except requests.RequestException as e:
            print(f"🚨 API Request Failed: {e}")
    else:
        print("❗ Environment variables for Railway API are missing.")


client.run(TOKEN)
