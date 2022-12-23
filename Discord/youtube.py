from googleapi_auth import *



#TODO:Get list of videos from selected phrase.

def show_looked_for(phrase):
    print(phrase)
    response = youtube.search().list(
        part="snippet",
        maxResults=5,
        q=phrase,
        type="video"
    )
    videos = {}
    results = response.execute()
    amount_of_videos =results['pageInfo']['resultsPerPage']
    # videoId= results['items'][0]['id']['videoId']
    # videoName= results['items'][0]['snippet']['title']
    for i in range(0,amount_of_videos):
        videos[f"{results['items'][i]['id']['videoId']}"] = results['items'][i]['snippet']['title']
    return videos

#TODO:Show 5 results from searched phrase.