import time

import discord

MAX_REACTIONS = 20


# formats a string for str_to_emojis
def string_adaptation(string):
    new_str = string[0]
    for i in range(1, len(string)):
        if string[i] in string[:i]:
            if string[i] == ' ':
                new_str += '_'
            else:
                new_str += string[i].upper()
        else:
            new_str += string[i]
    return new_str


# converts a string to a list of emojis
# for emoji list : https://emojipedia.org/twitter/
def str_to_emojis(string):
    letter_emojis_dict = {
        'a': '🇦',  # letters
        'A': '🅰️',
        'b': '🇧',
        'B': '🅱️',
        'c': '🇨',
        'C': '©️',
        'd': '🇩',
        'e': '🇪',
        'f': '🇫',
        'g': '🇬',
        'h': '🇭',
        'i': '🇮',
        'I': 'ℹ️',
        'j': '🇯',
        'k': '🇰',
        'l': '🇱',
        'm': '🇲',
        'M': 'Ⓜ️',
        'n': '🇳',
        'o': '🇴',
        'O': '🅾️',
        'p': '🇵',
        'P': '🅿️',
        'q': '🇶',
        'r': '🇷',
        'R': '®️',
        's': '🇸',
        't': '🇹',
        'u': '🇺',
        'v': '🇻',
        'w': '🇼',
        'x': '🇽',
        'y': '🇾',
        'z': '🇿',
        ' ': '▪️',  # space
        '_': '◼️',  # up to 2 spaces for now
        '0': '0️⃣',  # numbers
        '1': '1️⃣',
        '2': '2️⃣',
        '3': '3️⃣',
        '4': '4️⃣',
        '5': '5️⃣',
        '6': '6️⃣',
        '7': '7️⃣',
        '8': '8️⃣',
        '9': '9️⃣',
        '10': '🔟',
        '?': '❓',  # miscaellenous
        '!': '❗',
        '+': '➕',
        '-': '➖',
        '=': '🟰'
    }
    emojis = []
    string = string.lower()  # uppercase to lowercase
    string = string_adaptation(string)
    for i in range(len(string)):
        if string[i] in letter_emojis_dict:
            emojis.append(letter_emojis_dict[string[i]])
    return emojis


# modal-based class to react to a message with discord reactions from a text input
class ReactModal(discord.ui.Modal):
    def __init__(self, ctx: discord.ApplicationContext, msg: discord.Message, *args, **kwargs):
        super().__init__(
            discord.ui.InputText(label="React Modal",
                                 placeholder="Enter the text to turn into reactions",
                                 max_length=MAX_REACTIONS),
            title="Modal for text entry",
            *args,
            **kwargs, )
        self.ctx = ctx
        self.msg = msg

    # modal callback that responds to the interaction so as to avoid errors when the modal is submitted
    async def callback(self, interaction: discord.Interaction):
        text = self.children[0].value
        await interaction.response.send_message(content=f"You reacted {text}.", ephemeral=True,
                                                delete_after=1)
        print(
            f"{time.strftime('%X')} on day {time.strftime('%x')} : {self.ctx.user.name} reacted {text} to the message {self.msg.id}")
        reaction_emojis = str_to_emojis(text)
        for i in range(len(reaction_emojis)):
            await self.msg.add_reaction(reaction_emojis[i])


# cancels the reactions of a given user of a message
async def reactions_cancel(ctx: discord.ApplicationContext, msg: discord.Message, client: discord.Client):
    response_content = ""

    # 2 loops to avoid "INTERACTION ALREADY RESPONDED TO" when too many reactions (ctx.interaction.response.defer() not working here)
    for reaction in msg.reactions:  # loop to get the emojis and make the interacion response
        response_content += f"{reaction.emoji} "

    await ctx.interaction.response.send_message(content=f"Cancelling reaction {response_content}...", ephemeral=True,
                                                delete_after=2)
    print(
        f"{time.strftime('%X')} on day {time.strftime('%x')} : {ctx.user.name} cancelled the reaction {response_content} to the message {msg.id}")
    for reaction in msg.reactions:  # loop to remove the reactions
        await reaction.remove(client.user)
