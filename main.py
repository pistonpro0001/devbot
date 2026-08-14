import discord
from discord import app_commands
from discord.ext import commands
import re
from collections import Counter
import datetime
import os
import random
import asyncio
import urllib.request
import json
import socket
from dotenv import load_dotenv

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

USER_PROFILES = {}
GAME_STATE = {"active": False, "word": "", "category": ""}

def get_or_create_profile(user_id, username):
    if user_id not in USER_PROFILES:
        USER_PROFILES[user_id] = {
            "name": username,
            "level": 1,
            "xp": 0,
            "gold": 100,
            "inventory": ["rusty_sword", "health_potion"]
        }
    return USER_PROFILES[user_id]

@bot.event
async def on_ready():
    print(f"Logged in and active as: {bot.user.name}")
    try:
        synced = await bot.tree.sync()
    except Exception as e:
        print(f"Error syncing commands: {e}")

@bot.tree.command(name="xkcd", description="Displays an xkcd comic by its number.")
@app_commands.describe(n="The comic number to fetch")
async def xkcd_comic(interaction: discord.Interaction, n: int):
    if n <= 0:
        await interaction.response.send_message("[ERROR] Comic number must be greater than 0.", ephemeral=True)
        return

    await interaction.response.defer()
    
    url = f"https://xkcd.com/{n}/info.0.json"
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "DiscordBot/1.0"})
        with urllib.request.urlopen(req) as response:
            data = json.loads(response.read().decode())
            
            title = data.get("title", "Unknown Title")
            img_url = data.get("img", "")
            alt_text = data.get("alt", "No alt text available.")
            
            output = (
                f"*** XKCD Comic #{n}: {title} ***\n"
                f"Alt Text: {alt_text}\n"
                f"{img_url}"
            )
            await interaction.followup.send(output)
            
    except urllib.error.HTTPError as e:
        if e.code == 404:
            await interaction.followup.send(f"Comic #{n} could not be found.")
        else:
            await interaction.followup.send(f"Failed to fetch comic data (HTTP Status {e.code}).")
    except Exception as e:
        await interaction.followup.send(f"An unexpected internal error occurred: {e}")

token_path = os.path.expanduser("~/Documents/bot-key.txt")

load_dotenv()

BOT_TOKEN = os.getenv("DISCORD_API")
if not BOT_TOKEN:
    raise ValueError("The environemtnal variable DISCORD_API is empty. Please replace it with the bot token.")
bot.run(BOT_TOKEN)