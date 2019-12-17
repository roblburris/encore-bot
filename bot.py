import asyncio
import discord
from discord.ext import commands

bot = commands.Bot(command_prefix=';')
token = 'null'


@bot.event
async def on_ready():
    print('We have logged in as {0.user}'.format(bot))


@bot.event
async def on_message(message):
    curmessage = message.content.lower()

    if "hello" in curmessage and message.author != bot.user:
        await message.channel.send('Hello!')
        print("sent hello!")


@bot.command()
async def test(ctx):
    await ctx.send("Hello World!")
    print('hi')


bot.run(token)
