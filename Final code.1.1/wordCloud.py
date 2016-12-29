# -*- coding: utf-8 -*-
"""
Created on Thu Dec 22 15:34:01 2016

@author: Savan Kumar
"""

from scipy.misc import imread
import matplotlib.pyplot as plt
from wordcloud import WordCloud, STOPWORDS
from collections import Counter
from nltk.corpus import stopwords
from nltk.util import ngrams
import pymongo
import re
import string
#import html
import html

col =  pymongo.MongoClient("localhost",27017)["tweets"]["elections.test.1"]

col.count() #2505617,2504277 

def processTweet(tweet):
    tweet = re.sub('@[^\s]+','',tweet)#remove @ 
    tweet = re.sub(r'#([^\s]+)', r'\1', tweet) #remove hashtags
    tweet= html.unescape(tweet) # process the tweets
    tweet = tweet.lower()#Convert to lower case
    tweet = re.sub('((www\.[^\s]+)|(https?://[^\s]+)|(http[^\s]+))','',tweet)#remove www.* or https?://* 
    tweet = re.sub('[^a-zA-Z0-9 \n\.]', '', tweet)#consider only aplhabets
    tweet = re.sub('b4','before',tweet) #replace b4
    tweet = re.sub('[\s]+', ' ', tweet) #Remove additional white spaces
    tweet = re.sub(r'#([^\s]+)', r'\1', tweet) #remove hashtags
    tweet = tweet.strip('\'"')#trim
    featureVector = []
    #tweet=tweet.decode('unicode_escape')
    tweet=tweet.encode("utf-8")
    tweet=tweet.decode('unicode_escape').encode('ascii','ignore')
    words = tweet.split()
 # words = word_tokenize(tweet)
    for w in words:
    #ignore if it is a stop word or length less than 3
      if(w in stop or len(w)<3):
        continue
      else:
        #w= ps.stem(w)
        featureVector.append(w.lower().decode('unicode_escape'))
    return featureVector 
 
punctuation = list(string.punctuation)
stop = stopwords.words('english') + punctuation + ['rt', 'via','…','...']   


trump_stop = stop + ['clinton','trump','donald','election2016','hillary']   
#db.stuff.find_one({'text': re.compile(clinton, re.IGNORECASE)})
trump_search_tags = ['trump','donald']
clinton_search_tags = ['clinton','hillary']
total_words=[]
trump_cotags=[]
clinton_cotags=[]
for tweet in col.find().limit(100):
    processedTweet = processTweet(tweet['text'])
    wordString=" ".join(term for term in (processedTweet))
    if any( word in wordString for word in trump_search_tags):
     trump_terms = [term for term in processedTweet if term not in trump_stop ]
     if(len(trump_terms)>0):               
      trump_cotags.append(trump_terms)
    if any( word in wordString for word in clinton_search_tags):
     clinton_terms =  [term for term in processedTweet if term not in trump_stop ] 
     if(len(clinton_terms)>0):               
      clinton_cotags.append(clinton_terms)            
  #  terms_ngrams = ngrams(terms_only,1)
    total_trump_words = ' '.join( str(i) for i in trump_cotags)
  #  total_words.append(words) 

  
 #Hash tags word cloud 
remove_tags = ['clinton','trump','donald','election2016','hillary'] 
count_search_trump = Counter()
count_search_hillary = Counter()
count_hillary_tweets=0
count_donald_tweets=0
trump_cotags=[]
clinton_cotags=[]
for tweet in col.find():
    hashString=" ".join(term.lower() for term in (tweet['hashtags']))
    if any( word in hashString for word in trump_search_tags):
     count_donald_tweets +=1
     trump_terms = [term for term in (tweet['hashtags']) if term.lower() not in remove_tags ]
     if(len(trump_terms)>0):               
      trump_cotags.extend(trump_terms)
      count_search_trump.update(trump_terms)
    if any( word in hashString for word in clinton_search_tags):
     count_hillary_tweets +=1
     clinton_terms =  [term for term in (tweet['hashtags']) if term.lower() not in remove_tags ] 
     if(len(clinton_terms)>0):               
      clinton_cotags.extend(clinton_terms)                  
      count_search_hillary.update(clinton_terms)    
    
trump_total_tags = ' '.join( i for i in trump_cotags)
print(count_donald_tweets)#2222723

clinton_total_tags = ' '.join( i for i in clinton_cotags)
print(count_hillary_tweets)#438857   

twitter_mask = imread('./twitter_mask.png', flatten=True)


wordcloud = WordCloud(
                      font_path='CabinSketch-Bold.ttf',
                      stopwords=STOPWORDS,
                      background_color='white',
                      width=1800,
                      height=1400,
                      mask=twitter_mask
            ).generate(trump_total_tags)

plt.imshow(wordcloud)
plt.axis("off")
plt.savefig('./my_twitter_wordcloud_donald.png', dpi=300)
plt.show()