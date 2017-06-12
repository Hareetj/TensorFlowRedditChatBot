import praw

import secrets


class GenData(object):
    def __init__(self, subreddit):
        self.subreddit = subreddit
        self.reddit = praw.Reddit(client_id= secrets.client_id,
                             client_secret= secrets.client_secret,
                             password= secrets.password,
                             user_agent='chatbot',
                             username= secrets.user)
    def getComments(self):
        subreddit = self.reddit.subreddit(self.subreddit)
        for comment in subreddit.stream.comments():
            if ('*' not in comment.body):
                print (comment.body)
def main():
    askreddit = GenData("askreddit")
    askreddit.getComments()

if __name__ == '__main__':
	main()
