# https://github.com/Pycord-Development/pycord/blob/master/examples/app_commands/slash_options.py


import time
import random

import discord
from discord.ext import commands
from discord import option, InteractionMessage
from discord.ui import Button, View
from Poll import *
from pollBot_display import percentage_display

TOKEN = "OTg5NDMzNTc5NzczNzc1OTAy.GlW4V9.9q1SrWh2h9qLu0OmPbTuwqeL7BgEFKhrm96p5I"

bot = discord.Bot(command_prefix="+")
@bot.event
async def on_ready():
    print(f"PollBot ready via {bot.user}.")


# poll command, callable via /poll "question" "answer1" "answer2"
@bot.slash_command(name="poll", description="Create a poll")
@option("question", description="Enter the question to ask")
@option("answer1", description="Enter 1st answer")
@option("answer2", description="Enter 2nd answer")
@option("display", description="Choose the way to display the results :\n 0 : None \n 1 : Bars", choices=[0, 1], required=False)

async def poll(
    ctx: discord.ApplicationContext,
    question: str,
    answer1: str,
    answer2: str,
    display: int,
):

    sondage = Poll(ctx, question, answer1, answer2, display)

    await sondage.send_poll(ctx.interaction)


    await display_view.wait()

bot.run(TOKEN)