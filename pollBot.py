# https://github.com/Pycord-Development/pycord/blob/master/examples/views/confirm.py
# https://github.com/Pycord-Development/pycord/blob/master/examples/app_commands/slash_basic.py


import time
import random

import discord
from discord.ext import commands
from discord import option, InteractionMessage
from discord.ui import Button, View

from pollBot_display import percentage_display

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

    async def answer_button_callback(interaction):
        await interaction.response.send_message("Button ")
        nb_answer1 += 1

    async def answer2_button_callback(interaction):
        await interaction.response.send_message("Button ")
        await print("2")

    async def refresh_display(interaction):
        percentages = [random.randint(0,100)/100, random.randint(0,100)/100, random.randint(0,100)/100] # from 0 to 1
        percentage_display(percentages)
        message = interaction.original_message()
        message.delete()
        await ctx.send(file=discord.File('barChart.png'), content=f"Last update at {str(time.strftime('%X'))} on day {str(time.strftime('%x'))}")

    # refresh button
    button_refresh_display = Button(label="Refresh Display", style=discord.ButtonStyle.red)
    button_refresh_display.callback = refresh_display

    display_view = View()
    display_view.add_item(button_refresh_display)

    # create and display the choice buttons
    button1 = Button(label="A : " + answer1, style=discord.ButtonStyle.blurple)
    button1.callback = answer_button_callback

    button2 = Button(label="B : " + answer2, style=discord.ButtonStyle.blurple)
    button1.callback = answer2_button_callback

    buttons_view = View()
    buttons_view.add_item(button1)
    buttons_view.add_item(button2)
    
    await ctx.send("Question : " + question, view=buttons_view)

    # image update + 1st display
    percentages = [random.randint(0,100)/100, random.randint(0,100)/100, random.randint(0,100)/100] # from 0 to 1
    percentage_display(percentages)
    await ctx.send("Last update at " +str(time.strftime('%X'))+ " on date " + str(time.strftime('%x')), file=discord.File('barChart.png'), view=display_view)

bot.run(TOKEN)