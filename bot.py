from discord.ext import commands

bot = commands.Bot(command_prefix=';', case_insensitive=True)

token = 'null'


@bot.event
async def on_ready():
    print('We have logged in as {0.user}'.format(bot))


# parses messages to see if a user's message contains 'hello' in it and if it does, replies with
# 'Hello!' back
@bot.event
async def on_message(message):
    curmessage = message.content.lower()

    if "hello" in curmessage and message.author != bot.user:
        await message.channel.send('Hello!')
        print("sent hello!")

    await bot.process_commands(message)


# status command, returns ping and status of the bot
@bot.command(aliases=["test", "ping"])
async def status(ctx):
    latency = round(bot.latency, 2)
    await ctx.send("Encore is up and running! **Latency: {0}**".format(latency))
    print("sent status with returned latency of {0}".format(latency))


# help command, returns a list of all commands with their description
    # finish last once all commands are finished

# I'm thinking we have a class that defines a queue with all of the queue related commands with it


# play command


# queue command

# loop playlist command

# loop song command

# now playing command

# artist command

# artist -> view overview, related, and about command

# artist -> overview/top 5 songs command

# artist -> related artists command

# artist -> about/biography command

# pause command

# shuffle queue command

# return Spotify song link command

# join current voice channel command

# leave current voice channel command

# clear queue command

bot.run(token)
