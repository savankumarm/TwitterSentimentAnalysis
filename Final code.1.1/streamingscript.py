
# coding: utf-8

# In[16]:


import tweepy
import pymongo
from datetime import datetime
import time

api_key = "**************************" # <---- Add your API Key
api_secret = "***********************************" # <---- Add your API Secret
access_token = "****************************************" # <---- Add your access token
access_token_secret = "******************************************" # <---- Add your access token secret

auth = tweepy.OAuthHandler(api_key, api_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)

col = pymongo.MongoClient()["tweets"]["elections.v1"]
col.count()

from tweepy.streaming import StreamListener
class MyStreamListener(StreamListener):
    
    counter = 0
    
    def __init__(self, max_tweets=1000, *args, **kwargs):
        self.max_tweets = max_tweets
        self.counter = 0
        super(MyStreamListener, self).__init__(*args, **kwargs)
    
    def on_connect(self):
        self.counter = 0
        self.start_time = datetime.now()
        
    def on_error(self, status):
        print status
    
    def on_status(self, status):
        # Increment counter
        self.counter += 1
        
        # Store tweet to MongoDB
        col.insert_one(status._json)
        
        
        if self.counter % 1 == 0:
            mining_time = datetime.now() - self.start_time
            if self.counter >= self.max_tweets:
                myStream.disconnect()
                print("Finished at  %s" % datetime.now())
                print("Total Mining Time: %s" % (mining_time))
                print("Tweets/Sec: %.1f" % (self.max_tweets / mining_time.seconds))
   
    
myStreamListener = MyStreamListener(max_tweets=100)
myStream = tweepy.Stream(auth = api.auth, listener=myStreamListener)

keywords = ["#trump",
            "#clinton",
            "#elections16"
           ]
while True:
# Start a filter with an error counter of 20
 for error_counter in range(20):
    try:
        myStream.filter(track=keywords)
        print("Tweets collected: %s" % myStream.listener.counter)
        print("Total tweets in collection: %s" % col.count())
        break
    except:
        print("ERROR# %s" % (error_counter + 1))
        str(datetime.now())
        time.sleep(200)
        pass
        




