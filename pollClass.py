import time
from collections import defaultdict

import discord
from discord.ui import Button, View

from modalClasses import AddAnswerModal, OPTIONS_TIMEOUT, AnswerSelectMenu

# maximum amount of answers to keep the 'cancel my answer' button visible
MAX_ANSWERS = 18
ENABLED_EMOJI = "✅"
DISABLED_EMOJI = "❌"


# TODO : see if send_options_board and send can be merged
# TODO : improve answer removal
# TODO : add a way to remove the poll (reaction ?)


class Poll:  # base class for a poll

    def __init__(
            self,
            ctx: discord.ApplicationContext,
            question: str,
            answers: list,
            more_answers: bool = True,
            multi_vote: bool = True
    ):
        # discord-related attributes
        self.ctx = ctx
        self.poll_msg = None  # the message containing the poll
        self.owner_id = ctx.interaction.user.id

        # poll basic attributes
        self.question = question
        self.answers = list(filter(None, answers))  # extract non empty answers
        self.choices = defaultdict(
            list)  #  dict of the choices of the users as {user_id : [list of indexes of the answers]}

        # poll options
        self.more_answers = more_answers  # if True, users can add answers
        self.multi_vote = multi_vote  # if True, users can vote for multiple answers

        # poll buttons to choose and add answers
        self.buttons_view = View(timeout=None)
        self.update_buttons_view()

        # view for the poll options
        self.options_view = View(timeout=None)
        self.update_options_view()

        # default line when there's no vote for an answer
        self.default_embed_line = None

        print(
            f"{time.strftime('%X')} on day {time.strftime('%x')} : {ctx.interaction.user.name} created a poll : " + question)

    async def send(self):  # 1st display of question + answers
        message_content = f"_Last update at {time.strftime('%X')} on day {time.strftime('%x')}_"

        embed = discord.Embed(
            title=f"Question : {self.question} (0 vote)\n" + self.get_options_text(),
            fields=[discord.EmbedField(name=f"{self.answers[k]} : 0 vote", value=self.default_embed_line, inline=False)
                    for k in
                    range(len(self.answers))],
            color=discord.Color.random()
        )

        self.poll_msg = await self.ctx.send(embeds=[embed], content=message_content, view=self.buttons_view)

    async def send_options_board(self, interaction):
        await interaction.response.send_message(
            content=f"Options of the poll : {self.question}\n > Multiple vote : {self.multi_vote}\n > Answer addition : {self.more_answers}",
            ephemeral=True,
            delete_after=OPTIONS_TIMEOUT, view=self.options_view)

    async def update_options_board(self, interaction):
        self.update_options_view()
        await interaction.response.edit_message(
            content=f"Options of the poll : {self.question}\n > Multiple vote : {self.multi_vote}\n > Answer addition : {self.more_answers}",
            delete_after=OPTIONS_TIMEOUT, view=self.options_view)

    def create_callback_function(self, idx):
        async def callback(interaction):
            if idx not in self.choices[interaction.user.id]:  # if the user has not voted for this answer yet
                self.choices[interaction.user.id] = self.choices[interaction.user.id] + [idx] if self.multi_vote else [
                    idx]
            print(
                f"{time.strftime('%X')} on day {time.strftime('%x')} : {interaction.user.name} answered {self.answers[idx]} to {self.question}")
            await self.update_display()
            await interaction.response.send_message(f"You voted for {self.answers[idx]}.", ephemeral=True,
                                                    delete_after=2)

        return callback

    async def update_display(self):
        pass

    def create_toggle_button(self, option: bool, option_name, toggle_func):
        if option:
            button = Button(label=f"Disable {option_name}", style=discord.ButtonStyle.red)
        else:
            button = Button(label=f"Enable {option_name}", style=discord.ButtonStyle.green)
        button.callback = toggle_func
        return button

    async def toggle_multi_vote(self, interaction):
        self.multi_vote = not self.multi_vote
        self.update_options_view()
        self.update_buttons_view()
        for choice in self.choices:
            self.choices[choice] = [self.choices[choice][0]]  # keep only the first choice of each user
        await self.update_display()
        await self.update_options_board(interaction)

    async def toggle_more_answers(self, interaction):
        self.more_answers = not self.more_answers
        self.update_options_view()
        self.update_buttons_view()
        await self.update_display()
        await self.update_options_board(interaction)

    async def add_answer_callback(self, interaction):
        if self.more_answers or interaction.user.id == self.owner_id:
            if len(self.answers) >= MAX_ANSWERS:
                await interaction.response.send_message(content=f"No more answers allowed.", ephemeral=True,
                                                        delete_after=5)
            else:
                modal = AddAnswerModal(self)
                await modal.send(interaction)
        else:
            await interaction.response.send_message(
                content=f"Adding answers is disabled, only the owner of the poll can add answers.", ephemeral=True,
                delete_after=5)

    async def remove_answers(self, answer_indexes):
        answer_indexes = list(answer_indexes)
        for answer_idx in answer_indexes:
            print(
                f"{time.strftime('%X')} on day {time.strftime('%x')} : answer {self.answers[answer_idx]} removed from poll {self.question}")
            self.answers.pop(answer_idx)
            for choice in self.choices:
                if answer_idx in self.choices[choice]:
                    self.choices[choice].remove(answer_idx)
                # update the indexes of the answers in the choices
                self.choices[choice] = [idx - 1 if idx > answer_idx else idx for idx in self.choices[choice]]
        self.update_buttons_view()
        await self.update_display()

    async def remove_answer_callback(self, interaction):
        # no need to disable the addition of answers as the added answers will have a higher index than the removed ones
        if len(self.answers) == 1:
            await interaction.response.send_message(content=f"You can't remove the last answer.", ephemeral=True,
                                                    delete_after=5)
        else:
            select_menu = AnswerSelectMenu(self, self.remove_answers)
            remove_answer_view = View(timeout=None)
            remove_answer_view.add_item(select_menu)
            await interaction.response.send_message(
                content=f"Select the answer(s) to remove. You have 10 seconds to choose.", ephemeral=True,
                delete_after=10,
                view=remove_answer_view)

    async def cancel_callback(self, interaction):
        vote_idxs = self.choices[interaction.user.id]
        print(
            f"{time.strftime('%X')} on day {time.strftime('%x')} : {interaction.user.name} cancelled their vote {[self.answers[idx] for idx in vote_idxs]} for poll {self.question}")

        del self.choices[interaction.user.id]
        await self.update_display()
        await interaction.response.send_message(f"You cancelled your vote.", ephemeral=True, delete_after=2)

    def update_buttons_view(self):
        """
        Update the buttons view of the poll without updating the display of the poll
        """
        self.buttons_view.clear_items()

        for i in range(len(self.answers)):
            button = Button(label=f"{chr(ord('@') + i + 1)} : {self.answers[i]}", style=discord.ButtonStyle.blurple)
            button.callback = self.create_callback_function(i)
            self.buttons_view.add_item(button)

        if self.more_answers:
            add_answer_button = Button(label=f"Add an answer", style=discord.ButtonStyle.green, emoji="➕")
            add_answer_button.callback = self.add_answer_callback
            self.buttons_view.add_item(add_answer_button)

        cancel_button = Button(label=f"Cancel my answer" + 's' * self.multi_vote, style=discord.ButtonStyle.red,
                               emoji="🗑️")
        cancel_button.callback = self.cancel_callback
        self.buttons_view.add_item(cancel_button)

    def update_options_view(self):
        """
        Update the options view of the poll
        """
        self.options_view.clear_items()
        self.options_view.add_item(self.create_toggle_button(self.more_answers, "possibility to add answers",
                                                             toggle_func=self.toggle_more_answers))
        self.options_view.add_item(
            self.create_toggle_button(self.multi_vote, "multi-vote", toggle_func=self.toggle_multi_vote))
        add_answer_button = Button(label=f"Add an answer", style=discord.ButtonStyle.green, emoji="➕")
        add_answer_button.callback = self.add_answer_callback
        self.options_view.add_item(add_answer_button)
        remove_answer_button = Button(label=f"Remove an answer", style=discord.ButtonStyle.red, emoji="➖")
        remove_answer_button.callback = self.remove_answer_callback
        self.options_view.add_item(remove_answer_button)

    def bool_to_emoji(self, boolean):
        return "✅" if boolean else "❌"

    def get_options_text(self):
        return f"\n> Multiple vote : {self.bool_to_emoji(self.multi_vote)}\n > Answer addition : {self.bool_to_emoji(self.more_answers)}\n\n"


class PollPercentages(Poll):

    def __init__(self, ctx, question, answers, more_answers=True, multi_vote=True):
        super().__init__(ctx, question, answers, more_answers, multi_vote)
        self.default_embed_line = "**|** 0 %"

    async def update_display(self):
        votes = [0 for _ in range(len(self.answers))]
        tot = 0

        for user_id in self.choices:
            for choice in self.choices[user_id]:
                votes[choice] += 1
                tot += 1

        percentages = [0 for _ in range(len(votes))]
        if tot != 0:
            percentages = [votes[k] / tot for k in range(len(votes))]  # from 0 to 100 with no decimals

        nb_bar = 35  # the total amount of / to be distributed among the percentages

        embed = discord.Embed(
            title=f"Question : {self.question} ({str(tot)} vote" + (tot > 1) * "s" + ")\n" + self.get_options_text(),
            fields=[discord.EmbedField(name=f"{self.answers[k]} : {str(votes[k])} vote" + (votes[k] > 1) * "s",
                                       value="**|**" + "/" * int(percentages[k] * nb_bar) + (int(
                                           percentages[k] * nb_bar) > 0) * "**/**" + f" {int(percentages[k] * 100)} %",
                                       inline=False) for k in range(len(votes))],
            color=discord.Color.random(),
        )

        # add last update in italic to content
        message_content = f"\n_Last update at {time.strftime('%X')} on day {time.strftime('%x')}_"
        await self.poll_msg.edit(content=message_content, embeds=[embed], view=self.buttons_view)


class PollNames(Poll):
    def __init__(self, ctx, question, answers, more_answers=True, multi_vote=True):
        super().__init__(ctx, question, answers, more_answers, multi_vote)
        self.default_embed_line = "> "

    async def update_display(self):
        tot = 0
        votes = [[] for _ in range(len(self.answers))]

        # EXTRACT NAMES FROM THE PERSONS WHO VOTED A CERTAIN BUTTON
        for user_id in self.choices:
            member = await self.ctx.guild.fetch_member(int(user_id))
            name = member.nick or member.name
            for choice in self.choices[user_id]:
                votes[choice].append(name)
                tot += 1

        embed = discord.Embed(
            title=f"Question : {self.question} ({str(tot)} vote" + (
                    len(votes) > 1) * "s" + ")\n" + self.get_options_text(),
            fields=[
                discord.EmbedField(name=f"{self.answers[k]} : {str(len(votes[k]))} vote" + (len(votes[k]) > 1) * "s",
                                   value=f"> {', '.join(votes[k])}", inline=False) for k in range(len(votes))],
            color=discord.Color.random(),
        )

        # add last update in italic to content
        message_content = f"\n_Last update at {time.strftime('%X')} on day {time.strftime('%x')}_"
        await self.poll_msg.edit(content=message_content, embeds=[embed], view=self.buttons_view)
