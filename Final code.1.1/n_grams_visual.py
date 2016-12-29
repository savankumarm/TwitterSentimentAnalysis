# -*- coding: utf-8 -*-
"""
Created on Tue Dec 20 01:53:06 2016

@author: bus-superbowl
"""
from nltk.corpus import stopwords
import nltk
import pymongo
import re
import string
import datetime
#import HTMLParser
#import html.parser as HTMLParser
import html
from nltk.stem import PorterStemmer

#html_parser = HTMLParser.HTMLParser()
def processTweet(tweet):
    tweet = re.sub('@[^\s]+','',tweet)#remove @ 
    tweet= html.unescape(tweet) # process the tweets
    tweet = tweet.lower()#Convert to lower case
    tweet = re.sub('((www\.[^\s]+)|(https?://[^\s]+)|(http[^\s]+))','',tweet)#remove www.* or https?://* 
    tweet = re.sub('[^a-zA-Z0-9 \n\.]', '', tweet)#consider only aplhabets
    tweet = re.sub('b4','before',tweet) #replace b4
    tweet = re.sub('[\s]+', ' ', tweet) #Remove additional white spaces
    tweet = re.sub(r'#([^\s]+)', r'\1', tweet) #remove hashtags
    tweet = tweet.strip('\'"')#trim
    return tweet
    
punctuation = list(string.punctuation)
stop = stopwords.words('english')+ [u'rt', u'via',u'The',u'', u'...']  # + punctuation  
ps = PorterStemmer()
def getFeatureVector(tweet):
  featureVector = []
  tweet=tweet.encode("utf-8")
  tweet=tweet.decode('unicode_escape').encode('ascii','ignore')
  words = tweet.split()
 # words = word_tokenize(tweet)
  for w in words:
    w= w.lower().decode('unicode_escape')
    #ignore if it is a stop word or length less than 3
    if(w in stop or len(w)<3):
        continue
    else:
        featureVector.append(w)
  return featureVector 
  
col =  pymongo.MongoClient("localhost",27017)["tweets"]["elections.test.1"]

col.count()
featureList = []

#count_search_1 = Counter()
for tweet in col.find({'text': { '$regex' : 'trump'}}):
   text = tweet["text"]
   processed = processTweet(text)
   featureVector = getFeatureVector(processed)
   featureList.extend(featureVector)

featureFreqList = nltk.FreqDist(featureList)
print(featureFreqList.most_common(15))
#----------------------------------------------------------------------
import pandas
import vincent


trump_search_tags = ['trump','donald']
clinton_search_tags = ['clinton','hillary']
#{"created_ts":{'$lt': datetime.datetime(2016, 11, 8, 4, 00)}}
dates_timline1 = []
dates_timline2 = []
for tweet in col.find({"created_ts":{'$gte': datetime.datetime(2016, 11, 9, 4, 45)}}):
   terms_hash = tweet['hashtags']
   if any(("trump" or "donald") in s.lower() for s in terms_hash):
    dates_timline1.append(tweet['created_ts'])
   elif any(("clinton" or"hillary") in s.lower() for s in terms_hash):
    dates_timline2.append(tweet['created_ts'])
 
# a list of "1" to count the hashtags
ones1 = [1]*len(dates_timline1)
# the index of the series
idx1 = pandas.DatetimeIndex(dates_timline1)
# the actual series (at series of 1s for the moment)
axis_trump = pandas.Series(ones1, index=idx1)
 
# Resampling / bucketing
per_hour_trump = axis_trump.resample('60Min', how='sum').fillna(0)
#-----------------------------------------------------------------
 
# a list of "1" to count the hashtags
ones2 = [1]*len(dates_timline2)
# the index of the series
idx2 = pandas.DatetimeIndex(dates_timline2)
# the actual series (at series of 1s for the moment)
clinton_axis = pandas.Series(ones2, index=idx2)
 
# Resampling / bucketing
per_hour_clinton = clinton_axis.resample('60Min', how='sum').fillna(0)
 
# all the data together
election_data = dict(clinton=per_hour_clinton, trump=per_hour_trump)
# we need a DataFrame, to accommodate multiple series
all_matches = pandas.DataFrame(data=election_data,
                               index=per_hour_clinton.index)
# Resampling as above
all_matches = all_matches.resample('60Min', how='sum').fillna(0)
 
# and now the plotting
time_chart = vincent.Line(all_matches[['clinton', 'trump']])
time_chart.axis_titles(x='Time', y='Freq')
time_chart.legend(title='Matches')
time_chart.to_json('time_chart.json')