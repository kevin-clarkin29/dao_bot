import discord
import os
import asyncio
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")
CHANNEL_ID = int(os.getenv("CHANNEL_ID"))

# Load Dao De Jing chapters from a text file
def load_chapters(filename="dao_de_jing.txt"):
    with open(filename, "r", encoding="utf-8") as f:
        text = f.read()
        # Use the literal string "\n\n" as a delimiter
        return text.split("\\n\\n")  # Splitting on the literal "\n\n" string

chapters = load_chapters()

intents = discord.Intents.default()
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'Logged in as {client.user}')
    channel = client.get_channel(CHANNEL_ID)

    if not channel:
        print("Error: Could not find channel.")
        return

    for i, chapter in enumerate(chapters, start=1):
        await channel.send(f"**Dao De Jing - Chapter {i}**\n{chapter}")
        print(f"Posted Chapter {i}")

        if i < len(chapters):  # Wait 24 hours before posting next chapter
            await asyncio.sleep(24 * 60 * 60)

client.run(TOKEN)
