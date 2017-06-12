import praw
import requests
import json
import secrets

reddit = praw.Reddit(client_id= secrets.client_id,
                     client_secret= secrets.client_secret,
                     user_agent="chatbot",
                     username= secrets.user,
                     password= secrets.password)

#print(reddit.user.me())
