# -*- coding: utf-8 -*-
"""
Created on Tue Dec 20 01:53:06 2016

@author: bus-superbowl
"""
import pymongo
import datetime


col =  pymongo.MongoClient("localhost",27017)["tweets"]["elections.test.1"]

col.count()

import pandas
import vincent


trump_search_tags = ['trump','donald']
clinton_search_tags = ['clinton','hillary']
#{"created_ts":{'$lt': datetime.datetime(2016, 11, 8, 4, 00)}}
#{"created_ts":{'$gte': datetime.datetime(2016, 11, 9, 4, 45)}}
trump_pos_timeline = []
trump_neg_timeline = []
clinton_pos_timeline = []
clinton_neg_timeline = []
for tweet in col.find({"created_ts":{'$gte': datetime.datetime(2016, 11, 9, 4, 45)}}):
   terms_hash = tweet['hashtags']
   if any(("trump" or "donald") in s.lower() for s in terms_hash):
    if( tweet["pos_prob"] > 0.6 ):
      trump_pos_timeline.append(tweet['created_ts'])
    elif( tweet["neg_prob"] > 0.6 ): 
      trump_neg_timeline.append(tweet['created_ts'])
   elif any(("clinton" or"hillary") in s.lower() for s in terms_hash):
    if( tweet["pos_prob"] > 0.6 ):
      clinton_pos_timeline.append(tweet['created_ts'])
    elif( tweet["neg_prob"] > 0.6 ): 
      clinton_neg_timeline.append(tweet['created_ts'])
 
ones1 = [1]*len(trump_pos_timeline)
idx1 = pandas.DatetimeIndex(trump_pos_timeline)
axis_trump_pos = pandas.Series(ones1, index=idx1)
per_hour_trump_pos = axis_trump_pos.resample('60Min', how='sum').fillna(0)
#-----------------------------------------------------------------
ones2 = [1]*len(clinton_pos_timeline)
idx2 = pandas.DatetimeIndex(clinton_pos_timeline)
axis_clinton_pos = pandas.Series(ones2, index=idx2)
per_hour_clinton_pos = axis_clinton_pos.resample('60Min', how='sum').fillna(0)
#-----------------------------------------------------------------------------
ones3 = [1]*len(trump_neg_timeline)
idx3 = pandas.DatetimeIndex(trump_neg_timeline)
axis_trump_neg = pandas.Series(ones3, index=idx3)
per_hour_trump_neg = axis_trump_neg.resample('60Min', how='sum').fillna(0)
#-----------------------------------------------------------------
ones4 = [1]*len(clinton_neg_timeline)
idx4 = pandas.DatetimeIndex(clinton_neg_timeline)
axis_clinton_neg = pandas.Series(ones4, index=idx4)
per_hour_clinton_neg = axis_clinton_neg.resample('60Min', how='sum').fillna(0)
 
# all the data together
election_data = dict(clinton_pos=per_hour_clinton_pos, clinton_neg=per_hour_clinton_neg,trump_pos=per_hour_trump_pos, trump_neg=per_hour_trump_neg,)
# we need a DataFrame, to accommodate multiple series
all_matches = pandas.DataFrame(data=election_data,
                               index=per_hour_trump_pos.index)
# Resampling as above
all_matches = all_matches.resample('60Min', how='sum').fillna(0)
 
# and now the plotting
time_chart = vincent.Line(all_matches[['clinton_pos','clinton_neg','trump_pos','trump_neg']])
time_chart.axis_titles(x='Time', y='Freq')
time_chart.legend(title='Matches')
time_chart.to_json('time_chart.json')