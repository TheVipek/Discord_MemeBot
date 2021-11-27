import requests
import configparser

# config = configparser.ConfigParser
# config.read('config.ini')
import json
import os



#pass username and password
data = {'grant_type':'password',
        'username':os.getenv('REDDIT_username'),
        'password':os.getenv("REDDIT_password")}

#personal use script and SECRET
auth = requests.auth.HTTPBasicAuth(os.getenv("REDDIT_token"),os.getenv("REDDIT_secret"))
#headers info
headers = {'MemeBot':'TheVipek'}
#send request for Oauth token
r = requests.post('https://www.reddit.com/api/v1/access_token',
                  data=data,
                  headers=headers,
                  auth=auth)

#convert response to JSON and get token value
TOKEN = r.json()['access_token']
headers = {**headers, **{'Authorization': f"bearer {TOKEN}"}}

requests.get('https://oauth.reddit.com/api/v1/me', headers=headers)