import requests
import configparser

# config = configparser.ConfigParser
# config.read('config.ini')
import json
import os
if os.getcwd().endswith('/Discord'):
    path = "configs.json"
    file = os.path.abspath(path)
else:
    path = "Discord/configs.json"
    file = os.path.abspath(path)

with open(file, "r") as read_file:
    setting_file = json.load(read_file)


#pass username and password
data = {'grant_type':'password',
        'username':setting_file['REDDIT']['username'],
        'password':setting_file['REDDIT']['password']}

#personal use script and SECRET
auth = requests.auth.HTTPBasicAuth(setting_file['REDDIT']['id'],setting_file['REDDIT']['secret'])
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