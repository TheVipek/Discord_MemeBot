from reddit_memes import *
from new_video_checker import *
from mmorpg_checker import mmorpg_scrape,mmorpg_post_image
from youtube import *
# from playlist_music import *
from discord.ext import commands, tasks
import discord
import random
import time
import os
import logging
import logging.handlers
# import configparser
import youtube_dl
import json


# config = configparser.ConfigParser()
# config.read('config.ini')
# config_name = 'config.ini'

if os.getcwd().endswith('\Discord'):
    path = "configs.json"
    file = os.path.abspath(path)
else:
    path = "Discord/configs.json"
    file = os.path.abspath(path)

with open(file, "r") as read_file:
    setting_file = json.load(read_file)
print(setting_file)
logger_name = 'bot.log'
logger_war_name = 'bot_war.log'
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(logger_name, mode='a',encoding='utf-8')
handler.setLevel(logging.INFO)
handler_warn = logging.FileHandler(logger_war_name, mode='a',encoding='utf-8')
handler_warn.setLevel(logging.WARNING)

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
formatter_warn = logging.Formatter('%(asctime)s - %(message)s')
handler.setFormatter(formatter)
handler_warn.setFormatter(formatter_warn)

logger.addHandler(handler)
logger.addHandler(handler_warn)
logger.info('\nStart bot')
logger.warning('\nStart bot')

class MyClient(commands.Bot):
    async def on_ready(self):
        start = time.monotonic()
        await get_meme()
        await get_animeme()
        end = time.monotonic()
        logger.info(f'Start of bot took - {round(end - start, 2)}')


MemeBot = MyClient(command_prefix='$')



@MemeBot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        logger.warning(f'User:{ctx.author} missed command : {ctx.message.content}')






@MemeBot.event
async def on_guild_join(guild):
    global file
    logger.info(f'Bot joined at {guild.name} server.')
    await asyncio.sleep(15)
    news_info = discord.Embed()
    news_info.title = "NEWS"
    news_info.description = 'Please precise channel to send mmorpg news (send name of channel / channel id)'
    await guild.system_channel.send(embed=news_info)
    success = discord.Embed()
    while True:
        channels = MemeBot.get_all_channels()
        mmorpg_channel = await MemeBot.wait_for('message')  # waiting for message from user
        context = mmorpg_channel.content
        for channel in channels:
            channel_id = channel.id
            if str(channel.type) == 'text':
                # print(channel_id)
                # print(channel)
                if (isinstance(context,str)==True and context==str(channel)) or (isinstance(context,int)==True and context==int(channel_id)):
                    # config.set('DISCORD','news_id',f'{channel_id}')
                    setting_file['DISCORD']['news_id'] = channel_id
                    success.description = f"Sucessully added {channel.name} as news channel."
                    await guild.system_channel.send(embed=success)
                    # if config.get('DISCORD','news_id') == str(channel_id):
                    if str(setting_file['DISCORD']['news_id']) == str(channel_id):
                        await guild.system_channel.send('Okay everything is alright. :)')
                        break
                    else:
                        await guild.system_channel.send('Something went wrong ,please write again.')
        break


    youtube_info = discord.Embed()
    youtube_info.title = "VIDEO"
    youtube_info.description= 'Please precise channel to send youtube videos (send name of channel / channel id)'
    await guild.system_channel.send(embed=youtube_info)
    while True:
        channels = MemeBot.get_all_channels()
        youtube_channel = await MemeBot.wait_for('message')  # waiting for message from user
        context = youtube_channel.content
        for channel in channels:
            channel_id = channel.id
            if str(channel.type) == 'text':
                if (isinstance(context, str) == True and context == str(channel)) or (
                        isinstance(context, int) == True and context == int(channel_id)):
                    # config.set('DISCORD','new_vid_id',f'{channel_id}')
                    setting_file['DISCORD']['new_vid_id'] = channel_id
                    success.description = f"Sucessully added {channel.name} as youtube channel."
                    await guild.system_channel.send(embed=success)
                    # if config.get('DISCORD','new_vid_id') == str(channel_id):
                    if str(setting_file['DISCORD']['new_vid_id'] == str(channel_id)):
                        await guild.system_channel.send('Okay everything is alright. :)')
                        break
                    else:
                        await guild.system_channel.send('Something went wrong ,please write again.')
        break
    # with open(config_name,'w') as configfile:
    #     config.write(configfile)
    with open(file, "w") as jsonFile:
        json.dump(setting_file, jsonFile)

async def news_update(ctx):
    global file
    news_update = discord.Embed()
    success = discord.Embed()
    news_update.title = "NEWS | UPDATE"
    news_update.description = 'Please precise channel to send mmorpg news (send name of channel / channel id)'
    await ctx.channel.send(embed=news_update)
    channels = MemeBot.get_all_channels()
    mmorpg_channel = await MemeBot.wait_for('message')  # waiting for message from user
    context = mmorpg_channel.content
    while True:
        for channel in channels:
            channel_id = channel.id
            if str(channel.type) == 'text':
                if (isinstance(context, str) == True and context == str(channel)) or (
                        isinstance(context, int) == True and context == int(channel_id)):
                    # if config.get('DISCORD', 'news_id') != str(channel_id):

                    if str(setting_file['DISCORD']['news_id']) != str(channel_id):

                        # config.set('DISCORD', 'news_id', f'{channel_id}')
                        setting_file['DISCORD']['news_id'] =channel_id

                        success.description = f"Sucessully updated news channel to {channel.name}"
                        await ctx.channel.send(embed=success)
                        break
                    else:
                        await ctx.channel.send('Well... It\'s the same channel')
        break
    # with open(config_name, 'w') as configfile:
    #     config.write(configfile)
    with open(file, "w") as jsonFile:
        json.dump(setting_file, jsonFile)


async def news_delete(ctx):
    global file
    success = discord.Embed()
    # if config.get('DISCORD','news_id')=="":
    if setting_file['DISCORD']['news_id'] == "":
        success.description = "There\'s no news channel."
        await ctx.channel.send(embed=success)
    else:
        # config.set('DISCORD','news_id',"")
        setting_file['DISCORD']['news_id'] = ""
        success.description="Deleted news channel."
        await ctx.channel.send(embed=success)
    # with open(config_name, 'w') as configfile:
    #     config.write(configfile)
    with open(file, "w") as jsonFile:
        json.dump(setting_file, jsonFile)

async def youtube_update(ctx):
    global file
    success = discord.Embed()
    youtube_info = discord.Embed()
    youtube_info.title = "VIDEO | UPDATE"
    youtube_info.description = 'Please precise channel to send youtube videos (send name of channel / channel id)'
    await ctx.channel.send(embed=youtube_info)
    while True:
        channels = MemeBot.get_all_channels()
        youtube_channel = await MemeBot.wait_for('message')  # waiting for message from user
        context = youtube_channel.content
        for channel in channels:
            channel_id = channel.id
            if str(channel.type) == 'text':
                if (isinstance(context, str) == True and context == str(channel)) or (
                        isinstance(context, int) == True and context == int(channel_id)):
                    # if config.get('DISCORD', 'new_vid_id') != str(channel_id):
                    if str(setting_file['DISCORD']['new_vid_id']) != str(channel_id):
                        # config.set('DISCORD', 'new_vid_id', f'{channel_id}')
                        setting_file['DISCORD']['new_vid_id'] = channel_id
                        success.description = f"Sucessully updated news channel to {channel.name}"
                        await ctx.channel.send(embed=success)
                        break
                    else:
                        await ctx.channel.send('Well... It\'s the same channel')

        break
    # with open(config_name, 'w') as configfile:
    #     config.write(configfile)
    #
    with open(file, "w") as jsonFile:
        json.dump(setting_file, jsonFile)


async def youtube_delete(ctx):
    global file
    success = discord.Embed()
    # if config.get('DISCORD', 'new_vid_id') == "":
    if setting_file['DISCORD']['new_vid_id'] == "":
        success.description = "There\'s no video channel."
        await ctx.channel.send(embed=success)
    else:
        # config.set('DISCORD', 'new_vid_id', "")
        setting_file['DISCORD']['new_vid_id'] = ""
        success.description = "Deleted video channel."
        await ctx.channel.send(embed=success)
    # with open(config_name, 'w') as configfile:
    #     config.write(configfile)
    with open(file, "w") as jsonFile:
        json.dump(setting_file, jsonFile)

@MemeBot.command()
async def news(ctx,action=""):

    if action=="update":
        await ctx.channel.send("update")
        await news_update(ctx)
    elif action=="delete":
        await ctx.channel.send("delete")
        await news_delete(ctx)
    else:
        commands = discord.Embed()
        commands.add_field(name="News",value="update - change channel to send news.\n"
                                             "delete - delete channel to send news",inline=False)
        await ctx.send(embed=commands)

@MemeBot.command()
async def video(ctx,action=""):
    if action=="update":
        await youtube_update(ctx)
    elif action=="delete":
        await youtube_delete(ctx)
    else:
        commands = discord.Embed()
        commands.add_field(name="Video",value="update - change channel to send video.\n"
                                             "delete - delete channel to send video",inline=False)
        await ctx.send(embed=commands)


@tasks.loop(hours=24)
async def renew_list():
    """
    renew_list(): run two functions get_meme() and get_animeme() at 2nd time (When bot starts it didn't run,
    beacuse it's not necessary)
    :return:
    """
    if renew_list.current_loop != 0:
        logger.info('Starting to renew list')
        await get_meme()
        await get_animeme()
        logger.info('List has been renewed.')


@MemeBot.command()
async def meme(ctx):
    logger.info('Getting meme')
    """
    meme() send embed message (using name,url,ups,comments variables that are at beggining defined)
    also meme() trigger to run get_meme() while there's less than 10 objects in earlier generated list.
    :param ctx:
    :return:
    """
    random_post = random.choice(posts)
    posts.remove(random_post)
    name = random_post.title
    url = random_post.url
    ups = random_post.score
    permalink = f"https://www.reddit.com{random_post.permalink}"
    comments = random_post.num_comments
    if len(posts) < 10:
        await get_meme()
    # color = int(config['COLORS']['deep_sea'], 16)
    color = int(setting_file['COLORS']['deep_sea'],16)
    print(color)
    embed = discord.Embed(title=name, color=color)
    embed.set_image(url=url)
    embed.set_footer(text=f"👍:{ups} ⌨️:{comments}")
    embed.add_field(name="Source ⤵", value=f"[Click for redirect to page]({permalink})")
    await ctx.channel.send(embed=embed)
    logger.info(f'Meme returned {embed}')


@MemeBot.command()
async def animeme(ctx):
    logger.info('Getting animeme')
    """
    Works like meme() function.
    :param ctx:
    :return:
    """
    random_post = random.choice(ani_posts)
    ani_posts.remove(random_post)
    name, url, ups, comments = random_post.title, random_post.url, random_post.score, random_post.num_comments
    permalink = f"https://www.reddit.com{random_post.permalink}"
    if len(posts) < 10:
        await get_meme()
    # color = int(config['COLORS']['deep_lilac'], 16)
    color = int(setting_file['COLORS']['deep_lilac'],16)
    embed = discord.Embed(title=f'{name}', color=color)
    embed.set_image(url=url)
    embed.set_footer(text=f"👍:{ups} ⌨️:{comments}")
    embed.add_field(name="Source ⤵", value=f"[Click for redirect to page]({permalink})")
    await ctx.channel.send(embed=embed)
    logger.info(f'Animeme returned {embed}')


# yt_id = config['YOUTUBE']['channel']
yt_id = setting_file['YOUTUBE']['channel']
r = checker(yt_id)
current_vid_name = r['items'][0]['snippet']['title']


@tasks.loop(minutes=1)
async def video_checker():
    """
        video_checker() if there's new video (checked by updater() function) takes name , img and url of new video
        and sends message at selected channel.
        :return:
        """
    # if str(config['DISCORD']['new_vid_id'])=="":
    if str(setting_file['DISCORD']['new_vid_id'])=="":
        logger.info('No new_vid_id channel configured. Skipping video_checker...')
    else:
        logger.info(f'Checking video')
        global current_vid_name
        # channel_to_send = config['DISCORD']['new_vid_id']
        channel_to_send = setting_file['DISCORD']['new_vid_id']
        channel_id = MemeBot.get_channel(channel_to_send)

        if updater(yt_id, current_vid_name) is not None:
            response = checker(yt_id)
            new_vid_name, new_vid_img, new_vid_url = getter(response)
            # color = int(config['COLORS']['green_smoke'], 16)
            color = int(setting_file['COLORS']['green_smoke'],16)
            embed = discord.Embed(title=f"Memes arrived!", color=color)
            embed.set_image(url=new_vid_img)
            embed.set_footer(text=f"{new_vid_name}")
            embed.add_field(name="Source ⤵️", value=f'[Click for redirect to page]({new_vid_url})', inline=True)

            current_vid_name = new_vid_name
            await channel_id.send(embed=embed)
            logger.info(f'Video returned {embed}')


@video_checker.before_loop
async def before_video_checker():
    """
    before_video_checker() just make wait until bot is ready and waits 30 for end few tasks that are running meanwhile.
    :return:
    """
    logger.info(f'Waiting until everything is done')
    await MemeBot.wait_until_ready()
    await asyncio.sleep(30)
    logger.info(f'Done.')


o_name, o_url = mmorpg_scrape()
o_img = mmorpg_post_image(o_url)


@tasks.loop(minutes=1)
async def mmorpg_news():
    """
    mmorpg_news() checks if there's new news ,if there's any img(to set is as image at embed) and send it to selected
    channel.
    :return:
    """
    # if str(config['DISCORD']['news_id'])=="":
    if str(setting_file['DISCORD']['news_id'])=="":
        logger.info('No news_id channel configured. Skipping mmorpg_news...')
    else:
        logger.info(f'Checking mmorpg news')
        global o_name

        # channel_to_send = config['DISCORD']['news_id']
        channel_to_send = setting_file['DISCORD']['news_id']
        channel_id = MemeBot.get_channel(channel_to_send)
        n_name, n_url = mmorpg_scrape()
        n_img = mmorpg_post_image(n_url)
        if n_name != o_name:
            o_name = n_name
            # color = int(config['DISCORD']['deep_teal'], 16)
            color = int(setting_file['DISCORD']['deep_teal'],16)
            embed = discord.Embed(title=f"News:{n_name}", color=color)

            if n_img is not None:
                embed.set_image(url=n_img)
                logger.info(f'Returned news with image (normal post at site) {embed}')
            embed.add_field(name="Source ⤵️", value=f'[Click for redirect to page]({n_url})', inline=True)

            await channel_id.send(embed=embed)
            logger.info(f'Returned news without image (probably post at forum) {embed}')


@mmorpg_news.before_loop
async def before_mmorpg_news():
    """
    before_mmorpg_news() just make wait until bot is ready and waits 45 for end few tasks that are running meanwhile.
    :return:
    """
    logger.info(f'Waiting until everything is done')
    await MemeBot.wait_until_ready()
    await asyncio.sleep(45)
    logger.info(f'Done')


@MemeBot.command()
async def h(ctx):
    logger.info(f'Getting help message')
    help = discord.Embed()
    help.add_field(name="Memes:",value="$meme - send standard meme \n$animeme - send meme focused at anime",inline=False)
    help.add_field(name="Status/Updates:",value="$ping - check bot ping \n $news update/delete - deletes/updates channel for news \n $video same as $news but for youtube channel",inline=False)
    help.add_field(name="Youtube:",value="$join - bot join to your channel \n$playing - check song informations s\n$start - start song \n$pause - pause song\n $skip - skip song \n $volume - change bot volume",inline=False)

    # help.description +="$ping"
    await ctx.send(embed=help)
    logger.info(f'Helper returned {help}')


@MemeBot.command()
async def ping(ctx):
    """
    ping() is checking bot latency and send it to ctx channel
    :param ctx:
    :return:
    """
    logger.info('Checking latency of bot')
    await MemeBot.wait_until_ready()
    ping = round(MemeBot.latency, 3)
    await ctx.send(ping)
    logger.info(f'Latency : {ping}')


music_info = {}
youtube_queue = {}
result_embed_yt=discord.Embed()
# vol = config['PCMVolumeTransformer']['vol']
vol = setting_file['PCMVolumeTransformer']['vol']
# @MemeBot.command()
# async def play(ctx):
#
#     """
#     play() is playing audio from queue
#     :param ctx:
#     :return:
#     """
#     global youtube_queue
#     voice_client = discord.utils.get(MemeBot.voice_clients, guild=ctx.guild)
#     print(next(iter(youtube_queue.items())))
#     is_playing = voice_client.is_playing()
#     while True:
#         if is_playing == True:
#             continue
#         else:
#
#             audio_dc = discord.FFmpegPCMAudio(executable=config['FFmpegPCMAudio']['path-ffmpeg'],
#                                               source=youtube_queu['url'], **FFMPEG_OPTIONS)
#
#             print(audio_dc)
#
#             print(result_embed_yt)
#             logger.info('Trying to play sound...')
#             voice_client.play(audio_dc)
#             logger.info('Sound')

@MemeBot.command()
async def join(ctx):
    """
    play() is connecting bot to channel at which is actually connected user that sent message.
    :param ctx:
    :return:
    """
    voice_client = discord.utils.get(MemeBot.voice_clients, guild=ctx.guild)
    # logger.info('Checking if there user sending command is on voice channel.')
    # if ctx.author.voice.channel and ctx.author.voice.channel == ctx.voice_client.channel:
    #     await ctx.send('Connected to the same channel...')
    # else:
    logger.info('getting channel at which is user and list of voice connections.')
    channel = ctx.author.voice.channel
    print(channel)
    if voice_client is not None:
        logger.info(f'moving bot from {voice_client} to {channel}')
        await voice_client.move_to(channel)
        return
    else:
        logger.info('Trying to connect...')
        await channel.connect()
        return


@MemeBot.command()
async def playing(ctx):
    """
    playing() is checking what is actually played (if anything) and send embed as message
    :param ctx:
    :return:
    """

    global result_embed_yt
    voice_client = discord.utils.get(MemeBot.voice_clients,guild=ctx.guild)
    is_playing = voice_client.is_playing()
    # TODO:Return discord.embed that contains name,url,img ,likes,views
    if is_playing == True:
        name =result_embed_yt.fields[0].value
        logger.info(f"Currently playing audio {name}")
        await ctx.send(embed=result_embed_yt)
    else:
        logger.info('Currently there\'s no audio')


@MemeBot.command()
async def start(ctx):
    """
    start() is resuming audio , if audio wasn't paused ignore.
    :param ctx:
    :return:
    """
    voice_client = discord.utils.get(MemeBot.voice_clients, guild=ctx.guild)
    is_paused = voice_client.is_paused()
    if is_paused == True:
        voice_client.resume()
        logger.info("Paused audio.")
        return
    logger.info("No audio to stop.")


@MemeBot.command()
async def pause(ctx):
    """
    pause() is pausing audio , if audio isn't played ignore.
    :param ctx:
    :return:
    """
    voice_client = discord.utils.get(MemeBot.voice_clients, guild=ctx.guild)
    is_started = voice_client.is_playing()
    if is_started == True:
        voice_client.pause()
        logger.info("Started audio.")
        return

@MemeBot.command()
async def skip(ctx):
    """
    skip() checks whether there's played / paused audio and if there's skips it
    :param ctx:
    :return:
    """
    global music_info
    voice_client = discord.utils.get(MemeBot.voice_clients, guild=ctx.guild)
    is_started = voice_client.is_playing()
    is_paused = voice_client.is_paused()
    if is_started or is_paused:
        voice_client.stop()
        logger.info(f"Skipped audio {music_info.fields[0].value}")

@MemeBot.command()
async def volume(ctx,new_volume=0):
    print('started')
    global vol
    value = new_volume
    voice_client = discord.utils.get(MemeBot.voice_clients, guild=ctx.guild)
    is_playing = voice_client.is_playing()
    if 0<=value<=100:
        if is_playing == True:
            vol = new_volume/100
            voice_client.source.volume = vol
            await ctx.send(f"Volume set to {value}")
            return
        else:
            await ctx.send('Need to play video')
            return
    await ctx.send('Value must be between 0 and 100.')

@MemeBot.command()
async def youtube(ctx, *args):

    """
    youtube() - checks for selected before :param context_to_look_for from youtube and play it as audio.
    :param ctx:
    :param context_to_look_for:
    :return:
    """
    phrase = ' '.join(args)
    global vol
    global result_embed_yt
    global music_info
    global youtube_queue
    music_info = {}
    FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
                      'options': '-vn'}
    ytdl_format_options = {'format': 'bestaudio/best', 'restrictfilenames': True, 'noplaylist': True,
                           'nocheckcertificate': True, 'ignoreerrors': False,
                           'logtostderr': False, 'quiet': True, 'no_warnings': True,
                           'default_search': 'auto', 'source_address': '0.0.0.0'}

    logger.info(f'Getting list of videos that fits to {phrase}...')
    videos = show_looked_for(phrase) #gathers results for context.
    if videos is None:
        logger.warning(f'Looks that there is 0 results for {phrase}.')
    embed = discord.Embed()
    embed.title = f"Results from searching {phrase}..."
    suggestions = ""

    for idx, i in enumerate(videos.values(), start=1):
        suggestions += f"{idx}."
        suggestions += f"{i}\n".rjust(len(i) + 5, "-")
    suggestions += f"\nSelect one of above by sending 1-5"
    embed.description = suggestions # setting suggestions string that contains all gathered results before  in embed
                                    # description
    logger.info('Sending message with results...')
    await ctx.send(embed=embed)
    logger.info('Waiting for user to response...')
    message = await MemeBot.wait_for('message') #waiting for message from user
    if int(message.content) <= len(videos):
        for idx, i in enumerate(videos.keys(), start=1):
            if idx == int(message.content):
                video = f"https://www.youtube.com/watch?v={i}"
                name = videos[i]
                result_embed_yt = discord.Embed()
                result_embed_yt.add_field(name = "Youtube",value = f"[{videos[i]}]({video})")
                music_info[videos[i]] = [{"link": video,"thumbnail":[],"likes":[],"dislikes":[],"url":[]}]
                # logger.info('Sending previously selected result by user...')
                # await ctx.send(embed=music_info)
            #     print(ctx.member.voice

    is_join = await join(ctx)
    voice_client = discord.utils.get(MemeBot.voice_clients, guild=ctx.guild) #get MemeBot voice client in server
                                                                             # from
                                                                             #which content was sent
    with youtube_dl.YoutubeDL(ytdl_format_options) as ydl:
        logger.info(f'Downloading infomation from {video} to play sound ')
        audio_s = ydl.extract_info(video, download=False) #get info from video
        result_embed_yt.set_thumbnail(url=audio_s['thumbnail'])
        result_embed_yt.set_footer(text= f"{audio_s['like_count']} 👍   {audio_s['dislike_count']} 👎  ")
        music_info[name][0]['thumbnail'].append(audio_s['thumbnail'])
        music_info[name][0]['likes'].append(audio_s['like_count'])
        music_info[name][0]['dislikes'].append(audio_s['dislike_count'])
        music_info[name][0]['url'].append(audio_s['url'])

    # youtube_queue.update(music_info)
    # print(youtube_queue[0])
    if os.path.exists(setting_file['FFmpegPCMAudio']['path-ffmpeg'])==True:
        audio_dc = discord.PCMVolumeTransformer(discord.FFmpegPCMAudio(executable=setting_file['FFmpegPCMAudio']['path-ffmpeg'],
                                        source=audio_s['url'], **FFMPEG_OPTIONS),volume=float(vol))
    else:
        audio_dc = discord.PCMVolumeTransformer(discord.FFmpegPCMAudio(source=audio_s['url']),volume=float(vol))

    print(audio_dc)
    print(result_embed_yt)
    logger.info('Trying to play sound...')
    voice_client.play(audio_dc)
    logger.info('Sound')
    # TODO:Check whether audio is still playing and if not remove element from list and play other



renew_list.start()
video_checker.start()
mmorpg_news.start()
MemeBot.run(setting_file['DISCORD']['token'])
