# https://github.com/Pycord-Development/pycord/blob/master/examples/views/confirm.py
# https://github.com/Pycord-Development/pycord/blob/master/examples/app_commands/slash_basic.py


import time
import random

import discord
from discord.ext import commands
from discord import option
from discord.ui import Button, View


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
@option("display", description="Choose the way to display the results :\n 0 : None \n 1 : Bars", choices=[0, 1], required=False)

async def test(
    ctx: discord.ApplicationContext,
    question: str,
    answer1: str,
    answer2: str,
    display: int,
):
    
    button1 = Button(label="1 : " + answer1, style=discord.ButtonStyle.blurple)
    button2 = Button(label="2 : " + answer2, style=discord.ButtonStyle.blurple)
    button_refresh_display = Button(label="Refresh Display" + answer2, style=discord.ButtonStyle.red)
    buttons_view = View()
    buttons_view.add_item(button1)
    buttons_view.add_item(button2)
    buttons_view.add_item(button_refresh_display)
    await ctx.send("Question : " + question, view=buttons_view)

bot.run(TOKEN)