import re

import praw
import secrets

class redditPost(object):
    def __init__(self, subreddit):
        self.subreddit = subreddit
        self.reddit = praw.Reddit(client_id= secrets.client_id,
                             client_secret= secrets.client_secret,
                             password= secrets.password,
                             user_agent='commenter',
                             username= secrets.user)

    def postComment(self, subreddit):
        reddit = self.reddit
        subreddit = reddit.subreddit(subreddit)
        #replace this with logic for calling the chatbot
        for submission in subreddit.stream.submissions():
            print ("Title: " + submission.title)
            submission.reply("test123!")
def main():
    redditPost.postComment("askreddit")

if __name__ == '__main__':
    main()