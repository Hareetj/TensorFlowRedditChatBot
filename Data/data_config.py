import praw
from future.moves import _thread

from Data import secrets

mylock = _thread.allocate_lock()
num_threads = 0
thread_started = False

input = open("inputTest", 'w')
output = open("outputTest", 'w')
reddit = praw.Reddit(client_id= secrets.client_id,
                     client_secret= secrets.client_secret,
                     password= secrets.password,
                     user_agent='create dataset',
                     username= secrets.user)

age_1 = "all"
age_1_limit = 1
age_2 = "week"
age_2_limit = 1

white_list = ['philosophy', 'askreddit', 'casualconversation', 'iama', 'all', "Showerthoughts", "todayilearned",
              "politics", "IWantToLearn", "news"]