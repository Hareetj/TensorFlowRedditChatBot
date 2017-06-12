import praw
import secrets

reddit = praw.Reddit(client_id= secrets.client_id,
                     client_secret= secrets.client_secret,
                     password= secrets.password,
                     user_agent='chatbot',
                     username= secrets.user)

print (reddit.user.me())