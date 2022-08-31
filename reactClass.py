import time

import discord
from discord.ext import commands
from discord import option, InteractionMessage, Guild, Member
from discord.ui import Button, View, InputText


class React():

    def _init_(
        self,
        ctx : discord.ApplicationContext,
        letter_emojis_dict : dict
    ):
        self.ctx = ctx


    def str_to_emojis(self, str):
        letter_emojis_dict={
            'a':'🇦', 
            'b':'🇧', 
            'c':'🇨', 
            'd':'🇩',
            'e':'🇪',
            'f':'🇫',
            'g':'🇬',
            'h':'🇭',
            'i':'🇮',
            'j':'🇯',
            'k':'🇰',
            'l':'🇱',
            'm':'🇲',
            'n':'🇳',
            'o':'🇴',
            'p':'🇵',
            'q':'🇶',
            'r':'🇷',
            's':'🇸',
            't':'🇹',
            'u':'🇺',
            'v':'🇻',
            'w':'🇼',
            'x':'🇽',
            'y':'🇾',
            'z':'🇿'
            }
        emojis=[]
        for i in range(len(str)):
            emojis.append(letter_emojis_dict[str[i]])
        return emojis


    async def response(self, ctx:discord.ApplicationContext, msg:discord.Message):
        modal = discord.ui.Modal(title=f"Modal for text entry")
        input = discord.ui.InputText(label="Enter the text to turn into reactions")
        modal.add_item(input)
        # await ctx.send_modal(modal)
        await ctx.interaction.response.send_modal(modal)
        await modal.wait()
        text = input.value
        print(f"{time.strftime('%X')} on day {time.strftime('%x')} : {ctx.user.name} reacted {text} to the message {msg.id}")
        reaction_emojis = self.str_to_emojis(text)
        for i in range(len(reaction_emojis)):
            await msg.add_reaction(reaction_emojis[i])