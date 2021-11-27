import threading
import os
import asyncpraw
import praw
import asyncio
# import configparser
import json

#
# config = configparser.ConfigParser()
# config.read('config.ini')


reddit = asyncpraw.Reddit(
    client_id=os.getenv('REDDIT_token'),
    client_secret=os.getenv('REDDIT_secret'),
    user_agent=os.getenv('REDDIT_agent')
)

subreddits = ['unexpected', 'memes', 'funny', 'dankmemes', 'Tinder', 'HistoryMemes', 'trashy']
ani_subreddits=['animemes','goodanimemes','animememes','AnimeMeme','okbuddybaka']
# variable to store memes
posts = []
ani_posts = []
async def get_meme():

#iterate through wanted subreddits and get memes from them
    for subreddit in subreddits:
        print(f'Getting posts from {subreddit}...')
        sub = await reddit.subreddit(subreddit)
        top = sub.top(limit=10, time_filter="week")
        #append post but using async ,which means it will 'try' to append post and while 'trying' it will do it with next and next post... Which increase performance of script
        async for post in top:
            posts.append(post)

#Basically working the same as get_meme()
async def get_animeme():
    for subreddit in ani_subreddits:
        print(f'Getting posts from {subreddit}...')
        sub = await reddit.subreddit(subreddit)
        top = sub.top(limit=10, time_filter="week")
        async for post in top:
            ani_posts.append(post)
