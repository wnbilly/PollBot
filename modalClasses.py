import time

import discord

OPTIONS_TIMEOUT = 1200  # in secondes, equals to 20 minutes


class PollFillingModal(discord.ui.Modal):
    def __init__(self, ctx: discord.ApplicationContext, poll_class, *args, **kwargs):
        super().__init__(
            discord.ui.InputText(
                label="Question",
                placeholder="Enter your question",
                style=discord.InputTextStyle.long
            ),
            discord.ui.InputText(
                label="Answer 1",
                style=discord.InputTextStyle.short
            ),
            discord.ui.InputText(
                label="Answer 2",
                style=discord.InputTextStyle.short,
                required=False
            ),
            discord.ui.InputText(
                label="Answer 3",
                style=discord.InputTextStyle.short,
                required=False
            ),
            discord.ui.InputText(
                label="Answer 4",
                style=discord.InputTextStyle.short,
                required=False
            ),
            title="Poll creation modal",
            *args,
            **kwargs, )
        self.ctx = ctx
        self.question = ""
        self.answers = []
        self.poll_class = poll_class

    async def send(self):
        await self.ctx.interaction.response.send_modal(self)

    async def callback(self, interaction: discord.Interaction):
        self.question = self.children[0].value
        self.answers = [self.children[i].value for i in range(1, 5)]  # only 4 answers possible in the beginning but more can be added via buttons

        poll = self.poll_class(self.ctx, self.question, self.answers)

        await poll.send()
        await poll.send_options_board(interaction)

    async def on_error(self, interaction: discord.Interaction, error: Exception):
        await interaction.response.send_message("Oops! Something went wrong.", ephemeral=True, delete_after=2)


class AddAnswerModal(discord.ui.Modal):
    def __init__(self, poll, *args, **kwargs):
        super().__init__(
            discord.ui.InputText(
                label="Write the answer to add to the poll",
                placeholder="Type your new answer...",
                style=discord.InputTextStyle.short
            ),
            title="Modal for answer entry",
            *args, **kwargs)
        self.poll = poll

    async def send(self, interaction: discord.Interaction):
        await interaction.response.send_modal(self)

    async def callback(self, interaction: discord.Interaction):
        self.poll.answers.append(self.children[0].value)
        self.poll.update_buttons_view()
        await interaction.response.send_message(
            content=f"You added the answer {self.poll.answers[-1]} to the poll {self.poll.question}", ephemeral=True,
            delete_after=2)
        await self.poll.update_display()
        print(
            f"{time.strftime('%X')} on day {time.strftime('%x')} : {interaction.user.name} added the answer {self.poll.answers[-1]} to {self.poll.question}")

    async def on_error(self, interaction: discord.Interaction, error: Exception):
        await interaction.response.send_message("Oops! Something went wrong.", ephemeral=True, delete_after=2)


class AnswerSelectMenu(discord.ui.Select):
    def __init__(self, poll, method_to_call, *args, **kwargs):
        super().__init__(custom_id="Select the answer to remove", placeholder="Poll answers",
                         max_values=len(poll.answers) - 1, *args, **kwargs)
        self.poll = poll
        self.method_to_call = method_to_call
        for answer_idx in range(len(self.poll.answers)):
            self.add_option(label=f"{chr(ord('@') + answer_idx + 1)} : {self.poll.answers[answer_idx]}",
                            value=str(answer_idx))

    async def callback(self, interaction: discord.Interaction):
        answer_indexes = [int(value) for value in self.values]
        await interaction.response.send_message(
            content=f"You removed the answer(s) {', '.join([self.poll.answers[idx] for idx in answer_indexes])} from the poll {self.poll.question}",
            ephemeral=True,
            delete_after=2)
        await self.method_to_call(answer_indexes)
        self.disabled = True
        # TODO : find a way to delete the message containing the select menu
        await interaction.message.delete(delay=1) # not working
