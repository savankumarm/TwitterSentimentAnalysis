# -*- coding: utf-8 -*-
"""
Created on Mon Dec 26 14:35:28 2016

@author: bus-superbowl
"""
#{"created_ts":{'$gte': datetime.datetime(2016, 11, 9, 4, 45)}}

neutral 803209
neutral 1469703
neutral 273787
total 2546699

neu_count =0
neg_count =0
pos_count =0
for tweet in col.find({"created_ts":{'$gte': datetime.datetime(2016, 11, 9, 4, 45)}}):
   if any(("trump" or "donald") in s.lower() for s in tweet['hashtags']):
    if( tweet["pos_prob"] > 0.4 and  tweet["neg_prob"] > 0.4):
     neu_count+=1
    elif( tweet["pos_prob"] > 0.6 ):
     pos_count+=1
    elif( tweet["neg_prob"] > 0.6 ): 
     neg_count+=1

print ("neutral",neu_count)
print ("negative",neg_count)
print ("positive",pos_count)
pre
neutral 256,487
negative 362,673
positive 102,298

post
neutral 462033
negative 856841
positive 152192

total
neutral 729722
negative 1235375
positive 257392
total 2222489

neu_count =0
neg_count =0
pos_count =0
for tweet in col.find({"created_ts":{'$gte': datetime.datetime(2016, 11, 9, 4, 45)}}):
   if any(("hillary" or "clinton") in s.lower() for s in tweet['hashtags']):
    if( tweet["pos_prob"] > 0.4 and  tweet["neg_prob"] > 0.4):
     neu_count+=1
    elif( tweet["pos_prob"] > 0.6 ):
     pos_count+=1
    elif( tweet["neg_prob"] > 0.6 ): 
     neg_count+=1

print ("neutral",neu_count)
print ("negative",neg_count)
print ("positive",pos_count)

pre
neutral 34,997
negative 102,233
positive 11,776

post
neutral 12168
negative 43353
positive 6106

neutral 47303
negative 146414
positive 17942
total 211,659