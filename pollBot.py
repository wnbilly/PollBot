# https://github.com/Pycord-Development/pycord/blob/master/examples/app_commands/slash_options.py


import time
import random

import discord
from discord.ext import commands
from discord import option, InteractionMessage, ApplicationCommand, MessageCommand
from discord.ui import Button, View
from pollClass import Poll, PollWho, PollFillingModal, PollWhoFillingModal
from pollBot_display import percentage_display
from reactClass import React

TOKEN = "OTg5NDMzNTc5NzczNzc1OTAy.GlW4V9.9q1SrWh2h9qLu0OmPbTuwqeL7BgEFKhrm96p5I"

bot = discord.Bot(command_prefix="+")
@bot.event
async def on_ready():
    print(f"{bot.user} ready.")


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
    poll = Poll(ctx, question, answers)
    await poll.send_poll() # ctx.interaction 
    await poll.display_view.wait()

# poll command, callable via /poll_who "question"
@bot.slash_command(name="poll_who", description="Create a poll to know who")
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
    poll_who = PollWho(ctx, question, answers)
    await poll_who.send_poll()
    await poll_who.buttons_view.wait()


# poll message command, callable via message context menus
@bot.message_command(name="Create a poll", description="Create a poll with a percentage bars display via a modal")
async def poll_app_command(
    ctx: discord.ApplicationContext,
    msg: discord.Message
):
    modal = PollFillingModal(title="Poll Filling Modal", ctx=ctx)
    
    await ctx.interaction.response.send_modal(modal)


# poll_who message command, callable via message context menus
@bot.message_command(name="Create a pollWho", description="Create a poll with a names display via a modal")
async def poll_who_app_command(
    ctx: discord.ApplicationContext,
    msg: discord.Message
):
    modal = PollWhoFillingModal(title="PollWho Filling Modal", ctx=ctx)

    await ctx.interaction.response.send_modal(modal)

# react a text with discord reactions via the message menu
@bot.message_command(name="React")
async def react_callback(ctx: discord.ApplicationContext, msg: discord.Message):
    react = React()
    await react.response(ctx, msg)

@bot.message_command(name="React cancel")
async def react_cancel_callback(ctx: discord.ApplicationContext, msg: discord.Message):
    response_content = ""

    # 2 LOOPS TO AVOID INTERACTION ALREADY RESPONDED TO WHEN TOO MANY REACTIONS (ctx.interaction.response.defer() not working here)
    for reaction in msg.reactions: # loop to get the emojis and make the message
        response_content += f"{reaction.emoji} "
    
    await ctx.interaction.response.send_message(content=f"Reaction {response_content} cancelled.", ephemeral=True)
    print(f"{time.strftime('%X')} on day {time.strftime('%x')} : {ctx.user.name} cancelled the reaction {response_content} to the message {msg.id}")
    for reaction in msg.reactions: # loop to remove the reactions
        await reaction.remove(bot.user)


bot.run(TOKEN)