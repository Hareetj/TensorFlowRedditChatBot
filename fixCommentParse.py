from getRedditData import GenData
from praw.models import MoreComments

reddit = GenData("iama").reddit
submission = reddit.submission(id='3hq15d')

inp = open('testParse', 'w')

for top_level_comment in submission.comments:
    if isinstance(top_level_comment, MoreComments):
        continue
    print("##################################")
    com = top_level_comment.body
    com = com.replace("\r", " ")
    split = com.split(" ")
    temp = ""
    #print(split)
    for c in split:
        #print ("orig:" + c)
        temp += c + " "
        #print ("concat: " + temp)
    print(temp)
    temp2 = ""
    for c2 in temp.split(("\n")):
        temp2 += c2 + " "
    print(temp2)
    inp.write(str(temp2) + "\n")

