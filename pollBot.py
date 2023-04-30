import sys

import discord
from discord import option, SlashCommandOptionType

from pollClass import Poll, PollWho, PollFillingModal
from reactClass import ReactModal, reactions_cancel

try:
    TOKEN = sys.argv[1]
except IndexError:
    print("Bot token required as following : $ python3 pollBot.py TOKEN")
    quit(0)

try:
    bot = discord.Bot(auto_sync_commands=True)

    @bot.event
    async def on_ready():
        print(f"{bot.user} ready.")


    # initial poll command
    # poll command, callable via /poll "question" "answer1" "answer2" ... "more_answers"
    @bot.slash_command(name="poll", description="Create a percentages poll")
    @option("question", description="Enter the question to ask")
    @option("answer1", description="Enter 1st answer")
    @option("answer2", description="Enter 2nd answer", required=False)
    @option("answer3", description="Enter 3rd answer", required=False)
    @option("answer4", description="Enter 4th answer", required=False)
    @option("answer5", description="Enter 5th answer", required=False)
    @option("answer6", description="Enter 6th answer", required=False)
    @option("answer7", description="Enter 7th answer", required=False)
    @option("answer8", description="Enter 8th answer", required=False)
    @option(name="more_answers", description="Choose if others can add answers to the poll (0 or 1)",
            type=SlashCommandOptionType.integer, min_value=0, max_value=1, default=True)
    async def poll(ctx: discord.ApplicationContext, question: str, answer1: str, answer2: str, answer3: str,
                   answer4: str, answer5: str, answer6: str,
                   answer7: str, answer8: str, more_answers):
        answers = [answer1, answer2, answer3, answer4, answer5, answer6, answer7, answer8]
        poll = Poll(ctx, question, answers, more_answers)
        await ctx.interaction.response.send_message(content=f"You sent the poll : {question}", ephemeral=True,
                                                    delete_after=2)
        await poll.send_poll()


    # poll command, callable via /poll_who "question" "answer1" "answer2" ... "more_answers"
    @bot.slash_command(name="poll_who", description="Create a names poll")
    @option("question", description="Enter the question to ask")
    @option("answer1", description="Enter 1st answer")
    @option("answer2", description="Enter 2nd answer", required=False)
    @option("answer3", description="Enter 3rd answer", required=False)
    @option("answer4", description="Enter 4th answer", required=False)
    @option("answer5", description="Enter 5th answer", required=False)
    @option("answer6", description="Enter 6th answer", required=False)
    @option("answer7", description="Enter 7th answer", required=False)
    @option("answer8", description="Enter 8th answer", required=False)
    @option(name="more_answers", description="Choose if others can add answers to the poll (0 or 1)",
            type=SlashCommandOptionType.integer, min_value=0, max_value=1, default=True)
    async def poll_who(ctx: discord.ApplicationContext, question: str, answer1: str, answer2: str, answer3: str,
                       answer4: str, answer5: str, answer6: str,
                       answer7: str, answer8: str, more_answers):
        answers = [answer1, answer2, answer3, answer4, answer5, answer6, answer7, answer8]
        poll_who = PollWho(ctx, question, answers, more_answers)

        await ctx.interaction.response.send_message(content=f"You sent the poll : {question}", ephemeral=True,
                                                    delete_after=2)
        await poll_who.send_poll()


    # same poll command as before
    # poll message command, callable via message context menus
    @bot.message_command(name="Create a poll", description="Create a poll with a percentage bars display via a modal")
    async def poll_app_command(ctx: discord.ApplicationContext, msg: discord.Message):
        modal = PollFillingModal(title="Poll Filling Modal", ctx=ctx, poll_class=Poll)

        await ctx.interaction.response.send_modal(modal)


    # poll_who message command, callable via message context menus
    @bot.message_command(name="Create a pollWho", description="Create a poll with a names display via a modal")
    async def poll_who_app_command(ctx: discord.ApplicationContext, msg: discord.Message):
        modal = PollFillingModal(title="PollWho Filling Modal", ctx=ctx, poll_class=PollWho)
        await ctx.interaction.response.send_modal(modal)


    # reacts a text with discord reactions via the message menu
    @bot.message_command(name="React")
    async def react_callback(ctx: discord.ApplicationContext, msg: discord.Message):
        modal = ReactModal(ctx, msg)
        await ctx.interaction.response.send_modal(modal)
        # await modal.wait()


    # cancels the reactions of the bot to a message
    @bot.message_command(name="React cancel")
    async def react_cancel_callback(ctx: discord.ApplicationContext, msg: discord.Message):
        await reactions_cancel(ctx, msg, bot)


    bot.run(TOKEN)

except KeyboardInterrupt:
    print("\nPollBot shutting down...")

except discord.errors.LoginFailure:
    print("Invalid token, please check your token and try again.")
