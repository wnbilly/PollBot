# https://github.com/Pycord-Development/pycord/blob/master/examples/app_commands/slash_options.py


import time
import random

import discord
from discord.ext import commands
from discord import option, InteractionMessage
from discord.ui import Button, View
from pollClass import Poll, PollWho
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
@option("answer2", description="Enter 2nd answer", required=False)
@option("answer3", description="Enter 3rd answer", required=False)
@option("answer4", description="Enter 4th answer", required=False)
@option("answer5", description="Enter 5th answer", required=False)
@option("answer6", description="Enter 6th answer", required=False)
@option("answer7", description="Enter 7th answer", required=False)
@option("answer8", description="Enter 8th answer", required=False)
@option("display", description="Choose the way to display the results :\n 0 : None \n 1 : Bars", choices=[0, 1], required=False)

async def poll(
    ctx: discord.ApplicationContext,
    question: str,
    answer1: str,
    answer2: str,
    answer3: str,
    answer4: str,
    answer5: str,
    answer6: str,
    answer7: str,
    answer8: str,
    display: int,
):
    print(f"{ctx.interaction.user.name} created a poll : " + question)
    answers = [answer1, answer2, answer3, answer4, answer5, answer6, answer7, answer8]
    poll = Poll(ctx, question, answers, display)
    await poll.send_poll(ctx.interaction)
    await poll.display_view.wait()

# poll command, callable via /poll_who "question"
@bot.slash_command(name="poll_who", description="Create a poll to know who")
@option("question", description="Enter the question to ask")

async def poll_who(
    ctx: discord.ApplicationContext,
    question: str,
    answer1: str,
    answer2: str,
    answer3: str,
    answer4: str,
    answer5: str,
    answer6: str,
    answer7: str,
    answer8: str,
    display: int,
):
    print(f"{ctx.interaction.user.name} created a pollWho : " + question)
    answers = [answer1, answer2, answer3, answer4, answer5, answer6, answer7, answer8]
    poll_who = PollWho(ctx, question)
    await poll_who.send_poll(ctx.interaction)
    await poll_who.display_view.wait()


bot.run(TOKEN)