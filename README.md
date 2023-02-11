# PollBot for discord
Discord Bot to create polls and display the results.

The bot has to be launched via :

    python3 pollBot.py TOKEN

with TOKEN being your Bot Authentification Token delivered by Discord : https://github.com/reactiflux/discord-irc/wiki/Creating-a-discord-bot-&-getting-a-token

There are 4 commands available :

 - **Commands available via / in the textbar and message command**
 - /poll question answer1 answer2 ... answer 8
	 - Publishes a message displaying the percentages of votes and allowing users to vote/unvote
	 - ![poll](https://user-images.githubusercontent.com/102171805/218255929-b9c154e9-7c64-4b05-9092-2d7f554b9e19.png)

 - /poll_who question answer1 answer2 ... answer8
	 - Publishes a message displaying the names of the voters and allowing users to vote/unvote or add an answer
	 - ![poll_who](https://user-images.githubusercontent.com/102171805/218255940-a77f8d24-24e7-4cda-bfea-36aeaf5a2f23.png)

 - **Commands only available via message command**
 - react
	 - Allows to write a text as a reaction under a message via right click on message --> Applications --> React
	 - ![react](https://user-images.githubusercontent.com/102171805/218255952-be5abdc4-69e3-497f-bdc9-8ba673b8a72e.png)

 - react cancel
	- Cancel all PollBot reactions under a message

*Disclaimer : Some commands raise some errors appearing on the Discord client but they don't prevent the bot from working. I still have to fix that*
