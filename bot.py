from discord.ext import commands

bot = commands.Bot(command_prefix=';')
token = 'null'


@bot.event
async def on_ready():
    print('We have logged in as {0.user}'.format(bot))


# parses messages to see if a user's message contains 'hello' in it and if it does, replies with 'Hello!' back
@bot.event
async def on_message(message):
    curmessage = message.content.lower()

    if "hello" in curmessage and message.author != bot.user:
        await message.channel.send('Hello!')
        print("sent hello!")

    await bot.process_commands(message)


# defines the test command
@bot.command(pass_context=True)
async def test(ctx):
    await ctx.send("Hello World!")
    print('sent \'Hello World!\'')

# defines the repeat command
@bot.command()
async def repeat(ctx, arg):
    await ctx.send(arg)
    print('sent \'' + arg + '\'')


bot.run(token)
