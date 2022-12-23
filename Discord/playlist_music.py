from spotify_auth import *


#TODO:Write function that returns 50 most popular by followers playlists.

def getMostFollowedPlaylists():
    playlists = {}
    for playlist in sp.user_playlists('spotify')['items']:
        playlists[playlist['name']]=playlist['id']
    return playlists
playlists = getMostFollowedPlaylists()
# print(playlists)
#TODO:Write function that shows avaliable playlists.
def showAvaliablePlaylists(playlists):
    # print("Actually avaliable playlist are :")
    for i,(k,v) in enumerate(playlists.items(),1):
        print(f"{i}:{k}")
# all = showAvaliablePlaylists(playlists)
#TODO:Write function that get playlist that we want (if contains substring return it as result)
def getPlaylist(name_of_playlist):
    # print("Found results: ")
    results = {}
    for i, (k, v) in enumerate(playlists.items(), 1):
        if name_of_playlist.lower() in k.lower():
            results[i]={'name':k,'id':v}
            # print(k)
    return results
selected = getPlaylist('hip')
print(selected[31])
#TODO:Write function that returns 50 songs from selected before playlist.
def getSongsFromPlaylist(playlist_id):
    playlist = playlist_id.get('id')
    print(playlist)
    songs = {}
    for track in sp.playlist_tracks(playlist_id=playlist)['items']:
        songs[track['track']['name']]={track['track']['id'],track['track']['external_urls']['spotify']}
        # print(track['track'])
        # print(track['track']['name'])
        # print(track['track']['id'])
        # print(track['track']['external_urls']['spotify'])
    return songs
songs = getSongsFromPlaylist(selected[31])
print(songs)
#TODO:Import it to bot.
