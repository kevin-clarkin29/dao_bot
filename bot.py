import os
import discord
import psycopg2
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

TOKEN = os.getenv("DISCORD_TOKEN")
CHANNEL_ID = int(os.getenv("CHANNEL_ID", "0"))

# The PostgreSQL URL from Neon
DATABASE_URL = os.getenv("DATABASE_URL")

# Connect to Postgres
conn = psycopg2.connect(DATABASE_URL)
conn.autocommit = True
cursor = conn.cursor()

# Create table if it doesn't exist
cursor.execute("""
    CREATE TABLE IF NOT EXISTS progress (
        id SERIAL PRIMARY KEY,
        chapter INT NOT NULL
    );
""")

def get_current_chapter():
    cursor.execute("SELECT chapter FROM progress WHERE id = 1;")
    row = cursor.fetchone()
    if row:
        return row[0]
    else:
        # Insert default row (chapter=1)
        cursor.execute("INSERT INTO progress (id, chapter) VALUES (1, 1);")
        return 1

def save_current_chapter(ch):
    cursor.execute("""
        INSERT INTO progress (id, chapter)
        VALUES (1, %s)
        ON CONFLICT (id) DO UPDATE SET chapter = EXCLUDED.chapter;
    """, (ch,))

def load_chapters(filename="dao_de_jing.txt"):
    with open(filename, "r", encoding="utf-8") as f:
        # Split on literal "\n\n"  
        return f.read().split("\\n\\n")

chapters = load_chapters()

intents = discord.Intents.default()
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f"Logged in as {client.user}")

    if CHANNEL_ID == 0:
        print("CHANNEL_ID not set, exiting.")
        await client.close()
        return

    channel = client.get_channel(CHANNEL_ID)
    if not channel:
        print("Channel not found, exiting.")
        await client.close()
        return

    current_chapter = get_current_chapter()
    if 1 <= current_chapter <= len(chapters):
        # Post the current chapter
        await channel.send(f"**Dao De Jing - Chapter {current_chapter}**\n{chapters[current_chapter - 1]}")
        print(f"Posted Chapter {current_chapter}")

        # Increment and save
        new_chapter = current_chapter + 1
        save_current_chapter(new_chapter)
    else:
        await channel.send("All chapters have been posted!")
        print("Finished posting all chapters.")

    # Close after posting (if you run once a day)
    await client.close()

client.run(TOKEN)
