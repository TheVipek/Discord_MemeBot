from googleapi_auth import *




#Function checker(arg) checks selected channel and returns reponse (latest activites this channel (informations about videos etc...))
def checker(channel_id):
    if channel_id:
        r_for_channel = youtube.activities().list(
            part="snippet,contentDetails,id",
            channelId=channel_id
        )
        response = r_for_channel.execute()
        return response



#Function getter(arg) takes response from checker as argument and return from it video_name,video_img,video_url for later usage.
def getter(response):
    if response:
        video_name = response['items'][0]['snippet']['title']
        video_img = response['items'][0]['snippet']['thumbnails']['standard']['url']
        video_id = response['items'][0]['contentDetails']['upload']['videoId']
        video_url = f"https://www.youtube.com/watch?v={video_id}"
        return video_name,video_img,video_url



#Function updater(arg) takes video_name as argument and channel_id to frequently check if there's any new video
#and if there's video_name value is changed to newest one.
def updater(channel_id,vid_name):
    r = checker(channel_id)
    if vid_name != r['items'][0]['snippet']['title']:
        return r['items'][0]['snippet']['title']
    else:
        return None



