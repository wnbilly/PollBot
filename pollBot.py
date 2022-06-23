# https://github.com/Pycord-Development/pycord/blob/master/examples/views/confirm.py
# https://github.com/Pycord-Development/pycord/blob/master/examples/app_commands/slash_basic.py


import time
import random

import discord
from discord.ext import commands
from discord import option
from discord.ui import Button


TOKEN = "OTg5NDMzNTc5NzczNzc1OTAy.GlW4V9.9q1SrWh2h9qLu0OmPbTuwqeL7BgEFKhrm96p5I"

bot = discord.Bot(command_prefix="+")
@bot.event
async def on_ready():
    print(f"PollBot ready via {bot.user}.")

# note : option_type = 3 for string, 4 for integer, 5 for boolean

# poll command, callable via /poll "question" "answer1" "answer2"
@bot.slash_command(name="poll", description="Create a poll")
@option("question", description="Enter the question to ask")
@option("answer1", description="Enter 1st answer")
@option("answer2", description="Enter 2nd answer")
@option("gender", description="Choose your gender", choices=["Male", "Female", "Other"])

async def test(
    ctx: discord.ApplicationContext,
    question: str,
    answer1: str,
    answer2: int,
):
    await ctx.send("The question is " + question)

bot.run(TOKEN)