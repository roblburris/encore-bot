from discord.ext import commands
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

client_credentials_manager = SpotifyClientCredentials()
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
bot = commands.Bot(command_prefix=';', case_insensitive=True)

token = 'insert'


@bot.event
async def on_ready():
    print('We have logged in as {0.user}'.format(bot))


# parses messages to see if a user's message contains 'hello' in it and if it does, replies with
# 'Hello!' back
@bot.event
async def on_message(message):
    cur_message = message.content.lower()

    if "hello" in cur_message and message.author != bot.user:
        await message.channel.send('Hello!')
        print("sent hello!")

    await bot.process_commands(message)


# status command, returns ping and status of the bot
@bot.command(aliases=["test", "ping"])
async def status(ctx):
    latency = round(bot.latency, 2)
    await ctx.send("Encore is up and running! **Latency: {0}**".format(latency))
    print("Sent status with returned latency of {0}".format(latency))


# help command, returns a list of all commands with their description


# finish last once all commands are finished


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

def get_artist(name):
    results = sp.search(q='artist:' + name, type='artist')
    items = results['artists']['items']
    if len(items) > 0:
        return items[0]
    else:
        return None


# return artist info of
@bot.command()
async def info(ctx, *, args):  # * allows us to pass multiple parameters w/o having to worry
    # about the exact number of params passed

    artist = get_artist(args)
    uri = get_uri(artist)
    name = artist['name']
    artist = artist['external_urls']['spotify']
    await ctx.send("Here's the Spotify Page for: **" + name + "** \n" + artist + "\n Would you "
                                                                                 "like to see "
                                                                                 "more info "
                                                                                 "about **" + name
                   + "**?")
    await ctx.send(uri)


# join current voice channel command

# leave current voice channel command

# clear queue command


def get_uri(artist):
    return artist['uri']


@bot.command()
async def popularity(ctx, *, args):
    artist = get_artist(args)
    name = artist['name']
    print(artist)
    await ctx.send("Popularity Statics on **" + name + "**: \n*Followers*: " + '{:,}'.format(artist[
                                                                                                'followers'][
                                                                                                 'total']))


@bot.command()
async def albums(ctx, *, args):
    artist = get_artist(args)
    name = artist['name']
    uri = get_uri(artist)
    return_string = "Here are the 5 most recent albums released by **" + name + "**: \n"

    for i in range(6):
        album = sp.artist_albums(artist_id=uri, limit=1, offset=i)
        cur = album['items'][0]['name'] + " - " + album['items'][0]['external_urls']['spotify']
        return_string += cur
        return_string += "\n \n"
    await ctx.send(return_string)


# returns the cover art for a specified song album
@bot.command()
async def art(ctx, *, args):
    album = sp.search(q='album:' + args, type='album')
    await ctx.send(album['albums']['items'][0]['images'][0]['url'])


# returns the portrait of a specified artist on spotify
@bot.command()
async def portrait(ctx, *, args):
    artist = get_artist(args)
    await ctx.send(artist['images'][0]['url'])


# return album link
@bot.command()
async def album(ctx, *, args):
    album_links = sp.search(q='album:' + args, type='album')
    await ctx.send(album_links['albums']['items'][0]['external_urls']['spotify'])


@bot.command()
async def preview(ctx, *, args):
    song = sp.search(q='track:' + args, type='track')
    await ctx.send(song['tracks']['items'][0]['external_urls']['spotify'])


@bot.command()
async def stats(ctx, arg1, *, args):
    if arg1 == 'track':
        print(arg1)
    elif arg1 == 'artist':
        await ctx.send("Use the `;popularity` command instead!")
    elif arg1 == 'album':
        print(arg1)
    else:
        await ctx.send('Invalid query. Make sure you use track, artist, or album when using '
                       '`;stats`!')


bot.run(token)
