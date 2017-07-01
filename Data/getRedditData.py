import _thread
import re
from Data.data_config import *

class GenData(object):
    def __init__(self, subreddit):
        self.subreddit = subreddit
        self.reddit = reddit

    def qualifyData(self, string):
        string = string.lower()
        if len(string) > 300:
            return False
        if len(string) < 0:
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
        if "/u" in string:
            return False
        if "/r" in string:
            return False
        if "u/" in string:
            return False
        if "r/" in string:
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
        string = string.replace("\r", " ")
        splitStr = string.split('\n')
        strJoin = ""
        for s in splitStr:
            strJoin += s + " "
        strJoin = re.sub('[ \t\n]+', ' ', strJoin)
        strJoin = re.sub('\^', '', strJoin)
        strJoin = re.sub('\\\\', '', strJoin)
        return strJoin.lower()

    def generateData(self, age = 'all', limit = 1):
        my_dict = dict()
        global num_threads
        global thread_started
        subreddit = self.reddit.subreddit(self.subreddit)
        top = subreddit.top(age, limit = (limit))
        num_threads += 1
        thread_started = True
        for thread in top:
            #One off posts that all has the same comments...not the best for our dataset :)
            if (thread.title == "What bot accounts on reddit should people know about?"):
                continue
            if (thread.title == "You and a super intelligent snail both get 1 million dollars, and you both become immortal, however you die if the snail touches you. It always knows where you are and slowly crawls toward you. What's your plan?"):
                continue
            thread.comments.replace_more(limit=0)
            for comment in thread.comments.list():
                #find a top level comment
                if (self.qualifyData(comment.body)):
                    comment.replies.replace_more(limit=None, threshold=0)
                    #find a reply
                    for r in list(comment.replies):
                        if self.qualifyData(r.body):
                            reply = self.stringJoin(r.body)
                            top_level = self.stringJoin(comment.body)
                            my_dict[top_level] = reply
                            break
        self.writeToFile(my_dict)

    def writeToFile(self, my_dict):
        global num_threads
        global mylock
        print("Count: " + str(len(my_dict)) + " subreddit: " + self.subreddit)
        mylock.acquire()
        for parent,child in my_dict.items():
            input.write(parent + "\n")
            output.write(child + "\n")
        num_threads -= 1
        print("Done writing: " + self.subreddit)
        mylock.release()
        _thread.exit()

def main():
    global num_threads
    global thread_started
    for subreddit in white_list:
        mysub = GenData(str(subreddit))
        _thread.start_new_thread(mysub.generateData, (age_1, age_1_limit))
        _thread.start_new_thread(mysub.generateData, (age_2, age_2_limit))
    while not thread_started:
        pass
    while num_threads>0:
        pass
if __name__ == '__main__':
    main()
