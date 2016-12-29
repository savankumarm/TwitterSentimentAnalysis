# -*- coding: utf-8 -*-
"""
Created on Sun Dec 04 13:46:58 2016

@author: bus-superbowl
"""

#155.97.56.145
import pymongo
import re
import datetime
# this method converts the time stamp into mili seconds
def date_to_mil(date):
    if isinstance(date, datetime.datetime):
        epoch = datetime.datetime.utcfromtimestamp(0)
        return float((date - epoch).total_seconds() * 1000.0)

#this method extracts the relevant attributes from the JSON tweet object and transforms the relavant fields like location, timestamp 		
def separate_ads(sourceCol,destCol,starttime,endtime,word_lst,flag):
  gap=  7*60*60*1000# time adjustment to match with MST
  for tweet in sourceCol.find({"lang": "en"}):
       result = re.findall(r"(?=("+'|'.join(word_lst)+r"))",tweet["text"],re.I)
       text = ""
       hashtags=[]
       mst_time_stamp=int(tweet ["timestamp_ms"])-gap
       if 'retweeted_status' in tweet: 
         hashtags = [ rt['text'] for rt in tweet ['retweeted_status']['entities']['hashtags']]
         text = tweet['retweeted_status']['text']
         is_retweet = 1
       else:
         text = tweet['text']
         hashtags = [ hashtag ['text'].lower() for hashtag in tweet ['entities']['hashtags']]
         is_retweet =0
        
       match_tags = re.findall(r"(?=("+'|'.join(word_lst)+r"))", " ".join(hashtags),re.I)
       coordinates= 0
       location = None
       place =  tweet['place']
       if None != place:
          location = place['full_name']
          coordinates = place ['bounding_box']['coordinates']
       
       if (result or (len(match_tags)>0)):
           d= {"id": tweet["id"],
           "tweet_id_str": tweet["id_str"],
           "created_ts":datetime.datetime.utcfromtimestamp(float(tweet ["timestamp_ms"])/1000.0)- datetime.timedelta(hours=7),
           "timestamp_ms": mst_time_stamp,
           "text": text,
           "hashtags": hashtags,
           "user": tweet["user"]["screen_name"],
           "source": tweet["source"],
           "retweet_count":tweet["retweet_count"],
          "favorite_count": tweet ["favorite_count"],
          "followers_count": tweet["user"]["followers_count"],
          "coordinates": coordinates,
          "geo": location,
          "time_zone":tweet["user"]["time_zone"],
          "lang": tweet["lang"],
          "flag": flag,
          "is_retweet":is_retweet,
          }
           if  starttime <= int(tweet ["timestamp_ms"]) <= endtime:
            try:
             destCol.insert_one(d)
            except pymongo.errors.DuplicateKeyError:
             pass
# specifiying the source and destination IP adresss   
sourceIP = "155.97.56.48"# server 3
destIP = "155.97.56.145"# server 7           
sourceCol =  pymongo.MongoClient(sourceIP,27017)["tweets"]["elections.v0"]   
destCol =  pymongo.MongoClient(destIP,27017)["tweets"]["elections.test.1.1"]
#destCol =  pymongo.MongoClient(destIP,27017)["tweets"]["elections.step1"]
#create a unique indexed ID 
destCol.create_index("id",unique=True)

#starttime = date_to_mil(datetime.datetime(2016, 11, 9, 4, 45))
#endtime = date_to_mil(datetime.datetime(2016, 11, 20, 00, 00))


starttime = date_to_mil(datetime.datetime(2016, 11,1, 00, 00))
endtime = date_to_mil(datetime.datetime(2016, 11, 8, 4, 00))

#Key words to identify tweets belonging to trump
word_lst1 = ['trump','DONALDTRUMP','DONALD TRUMP','donald']

#flag to identify Trump tweets
separate_ads(sourceCol,destCol,starttime,endtime,word_lst1,0)  

sourceCol.count()
destCol.count()#938626
#test.1 2,546,699
#step1 2,505,617
destCol1 =  pymongo.MongoClient(destIP,27017)["tweets"]["elections.test.1.1"]
destCol2 =  pymongo.MongoClient(destIP,27017)["tweets"]["elections.test.1.2"]
print (destCol1.count())#938626
print (destCol2.count())#94824
#Key words to identify tweets belonging to Hillary
word_lst2 = ['clinton','HillaryClinton','Hillary','CLINTON']


#flag to identify HillaryClinton tweets
separate_ads(sourceCol,destCol,starttime,endtime,word_lst2,1)  
         
         
col = pymongo.MongoClient()["tweets"]["elections.test.1"]
col.count()

for tweet in col.find():
    col.update_one({
      'id': tweet['id']
    },{
      '$set': {
        'created_ts': datetime.datetime.utcfromtimestamp(float(tweet ["timestamp_ms"])/1000.0),
      }
    }, upsert=False)

for i in sourceCol.find().sort("timestamp_ms", 1).limit(1):
   print( i ['created_at'])
   print( i ['text'])
   print( i ['id'])
   
   #db.collection.find().sort({_id:-1}).limit(1).pretty()
for i in destCol.find().sort('timestamp_ms',-1).limit(1):
   print( i ['created_ts'])
   print( i ['text'])
   print( i ['id'])

   
db_connect = pymongo.MongoClient(sourceIP,27017)
database_name = 'tweets'
database = db_connect[database_name]
collection = database.collection_names(include_system_collections=False)
for collect in collection:
    print (collect)
 StreamingTutorial
elections.v0
elections.v1


endtime = date_to_mil(datetime.datetime(2016, 11, 8, 00, 00))

print (datetime.datetime.utcfromtimestamp(float(endtime)/1000.0))
