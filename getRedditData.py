import re

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
        self.start = 1

    def qualifyData(self, string):
        string = string.lower()
        if len(string) > 1000:
            return False
        if len(string) < 50:
            return False
        if string == " ":
            return False
        if "deleted" in string:
            return False
        if "removed" in string:
            return False
        if "http://" in string:
            return False
        if "https://" in string:
            return False
        if "edit:" in string:
            return False
        if "edited:" in string:
            return False
        isascii = lambda string: len(string) == len(string.encode())
        if not isascii(string):
            return False
        if "<" in string:
            return False
        if ">" in string:
            return False
        return True

    def stringJoin(self, string):
        splitStr = string.split('\n')
        strJoin = ""
        for s in splitStr:
            strJoin += s + " "
        strJoin = re.sub('[ \t\n]+', ' ', strJoin)
        strJoin = re.sub('\^', '', strJoin)
        strJoin = re.sub('\\\\', '', strJoin)
        return strJoin

    def writeToFile (self, top_level, child):
        if top_level is not None:
            if child is not None:
                with open("input", 'a') as input:
                    input.write(top_level + "#### " + str(self.start) + '\n')
                with open("output", 'a') as out:
                    out.write(child + "#### " + str(self.start) + '\n')
                self.start += 1
                return True
        return False

    def generateData(self, age = 'all', limit = '100'):
        count = 0
        print ("######### " + self.subreddit + " ############")
        subreddit = self.reddit.subreddit(self.subreddit)
        top = subreddit.top(age, limit = int(limit))
        top_level = None
        child = None
        for thread in top:
            #print (thread.title)
            #One off posts that all has the same comments...not the best for our dataset :)
            if (thread.title == "What bot accounts on reddit should people know about?"):
                continue
            if (thread.title == "You and a super intelligent snail both get 1 million dollars, and you both become immortal, however you die if the snail touches you. It always knows where you are and slowly crawls toward you. What's your plan?"):
                continue
            #increase limit for bigger dataset
            thread.comments.replace_more(limit=0)
            #Use this command to get all replies for top level -> second level, seconed level - > third level, etc
            #for comment in thread.comments.list():
            for comment in thread.comments.list():
                if (self.qualifyData(comment.body)):
                    top_level = self.stringJoin(comment.body)
                    #print ("Top Leve: " + top_level)
                    comment.replies.replace_more(limit=None, threshold=0)
                    for c in list(comment.replies):
                        #print ("Original subcomment: " + c.body)
                        if self.qualifyData(c.body):
                            #print ("actually chosen: " + self.stringJoin(c.body))
                            child = self.stringJoin(c.body)
                            break
                    if (self.writeToFile(top_level, child)):
                        count += 1
                    top_level = None
                    child = None
        print(count)

def main():
    #splititng into specific subreddits allows more control over content
    white_list = ['askreddit', 'philosopy', 'casualconversation', 'iama', 'all']
    #for subreddit in white_list:
    #    mysub = GenData(subreddit)
    #    mysub.generateData()
    #    mysub.generateData("week", 30)

    #~ For testing purposes ~
    askreddit = GenData("askreddit")
    askreddit.generateData()
    askreddit.generateData("week",30)
    philosophy = GenData("philosophy")
    philosophy.generateData()
    philosophy.generateData("week",30)
    casualConv = GenData("casualconversation")
    casualConv.generateData()
    casualConv.generateData("week", 30)
    ama = GenData("iama")
    ama.generateData()
    ama.generateData("week", 30)
    all = GenData("all")
    all.generateData()
    all.generateData("week", 30)

if __name__ == '__main__':
    main()
