import discord
import os
from dotenv import load_dotenv

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

    # Post the current chapter and shut down
    if 1 <= CURRENT_CHAPTER <= len(chapters):
        await channel.send(f"**Dao De Jing - Chapter {CURRENT_CHAPTER}**\n{chapters[CURRENT_CHAPTER - 1]}")
        print(f"Posted Chapter {CURRENT_CHAPTER}")

    await client.close()

client.run(TOKEN)
