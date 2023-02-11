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

    def string_adaptation(self, str):
        new_str=str[0]
        for i in range(1,len(str)):
            if str[i] in str[:i]:
                if str[i]==' ':
                    new_str += '_'
                else:
                    new_str += str[i].upper()
            else:
                new_str += str[i]
        return new_str


    # for emoji list : https://emojipedia.org/twitter/
    def str_to_emojis(self, str):
        letter_emojis_dict={
            'a':'🇦', # letters
            'A':'🅰️',
            'b':'🇧', 
            'B':'🅱️',
            'c':'🇨',
            'C':'©️',
            'd':'🇩',
            'e':'🇪',
            'f':'🇫',
            'g':'🇬',
            'h':'🇭',
            'i':'🇮',
            'I':'ℹ️',
            'j':'🇯',
            'k':'🇰',
            'l':'🇱',
            'm':'🇲',
            'M':'Ⓜ️',
            'n':'🇳',
            'o':'🇴',
            'O':'🅾️',
            'p':'🇵',
            'P':'🅿️',
            'q':'🇶',
            'r':'🇷',
            'R':'®️',
            's':'🇸',
            't':'🇹',
            'u':'🇺',
            'v':'🇻',
            'w':'🇼',
            'x':'🇽',
            'y':'🇾',
            'z':'🇿',
            ' ':'▪️', # space
            '_':'◼️', # up to 2 spaces for now
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
            '10':'🔟',
            '?':'❓', # miscaellenous
            '!':'❗',
            '+':'➕',
            '-':'➖',
            '=':'🟰'
            }
        emojis=[]
        str = str.lower() # uppercase to lowercase
        str = self.string_adaptation(str)
        for i in range(len(str)):
            if str[i] in letter_emojis_dict:
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

        response_content = "" # to answer the interaction

        
        print(f"{time.strftime('%X')} on day {time.strftime('%x')} : {ctx.user.name} reacted {text} to the message {msg.id}")
        reaction_emojis = self.str_to_emojis(text)
        for i in range(len(reaction_emojis)):
            await msg.add_reaction(reaction_emojis[i])
            response_content += f"{reaction_emojis[i]} "
        await ctx.interaction.response.send_message(content=f"Reaction {response_content} cancelled.", ephemeral=True, delete_after=1)