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
            for comment in thread.comments:
                if (self.qualifyData(comment.body)):
                    #TODO: split comment into master/highest rated child and write to two files
                    #TODO: Only write to file if top level comment has a subcomment
                    print (self.stringJoin(comment.body))
                    comment.replies.replace_more(limit=4)
                    for c in comment.replies:
                        if self.qualifyData(c.body):
                            print (self.stringJoin(c.body))
                            break
                        else:
                            print ("did not qualify")
                    print ("--------------")
                    count += 1

            break
        print(count)

def main():
    askreddit = GenData("askreddit")
    askreddit.generateData()

if __name__ == '__main__':
	main()
