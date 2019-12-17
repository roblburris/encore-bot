import discord
from discord.ext import commands

bot = commands.Bot(command_prefix=';')


class RunBot:
    def __init__(self, token):
        self.token = token

    @bot.event()
    async def on_ready(self):
        print('We have logged in as {0.user}'.format(bot))

    @bot.event
    async def on_message(self, message):
        curmessage = message.content.lower()

        if "hello" in curmessage and message.author != bot.user:
            await message.channel.send('Hello!')
            print("sent hello!")

    @bot.command()
    async def test(self, ctx, arg):
        print('hi')

    async def runbot(self):
        bot.run(self.token)
