from googleapiclient.discovery import build
# import configparser
#
# config =configparser.ConfigParser()
# config.read('config.ini')
import json
import os


#get key to use API
key=os.getenv('GOOGLE_token')
youtube = build('youtube','v3',developerKey=key,static_discovery=False)