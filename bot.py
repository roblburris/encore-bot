import discord
from discord.ext import commands
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

client_credentials_manager = SpotifyClientCredentials()
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
bot = commands.Bot(command_prefix=';', case_insensitive=True)

token = 'null'
bot.remove_command('help')


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

# function that shortens the process of getting the Spotify URI key for a specified artist
def get_artist(name):
    results = sp.search(q='artist:' + name, type='artist')
    items = results['artists']['items']
    if len(items) > 0:
        return items[0]
    else:
        return None


# return artist info for specified artist
@bot.command()
async def info(ctx, *, args):  # * allows us to pass multiple parameters w/o having to worry
    # about the exact number of params passed

    artist = get_artist(args)
    name = artist['name']
    artist = artist['external_urls']['spotify']
    await ctx.send("Here's the Spotify Page for: **" + name + "** \n" + artist)


def get_uri(artist):
    return artist['uri']


# returns the number of followers and Spotify popularity score for a specified artist
@bot.command()
async def popularity(ctx, *, args):
    artist = get_artist(args)
    name = artist['name']
    await ctx.send("Popularity Statistics on **" + name + "**: \n*Followers*: " + '{:,}'.format(
        artist['followers']['total']) + "\n*Popularity*: " + str(artist['popularity']) + "/100")


# returns the 5 most recent albums released by a specified artist
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
    cur = sp.search(q='album:' + args, type='album')
    await ctx.send(cur['albums']['items'][0]['images'][0]['url'])


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

# return 30 second preview of a specified song
@bot.command()
async def preview(ctx, *, args):
    song = sp.search(q='track:' + args, type='track')
    await ctx.send(song['tracks']['items'][0]['external_urls']['spotify'])

# return statistics on a song, artist, or album
@bot.command()
async def stats(ctx, arg1, *, args):
    if arg1 == 'track':
        query = sp.search(q='track:' + args, type='track')['tracks']['items'][0]
        await ctx.send("Artist: **" + query['artists'][0]['name'] + "**\n" +
                       "Release Date for **" + query['name'] + "**: " +
                       format_date(query['album']['release_date']) + "\nPopularity: " +
                       str(query['popularity']) + "/100" + "\nAlbum Art: " + query['album'][
                           'images'][0]['url'] + "\nLink: " + query['external_urls']['spotify'])
    elif arg1 == 'artist':
        await ctx.send("Use the `;popularity` command instead!")
    elif arg1 == 'album':
        print(arg1)
    else:
        await ctx.send('Invalid query. Make sure you use track, artist, or album when using '
                       '`;stats`!')


months = ["January", "February", "March", "April", "May", "June", "July", "August", "September",
          "October", "November", "December"]

# function that formats Spotify dates from DD/MM/YYYY to MM/DD/YYYY
def format_date(date):
    temp = ""
    for x in range(len(date)):
        if date[x] == '-':
            temp += ' '
        else:
            temp += date[x]
    num_dates = [int(s) for s in temp.split() if s.isdigit()]

    return str(months[num_dates[1] % 12 - 1]) + " " + str(num_dates[2]) + ", " + str(num_dates[0])


commands = {'status': "Returns whether or not the bot is online as well as the latency",
            'info': "Returns the Spotify page for a specified artist", 'popularity': "Returns the "
            "Spotify popularity metric for a specified artist",
            'albums': "Sends the 5 most recent albums released by a specified artist ",
            'art': "Sends the album cover/art for a specified album",
            'portrait': "Returns the Spotify cover image for a specified artist",
            'album': "Sends a link to a specified album",
            'preview': "Sends a 30 second preview/Spotify link for a specified song",
            'stats': "Returns Spotify generated statistics on a specified track"}

# defines the help command
@bot.command()
async def help(ctx):
    cur = "Here are all of the commands for Encore!\n"
    for key, value in commands.items():
        cur += "`" + key + "` - " + value + "\n"
    await ctx.send(cur)

# set bot status
@bot.event
async def on_ready():
    print('We have logged in as {0.user}'.format(bot))
    activity = discord.Activity(name='Listening to 트와이스|;help', type=discord.ActivityType.listening)
    await bot.change_presence(activity=activity)


bot.run(token)
