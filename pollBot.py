# https://github.com/Pycord-Development/pycord/blob/master/examples/views/confirm.py
# https://github.com/Pycord-Development/pycord/blob/master/examples/app_commands/slash_basic.py


import time
import random

import discord
from discord.ext import commands
from discord import Option
from discord import SlashCommand


TOKEN = "OTg5NDMzNTc5NzczNzc1OTAy.GlW4V9.9q1SrWh2h9qLu0OmPbTuwqeL7BgEFKhrm96p5I"

bot = discord.Bot(name="PollBot", command_prefix="+")
slash = SlashCommand(bot, sync_commands=True)
@bot.event
async def on_ready():
    print("Poll Bot ready.")
    print(f"Poll Bot ready via {bot.user}")

# note : option_type = 3 for string, 4 for integer, 5 for boolean

# poll command, callable via /poll "question" "number_of_possible_answers"
@slash.slash(name="poll", options=[], description="First poll function")
async def display_poll(ctx, question, answer1, answer2):
    question: Option(str, "the question to ask", required=True)
    #answer1: Option(str, "sentence that describes the 1st answer", required=True)
    #answer2: Option(str, "sentence that describes the 2nd answer", required=True)
    ctx.send("The question is " + question)


bot.run(TOKEN)