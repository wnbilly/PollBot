from pollBot_display import percentage_display

import time
import random

import discord
from discord.ext import commands
from discord import option, InteractionMessage, Guild, Member
from discord.ui import Button, View


class Poll():   # poll to display percentages only, no names

    def __init__(
        self,
        ctx: discord.ApplicationContext,
        question: str,
        answers: list,
        ):

        self.ctx = ctx
        self.question = question
        self.answers = list(filter(None, answers)) # extract non empty answers

        self.choices = {} # dict of the choices of the users

        self.buttons_view = View()

        for i in range(len(self.answers)):
            button = Button(label=f"{chr(ord('@')+i+1)} : {self.answers[i]}", style=discord.ButtonStyle.blurple)
            button.callback = self.create_callbackfunction(i)
            self.buttons_view.add_item(button)

        cancel_button = Button(label=f"{chr(ord('@')+len(self.answers)+1)} : Cancel", style=discord.ButtonStyle.red)
        cancel_button.callback = self.cancel_callback
        self.buttons_view.add_item(cancel_button)
        self.buttons_view.timeout = None

        self.display_view = View()

        button_refresh_display = Button(label="Refresh Display", style=discord.ButtonStyle.red)
        button_refresh_display.callback = self.refresh_display

        self.display_view.add_item(button_refresh_display)
        self.display_view.timeout = None

    async def refresh_display(self, interaction):
        print(f"{time.strftime('%X')} on day {time.strftime('%x')} : {interaction.user.name} refrshed display of poll {self.question}")
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

        message_content = f"_Last update at {time.strftime('%X')} on day {time.strftime('%x')}_\n"
        message_content += self.question + f" :\n"

        for i in range(len(self.answers)):
            message_content += f"{chr(ord('@')+i+1)} : {self.answers[i]}\n"

        await self.ctx.send(file=discord.File('barChart.png'), content=message_content, view=self.display_view)


    def create_callbackfunction(self, idx):
        async def callback(interaction):
            self.choices[interaction.user.id] = idx
            print(f"{time.strftime('%X')} on day {time.strftime('%x')} : {interaction.user.name} answered {self.answers[idx]} to {self.question}")
            await interaction.response.send_message(f"You voted {self.answers[idx]}", ephemeral=True)

        return callback

    async def cancel_callback(self, interaction):
        vote_idx = self.choices[interaction.user.id]
        print(f"{time.strftime('%X')} on day {time.strftime('%x')} : {interaction.user.name} cancelled their vote {self.answers[vote_idx]} for poll {self.question}")

        del self.choices[interaction.user.id]
        await interaction.response.send_message(f"You cancelled your vote for {self.answers[vote_idx]}", ephemeral=True)


    async def send_poll(self, *args, **kwargs):
        await self.ctx.send("Question : " + self.question, view=self.buttons_view)

        # image update + 1st display
        percentages = [0 for k in range(len(self.answers))]
        percentage_display(percentages)

        message_content = f"_Last update at {time.strftime('%X')} on day {time.strftime('%x')}_\n"
        message_content += self.question + f" :\n"

        for i in range(len(self.answers)):
            message_content += f"{chr(ord('@')+i+1)} : {self.answers[i]}\n"

        await self.ctx.send(content=message_content, file=discord.File('barChart.png'), view=self.display_view)

        await self.display_view.wait()


def better_str(list):
    better_string = ""
    length = len(list)
    if length>0:
        for k in range(length-1):
            better_string += str(list[k]) + ", "
        better_string += str(list[length-1])
    return better_string

class PollWho():    # poll to know who and no percentages display

    def __init__(
        self,
        ctx: discord.ApplicationContext,
        question: str,
        answers: list,
        ):

        self.ctx = ctx
        self.question = question
        self.answers = list(filter(None, answers)) # extract non empty answers

        self.choices = {} # dict of the choices of the users

        self.buttons_view = View()

        for i in range(len(self.answers)):
            button = Button(label=f"{chr(ord('@')+i+1)} : {self.answers[i]}", style=discord.ButtonStyle.blurple)
            button.callback = self.create_callbackfunction(i)
            self.buttons_view.add_item(button)

        cancel_button = Button(label=f"{chr(ord('@')+len(self.answers)+1)} : Cancel", style=discord.ButtonStyle.red)
        cancel_button.callback = self.cancel_callback
        self.buttons_view.add_item(cancel_button)
        self.buttons_view.timeout = None

    async def refresh_display(self, interaction):
        # print(f"{time.strftime('%X')} on day {time.strftime('%x')} : {interaction.user.name} refreshed poll_who : "+ self.question)

        message_content = str(self.question) + f" : \n"        
        
        separator = "--------------"
        message_content += separator

        tot = 0
        votes = [[] for _ in range(len(self.answers))]

        # EXTRACT NAMES FROM THE PERSONS WHO VOTED A CERTAIN BUTTON
        for user_id in self.choices:
            member = await self.ctx.guild.fetch_member(int(user_id))
            name = member.nick or member.name
            votes[self.choices[user_id]].append(name)
            tot += 1

        # add the names by choice
        for k in range(len(votes)):
            message_content += "\n" + self.answers[k] + " : " + str(len(votes[k])) + " votes\n"
            message_content += better_str(votes[k]) + "\n"
            message_content += separator


        # add last update in italic to content
        message_content += f"\n_Last update at {time.strftime('%X')} on day {time.strftime('%x')}_"
        await interaction.message.edit(content=message_content)


    def create_callbackfunction(self, idx):
        async def callback(interaction):
            self.choices[interaction.user.id] = idx
            print(f"{time.strftime('%X')} on day {time.strftime('%x')} : {interaction.user.name} answered {self.answers[idx]} to {self.question}")
            # await interaction.response.send_message(f"You voted {self.answers[idx]}", ephemeral=True)
            await interaction.response.defer()
            await self.refresh_display(interaction)

        return callback

    async def cancel_callback(self, interaction):
        vote_idx = self.choices[interaction.user.id]
        print(f"{time.strftime('%X')} on day {time.strftime('%x')} : {interaction.user.name} cancelled their vote {self.answers[vote_idx]} for poll {self.question}")

        del self.choices[interaction.user.id]
        await interaction.response.defer() # to avoid "This interaction failed." error
        await self.refresh_display(interaction)


    async def send_poll(self): # 1st display of question + answers
        last_update = f"_Last update at {time.strftime('%X')} on day {time.strftime('%x')}_"
        message_content = "Question : " + str(self.question) + f"\n0 votes\n"
        
        await self.ctx.send(content=message_content+last_update, view=self.buttons_view)

        await self.buttons_view.wait()

class PollFillingModal(discord.ui.Modal):
    def __init__(self, ctx:discord.ApplicationContext, *args, **kwargs) -> None:
        super().__init__(
            discord.ui.InputText(
                label="Question",
                placeholder="Enter your question",
                style=discord.InputTextStyle.long
            ),
            discord.ui.InputText(
                label="Answer 1",
                style=discord.InputTextStyle.long
            ),
            discord.ui.InputText(
                label="Answer 2",
                style=discord.InputTextStyle.long
            ),
            discord.ui.InputText(
                label="Answer 3",
                style=discord.InputTextStyle.long,
                required=False
            ),
            discord.ui.InputText(
                label="Answer 4",
                style=discord.InputTextStyle.long,
                required=False
            ),
            *args,
            **kwargs,)
        self.ctx = ctx
        self.question = ""
        self.answers = []

    async def callback(self, interaction: discord.Interaction):
        self.question = self.children[0].value
        self.answers = [self.children[i].value for i in range(1,5)] # only 4 answers possible at the moment

        poll = Poll(self.ctx, self.question, self.answers)
        print(f"{self.ctx.interaction.user.name} created a poll via menu : " + self.question)

        await poll.send_poll()
        await poll.display_view.wait()

class PollWhoFillingModal(discord.ui.Modal):
    def __init__(self, ctx:discord.ApplicationContext, *args, **kwargs) -> None:
        super().__init__(
            discord.ui.InputText(
                label="Question",
                placeholder="Enter your question",
                style=discord.InputTextStyle.long
            ),
            discord.ui.InputText(
                label="Answer 1",
                style=discord.InputTextStyle.long
            ),
            discord.ui.InputText(
                label="Answer 2",
                style=discord.InputTextStyle.long
            ),
            discord.ui.InputText(
                label="Answer 3",
                style=discord.InputTextStyle.long,
                required=False
            ),
            discord.ui.InputText(
                label="Answer 4",
                style=discord.InputTextStyle.long,
                required=False
            ),
            *args,
            **kwargs,)
        self.ctx = ctx
        self.question = ""
        self.answers = []

    async def callback(self, interaction: discord.Interaction):
        self.question = self.children[0].value
        self.answers = [self.children[i].value for i in range(1,5)] # only 4 answers possible at the moment

        poll_who = PollWho(self.ctx, self.question, self.answers)
        print(f"{self.ctx.interaction.user.name} created a poll via menu : " + self.question)

        await poll_who.send_poll()
        await poll_who.display_view.wait()