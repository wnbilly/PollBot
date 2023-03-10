import time
import random
# import json

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

        cancel_button = Button(label=f"Cancel", style=discord.ButtonStyle.red)
        cancel_button.callback = self.cancel_callback
        self.buttons_view.add_item(cancel_button)
        self.buttons_view.timeout = None

        self.display_view = View()

        button_refresh_display = Button(label="Refresh Display", style=discord.ButtonStyle.red)
        button_refresh_display.callback = self.refresh_display

        self.display_view.add_item(button_refresh_display)
        self.display_view.timeout = None

        print(f"{time.strftime('%X')} on day {time.strftime('%x')} : {ctx.interaction.user.name} created a poll : " + question)

    async def refresh_display(self, interaction):
        print(f"{time.strftime('%X')} on day {time.strftime('%x')} : {interaction.user.name} refreshed poll : "+ self.question)

        votes = [0 for _ in range(len(self.answers))]
        tot = 0

        for user_id in self.choices:
            votes[self.choices[user_id]] += 1
            tot += 1

        percentages = [0 for k in range(len(votes))]
        if tot != 0:
            percentages = [votes[k]/tot for k in range(len(votes))] # from 0 to 100 with no decimals

        nb_bar = 35 # the total amount of / to be distributed among the percentages

        embed = discord.Embed(
            title=f"Question : {self.question} ({str(tot)} vote"+(tot>1)*"s"+")",
            fields=[discord.EmbedField(name=f"{self.answers[k]} : {str(votes[k])} vote"+(votes[k]>1)*"s", value="**|**"+"/"*int(percentages[k]*nb_bar)+(int(percentages[k]*nb_bar)>0)*"**/**"+f" {int(percentages[k]*100)} %", inline=False) for k in range(len(votes))],
            color=discord.Color.random(),
            )

        # add last update in italic to content
        message_content = f"\n_Last update at {time.strftime('%X')} on day {time.strftime('%x')}_"
        # await interaction.message.edit(content=message_content)
        await interaction.message.edit(content=message_content, embeds=[embed], view=self.buttons_view)

    def create_callbackfunction(self, idx):
        async def callback(interaction):
            self.choices[interaction.user.id] = idx
            print(f"{time.strftime('%X')} on day {time.strftime('%x')} : {interaction.user.name} answered {self.answers[idx]} to {self.question}")
            await self.refresh_display(interaction)
            await interaction.response.send_message(f"You voted {self.answers[idx]}", ephemeral=True, delete_after=2)

        return callback

    async def cancel_callback(self, interaction):
        vote_idx = self.choices[interaction.user.id]
        print(f"{time.strftime('%X')} on day {time.strftime('%x')} : {interaction.user.name} cancelled their vote {self.answers[vote_idx]} for poll {self.question}")

        del self.choices[interaction.user.id]
        await interaction.response.send_message(f"You cancelled your vote for {self.answers[vote_idx]}", ephemeral=True)

    async def send_poll(self): # 1st display of question + answers
        message_content = f"_Last update at {time.strftime('%X')} on day {time.strftime('%x')}_"

        percentages = [0 for k in range(len(self.answers))]

        embed = discord.Embed(
            title=f"Question : {self.question} (0 vote)",
            fields=[discord.EmbedField(name=f"{self.answers[k]} :", value=f"**|** 0 %", inline=False) for k in range(len(self.answers))],
            color=discord.Color.random()
            )

        await self.ctx.send(embeds=[embed], content=message_content, view=self.buttons_view)

        await self.buttons_view.wait()


def better_str(list):
    better_string = "> "
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

        add_answer_button = Button(label=f"Add an answer", style=discord.ButtonStyle.green)
        add_answer_button.callback = self.add_answer_callback
        self.buttons_view.add_item(add_answer_button)

        cancel_button = Button(label=f"Cancel my answer", style=discord.ButtonStyle.red)
        cancel_button.callback = self.cancel_callback
        self.buttons_view.add_item(cancel_button)
        self.buttons_view.timeout = None

        print(f"{time.strftime('%X')} on day {time.strftime('%x')} : {ctx.interaction.user.name} created a pollWho : " + question)

    async def refresh_display(self, interaction):
        tot = 0
        votes = [[] for _ in range(len(self.answers))]

        # EXTRACT NAMES FROM THE PERSONS WHO VOTED A CERTAIN BUTTON
        for user_id in self.choices:
            member = await self.ctx.guild.fetch_member(int(user_id))
            name = member.nick or member.name
            votes[self.choices[user_id]].append(name)
            tot += 1

        embed = discord.Embed(
            title=f"Question : {self.question} ({str(tot)} vote"+(len(votes)>1)*"s"+")",
            fields=[discord.EmbedField(name=f"{self.answers[k]} : {str(len(votes[k]))} vote"+(len(votes[k])>1)*"s", value=f"{better_str(votes[k])}", inline=False) for k in range(len(votes))],
            color=discord.Color.random(),
            )

        # add last update in italic to content
        message_content = f"\n_Last update at {time.strftime('%X')} on day {time.strftime('%x')}_"

        await interaction.message.edit(content=message_content, embeds=[embed], view=self.buttons_view)

    def create_callbackfunction(self, idx):
        async def callback(interaction):
            self.choices[interaction.user.id] = idx
            print(f"{time.strftime('%X')} on day {time.strftime('%x')} : {interaction.user.name} answered {self.answers[idx]} to {self.question}")
            # await interaction.response.defer()
            await self.refresh_display(interaction)
            await interaction.response.send_message(f"You voted {self.answers[idx]}", ephemeral=True, delete_after=2)
        return callback

    async def add_answer_callback(self, interaction):
        
        if (len(self.answers)>=23):
            await interaction.response.send_message(content=f"No more answers allowed.", ephemeral=True, delete_after=5)
        else :
            modal = discord.ui.Modal(title=f'Modal for answer entry')
            input = discord.ui.InputText(
                label="Write the answer to add to the poll",
                placeholder="Type your new answer...",
                style=discord.InputTextStyle.short
            )
            modal.add_item(input)
            # await ctx.send_modal(modal)
            await interaction.response.send_modal(modal)
            await modal.wait()
            new_answer = input.value
            self.answers.append(new_answer)

            # remove add_answer_button and cancel_button
            cancel_button = self.buttons_view.children[-1]
            self.buttons_view.remove_item(self.buttons_view.children[-1])
            add_answer_button = self.buttons_view.children[-1]
            self.buttons_view.remove_item(self.buttons_view.children[-1])

            # add new button to the view
            button = Button(label=f"{chr(ord('@')+len(self.answers))} : {self.answers[-1]}", style=discord.ButtonStyle.blurple)
            button.callback = self.create_callbackfunction(len(self.answers)-1)
            self.buttons_view.add_item(button)

            # add add_answer_button and cancel_button
            self.buttons_view.add_item(add_answer_button)
            self.buttons_view.add_item(cancel_button)

            print(f"{time.strftime('%X')} on day {time.strftime('%x')} : {interaction.user.name} added the answer {self.answers[-1]} to {self.question}")
            await self.refresh_display(interaction)

    async def cancel_callback(self, interaction):
        vote_idx = self.choices[interaction.user.id]
        print(f"{time.strftime('%X')} on day {time.strftime('%x')} : {interaction.user.name} cancelled their vote {self.answers[vote_idx]} for poll {self.question}")

        del self.choices[interaction.user.id]
        await interaction.response.defer() # to avoid "This interaction failed." error
        await self.refresh_display(interaction)


    async def send_poll(self): # 1st display of question + answers
        message_content = f"_Last update at {time.strftime('%X')} on day {time.strftime('%x')}_"
        
        embed = discord.Embed(
            title=f"Question : {self.question} (0 vote)",
            fields=[discord.EmbedField(name=f"{self.answers[k]} : 0 vote", value=f"> ", inline=False) for k in range(len(self.answers))],
            color=discord.Color.random()
            )

        await self.ctx.send(embeds=[embed], content=message_content, view=self.buttons_view)

        await self.buttons_view.wait()

    # TODO
    """def save_to_json(self, path=None):
        save_file = open("poll_who.json","w+")
        json_string = json.dump(self, save_file)
        save_file.close()"""


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
        print(f"{time.strftime('%X')} on day {time.strftime('%x')} : {self.ctx.interaction.user.name} created a poll via menu : " + self.question)

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
                style=discord.InputTextStyle.long,
                required=False
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
        print(f"{time.strftime('%X')} on day {time.strftime('%x')} : {self.ctx.interaction.user.name} created a poll via menu : " + self.question)

        await poll_who.send_poll()
        await poll_who.display_view.wait()

    async def on_error(self, interaction: discord.Interaction, error: Exception) -> None:
        await interaction.response.send_message('Oops! Something went wrong.', ephemeral=True)
