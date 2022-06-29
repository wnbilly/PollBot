from email import message
from pollBot_display import percentage_display

import time
import random

import discord
from discord.ext import commands
from discord import option, InteractionMessage
from discord.ui import Button, View

class Poll():

    def __init__(
        self,
        ctx: discord.ApplicationContext,
        question: str,
        answers: list,
        display: int,
        ):

        self.ctx = ctx
        self.question = question
        self.answers = list(filter(None, answers)) # extract non empty answers
        self.display = display

        self.choices = {} # dict of the choices of the users

        self.buttons_view = View()

        for i in range(len(self.answers)):
            button = Button(label=f"{chr(ord('@')+i+1)} : {self.answers[i]}", style=discord.ButtonStyle.blurple)
            button.callback = self.create_callbackfunction(i)
            self.buttons_view.add_item(button)

        self.display_view = View()

        button_refresh_display = Button(label="Refresh Display", style=discord.ButtonStyle.red)
        button_refresh_display.callback = self.refresh_display

        self.display_view.add_item(button_refresh_display)

    async def refresh_display(self, interaction):
        print(f"{interaction.user.name} refreshed poll : "+ self.question)

        votes = [0 for _ in range(len(self.answers))]
        tot = 0

        for user_id in self.choices:
            votes[self.choices[user_id]] += 1
            tot += 1

        percentages = [0 for k in range(len(votes))]
        if tot != 0:
            percentages = [votes[k]/tot for k in range(len(votes))] # from 0 to 1

        percentage_display(percentages)
        await interaction.message.delete()
        await self.ctx.send(file=discord.File('barChart.png'), content=f"Last update at {str(time.strftime('%X'))} on day {str(time.strftime('%x'))}", view=self.display_view)


    def create_callbackfunction(self, idx):
        async def callback(interaction):
            self.choices[interaction.user.id] = idx
            print(f"{interaction.user.name} voted {self.answers[idx]}")
            await interaction.response.send_message(f"You voted {self.answers[idx]}", ephemeral=True)

        return callback

    async def send_poll(self, interaction):
        await interaction.response.send_message("Question : " + self.question, view=self.buttons_view)

        # image update + 1st display
        percentages = [0 for k in range(len(self.answers))]
        percentage_display(percentages)
        await self.ctx.send(content=f"Last update at {str(time.strftime('%X'))} on day {str(time.strftime('%x'))}", file=discord.File('barChart.png'), view=self.display_view)

        await self.display_view.wait()

class Pollb(): # poll that refreshes at every vote

    def __init__(
        self,
        ctx: discord.ApplicationContext,
        question: str,
        answers: list,
        display: int,
        ):

        self.ctx = ctx
        self.question = question
        self.answers = list(filter(None, answers)) # extract non empty answers
        self.display = display

        self.choices = {} # dict of the choices of the users

        self.buttons_view = View()

        for i in range(len(self.answers)):
            button = Button(label=f"{chr(ord('@')+i+1)} : {self.answers[i]}", style=discord.ButtonStyle.blurple)
            button.callback = self.create_callbackfunction(i)
            self.buttons_view.add_item(button)

        self.display_view = View()

        button_refresh_display = Button(label="Refresh Display", style=discord.ButtonStyle.red)
        button_refresh_display.callback = self.refresh_display

        self.display_view.add_item(button_refresh_display)

    async def refresh_display(self, interaction):
        print(f"{interaction.user.name} a refresh")

        votes = [0 for _ in range(len(self.answers))]
        tot = 0

        for user_id in self.choices:
            votes[self.choices[user_id]] += 1
            tot += 1

        percentages = [0 for k in range(len(votes))]
        if tot != 0:
            percentages = [votes[k]/tot for k in range(len(votes))] # from 0 to 1

        percentage_display(percentages)
        await interaction.message.delete()
        await self.ctx.send(file=discord.File('barChart.png'), content=f"Last update at {str(time.strftime('%X'))} on day {str(time.strftime('%x'))}")


    def create_callbackfunction(self, idx):
        async def callback(interaction):
            self.choices[interaction.user.id] = idx
            print(f"{interaction.user.name} voted {self.answers[idx]}")
            await self.refresh_display(interaction)
            await interaction.response.send_message(f"You voted {self.answers[idx]}", ephemeral=True)

        return callback

    async def send_poll(self, interaction):
        await interaction.response.send_message("Question : " + self.question, view=self.buttons_view)

        # image update + 1st display
        percentages = [0 for k in range(len(self.answers))]
        percentage_display(percentages)
        await self.ctx.send(content=f"Last update at {str(time.strftime('%X'))} on day {str(time.strftime('%x'))}", file=discord.File('barChart.png'))

        await self.display_view.wait()

def extract_equal(list, value):
    for i in 

class PollWho():    # poll to know who

    def __init__(
        self,
        ctx: discord.ApplicationContext,
        answers: list,
        question: str,
        display: int
        ):

        self.ctx = ctx
        self.question = question
        self.answers = list(filter(None, answers)) # extract non empty answers
        self.display = display

        self.choices = {} # dict of the choices of the users

        self.buttons_view = View()

        for i in range(len(self.answers)):
            button = Button(label=f"{chr(ord('@')+i+1)} : {self.answers[i]}", style=discord.ButtonStyle.blurple)
            button.callback = self.create_callbackfunction(i)
            self.buttons_view.add_item(button)


    async def refresh_display(self, interaction):
        print(f"{interaction.user.name} refreshed poll_who : "+ self.question)

        message_content = self.question + " : \n"

        for idx in range(len(self.answers)):
            names_list = list(filter(, choices))

        votes = [0 for _ in range(len(self.answers))]
        tot = 0

        for user_name in self.choices:
            votes[self.choices[user_name]] += 1
            tot += 1
# to continue
        if tot != 0:
            percentages = [votes[k]/tot for k in range(len(votes))] # from 0 to 1

        await interaction.message.delete()
        await self.ctx.send(file=discord.File('barChart.png'), content=f"Last update at {str(time.strftime('%X'))} on day {str(time.strftime('%x'))}", view=self.display_view)


    def create_callbackfunction(self, idx):
        async def callback(interaction):
            self.choices[interaction.user.name] = idx
            print(f"{interaction.user.name} voted {self.answers[idx]}")
            await interaction.response.send_message(f"You voted {self.answers[idx]}", ephemeral=True)
            await self.refresh_display(interaction)

        return callback

    async def send_poll(self, interaction): # 1st display of question + answers
        last_update = f"Last update at {time.strftime('%X')} on day {time.strftime('%x')}"
        message_content = f"Question : " + self.question + "\n\n"
        
        await interaction.response.send_message(content=message_content+last_update, view=self.buttons_view)

        await self.display_view.wait()