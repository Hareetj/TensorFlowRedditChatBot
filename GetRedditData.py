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
    def qualifyData(self, string):
        string = string.lower()
        if len(string) > 600:
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
        return True

    def stringJoin(self, string):
        splitStr = string.split('\n')
        strJoin = ""
        for s in splitStr:
            #print ("SPLIT " + s)
            strJoin += s
        return strJoin

    def generateData(self):
        count = 0
        subreddit = self.reddit.subreddit(self.subreddit)
        top = subreddit.top('all')
        for thread in top:
            print (thread.title)
            #One off post that all has the same comments...not the best for our dataset :)
            if (thread.title == "What bot accounts on reddit should people know about?"):
                continue
            #increase limit for bigger dataset
            thread.comments.replace_more(limit=0)
            #thread.comments = top level comments forest
            top_level = None
            child = None
            for comment in thread.comments.list():
                if (self.qualifyData(comment.body)):
                    #print ("Top Level Comment: " + self.stringJoin(comment.body))
                    top_level = self.stringJoin(comment.body)
                    comment.replies.replace_more(limit=None, threshold=0)
                    for c in comment.replies:
                        #print ("Original subcomment: " + c.body)
                        if self.qualifyData(c.body):
                            #print ("actually chosen: " + self.stringJoin(c.body))
                            child = self.stringJoin(c.body)
                            break
                    if top_level is not None and child is not None:
                        #print ("input: " + top_level)
                        #print ("output: " + child)
                        with open("input", 'a') as input:
                            input.write(str(top_level) + '\n')
                        with open("output", 'a') as out:
                            out.write(str(child) + '\n')
                        top_level = None
                        child = None
                        count += 1
        print(count)

def main():
    #multireddit = GenData("seduction+askreddit+science+politics+theredpill+philosophy")
    multireddit = GenData("askreddit")
    multireddit.generateData()

if __name__ == '__main__':
	main()
