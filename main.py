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
import requests

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"Logged in and active as: {bot.user.name}")
    try:
        synced = await bot.tree.sync()
    except Exception as e:
        print(f"Error syncing commands: {e}")
        
@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    was_mentioned = bot.user in message.mentions
    is_reply_to_bot = False
    
    if message.reference and message.reference.cached_message:
        is_reply_to_bot = message.reference.cached_message.author == bot.user
    elif message.reference and not message.reference.cached_message:
        try:
            original_msg = await message.channel.fetch_message(message.reference.message_id)
            is_reply_to_bot = original_msg.author == bot.user
        except discord.HTTPException:
            pass

    if was_mentioned or is_reply_to_bot:
        await message.reply("beep boop this is my impression of a non-commital robot")
    await bot.process_commands(message)

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
        
def get_pypi_package_details(package_name):
    url = f"https://pypi.org/pypi/{package_name}/json"
    
    try:
        response = requests.get(url)
        
        if response.status_code == 404:
            return f"Error: Package '{package_name}' not found on PyPI."
            
        response.raise_for_status()
        data = response.json()
        
        info = data.get("info", {})
        
        return (
            info.get("name"),
            info.get("version"),
            info.get("summary"),
            info.get("author"),
            info.get("license"),
            info.get("home_page"),
            info.get("project_url"),
            info.get("requires_dist") or [],
            list(data.get("releases", {}).keys())
        )
        
    except requests.exceptions.RequestException as e:
        return f"An error occurred while connecting to PyPI: {e}"
    
@bot.tree.command(name="pypi", description="Displays a PyPI package by it's name.")
@app_commands.describe(name="The pypi package name")
async def pypi_package(interaction: discord.Interaction, name: str):
    if not name:
        await interaction.response.send_message("[ERROR] Must specify PyPI package.", ephemeral=True)
        return

    await interaction.response.defer()
    
    package_details = get_pypi_package_details(name)
    
    if isinstance(package_details, str):
        await interaction.followup.send(package_details)
        
    name, version, summary, author, _license, home_page, project_url, requires_dist, releases = package_details
    
    output = (
                f"*** {name} v{version} by {author}***\n"
                f"{summary}\n"
                f"{len(releases)} total releases\n"
                f"{project_url}"
            )
    
    await interaction.followup.send(output)

load_dotenv()

BOT_TOKEN = os.getenv("DISCORD_API")
if not BOT_TOKEN:
    raise ValueError("The environemtnal variable DISCORD_API is empty. Please replace it with the bot token.")
bot.run(BOT_TOKEN)