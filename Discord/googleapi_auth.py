from googleapiclient.discovery import build
# import configparser
#
# config =configparser.ConfigParser()
# config.read('config.ini')
import json
import os

if os.getcwd().endswith('\Discord'):
    path = "configs.json"
    file = os.path.abspath(path)
else:
    path = "Discord/configs.json"
    file = os.path.abspath(path)

with open(file, "r") as read_file:
    setting_file = json.load(read_file)

#get key to use API
key=setting_file['GOOGLE_API']['key']
youtube = build('youtube','v3',developerKey=key,static_discovery=False)