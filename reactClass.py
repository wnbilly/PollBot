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

    # for emoji list : https://emojipedia.org/twitter/
    def str_to_emojis(self, str):
        letter_emojis_dict={
            'a':'🇦', # letters
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
            'z':'🇿',
            ' ':'▪️', # space
            '0':'0️⃣', # numbers
            '1':'1️⃣',
            '2':'2️⃣',
            '3':'3️⃣',
            '4':'4️⃣',
            '5':'5️⃣',
            '6':'6️⃣',
            '7':'7️⃣',
            '8':'8️⃣',
            '9':'9️⃣',
            '10':'🔟'
            }
        emojis=[]
        str = str.lower() # uppercase to lowercase
        for i in range(len(str)):
            if str[i] in letter_emojis_dict :
                emojis.append(letter_emojis_dict[str[i]])
        return emojis


    async def response(self, ctx:discord.ApplicationContext, msg:discord.Message):
        modal = discord.ui.Modal(title=f"Modal for text entry")
        input = discord.ui.InputText(label="Enter the text to turn into reactions", max_length=20) # max amount of reactions is 20
        modal.add_item(input)
        # await ctx.send_modal(modal)
        await ctx.interaction.response.send_modal(modal)
        await modal.wait()
        text = input.value
        print(f"{time.strftime('%X')} on day {time.strftime('%x')} : {ctx.user.name} reacted {text} to the message {msg.id}")
        reaction_emojis = self.str_to_emojis(text)
        for i in range(len(reaction_emojis)):
            await msg.add_reaction(reaction_emojis[i])
