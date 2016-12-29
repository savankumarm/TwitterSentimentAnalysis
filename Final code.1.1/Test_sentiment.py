# -*- coding: utf-8 -*-
"""
Created on Wed Dec 14 15:13:48 2016

@author: Savan Kumar
"""
import re
import nltk
from nltk.corpus import stopwords
import html
import string
from nltk.stem import PorterStemmer

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
stop = stopwords.words('english')+ [u'rt', u'via',u'The',u'', u'...',u'htt']  # + punctuation  
ps = PorterStemmer()
def getFeatureVector(tweet):
  featureVector = []
  tweet=tweet.encode("utf-8")
  tweet=tweet.decode('unicode_escape').encode('ascii','ignore')
  words = tweet.split()
#  words = word_tokenize(tweet)
  for w in words:
    w=w.decode('unicode_escape')
    #ignore if it is a stop word or length less than 3
    if(w in stop or len(w)<3):
        continue
    else:
        #w= ps.stem(w)
        featureVector.append(w.lower())
  return featureVector 
 #-----------------------Mass Feature extractions-------------------------------------------------------- 
from openpyxl import load_workbook
import pickle
import random 

wb = load_workbook(filename='C:/Users/bus-superbowl/Desktop/Python scripts/hereyougo/ElectionFinal-143-p-215n.xlsx', read_only=False)
ws = wb['sheet1']

rawTweets = []

rtrainData =[]
rtestData = []
count = 0
 #Approach 2 Randomise
     #and (row[2].value !=0)
for row in ws.rows:
    if((row[0].value != None) and (row[2].value !=0)and((row[0].value != 'id'))):
     rsentiment = row[2].value
     rtweet = row[1].value
     rId = row[0].value
     rawTweets.append((rId,rtweet, rsentiment))
    if(row[0].value== None):
      break
  
print (len(rawTweets))   
random.shuffle(rawTweets)     

rtrainData = rawTweets[:250]
rtestData = rawTweets[250:] 
print (len(rtrainData))
print (len(rtestData))
#election final total 362 neg 250 pos 112

pos = 0
neg= 0
neu =0
for row in rawTweets:
     if(row[2] == 0):
       neu+=1
     elif(row[2] == 1):
       pos+=1
     elif(row[2] == -1):
       neg+=1
print (neu) #
print (pos) #142   
print (neg) #188
#electionfinal2 pos 111 neg 250
print (len(rtestData)) #112
print (len(rtrainData)) #250

pos = 0 
neg= 0
for (i,t,s) in rtestData:
 if(s== -1):
    neg+=1
 elif(s == 1):
    pos+=1   
print (pos) #40
print (neg) #68


pos = 0
neg= 0
negTweets=[]
posTweets=[]
for (i,t,s) in rtrainData:
 if(s== -1):
    negTweets.append((i,t, s))  
    neg+=1
 elif(s == 1):
    posTweets.append((i,t, s))  
    pos+=1   
print (pos) #103
print (neg) #147

def getFeatureList_Vector(rawTweets):
 tweets= []
 featureList = []
 for rawTweet in rawTweets:
     sentiment = rawTweet[2]
     tweet = rawTweet[1]
     processedTweet = processTweet(tweet)
     featureVector = getFeatureVector(processedTweet)
     featureList.extend(featureVector)
     tweets.append((featureVector, sentiment))
 return featureList,tweets


TrFeatureList,trainData= getFeatureList_Vector(rtrainData)
len(trainData)

TeFeatureList,testData= getFeatureList_Vector(rtestData)
len(testData)


#top20 neg words
negTrFeatureList,negtrainData= getFeatureList_Vector(negTweets)
negfeatureFreqList = nltk.FreqDist(negTrFeatureList).most_common(20)
print(negfeatureFreqList)

#top20 pos words
posTrFeatureList,postrainData= getFeatureList_Vector(posTweets)
posfeatureFreqList = nltk.FreqDist(posTrFeatureList).most_common(20)
print(posfeatureFreqList)

ToFeatureList= TrFeatureList+TeFeatureList
#find the frequency list for train and test
featureFreqList = nltk.FreqDist(ToFeatureList).most_common(2000)
#print(featureFreqList)
topFreqfeatureList = [i[0] for i in featureFreqList]
#print(topFreqfeatureList)

def extract_features(document):
	    document_words = set(document)
	    features = {}
	    for word in topFreqfeatureList:
	        features['contains(%s)' % word] = (word in document_words)
	    return features
     
def find_features(text):
        processedTweet = processTweet(text)
        featureVector = getFeatureVector(processedTweet)
        features = {}
        for word in topFreqfeatureList:
          features['contains(%s)' % word] = (word in featureVector)
        return features
     
training_set = nltk.classify.apply_features(extract_features, trainData)
testing_set = nltk.classify.apply_features(extract_features, testData)

train_set = rtrainData
#testing_set = testData
# with neutral 0.448
test_truth   = [s for (t,s) in testing_set]
test_predict = [classifier.classify(t) for (t,s) in testing_set]

classifier = nltk.NaiveBayesClassifier.train(training_set)

#save_NB = open("NB.pickle","wb")
#pickle.dump(classifier, save_NB)
#save_NB.close()
#classifier.show_most_informative_features(32)
print("NaiveBayesClassifier accuracy percent:",(nltk.classify.accuracy(classifier, testing_set))*100)
print ('Confusion Matrix')
print (nltk.ConfusionMatrix( test_truth, test_predict ))

#----------------------------------variations of NB for imporoved accuracy
from nltk.classify.scikitlearn import SklearnClassifier
from sklearn.naive_bayes import MultinomialNB,BernoulliNB
from sklearn.linear_model import LogisticRegression, SGDClassifier
from sklearn.svm import SVC, LinearSVC, NuSVC



print (nltk.ConfusionMatrix( test_truth, test_predict ))
MNB_classifier = SklearnClassifier(MultinomialNB())
MNB_classifier.train(training_set)
print("MultinomialNB accuracy percent:",(nltk.classify.accuracy(MNB_classifier, testing_set))*100)
# 0.46400000000000002 neutral
BNB_classifier = SklearnClassifier(BernoulliNB())
BNB_classifier.train(training_set)
print("BernoulliNB accuracy percent:",(nltk.classify.accuracy(BNB_classifier, testing_set))*100)
# neutral 0.38
LogisticRegression_classifier = SklearnClassifier(LogisticRegression())

#save_LogisticRegression = open("LogisticRegression.pickle","wb")
#pickle.dump(LogisticRegression_classifier, save_LogisticRegression)
#save_LogisticRegression.close()

LogisticRegression_classifier.train(training_set)
print("LogisticRegression_classifier accuracy percent:", (nltk.classify.accuracy(LogisticRegression_classifier, testing_set))*100)
test_predict = [LogisticRegression_classifier.classify(t) for (t,s) in testing_set]
print (nltk.ConfusionMatrix( test_truth, test_predict ))
# 45.60 neutral 
SGDClassifier_classifier = SklearnClassifier(SGDClassifier())
SGDClassifier_classifier.train(training_set)
print("SGDClassifier_classifier accuracy percent:", (nltk.classify.accuracy(SGDClassifier_classifier, testing_set))*100)
#41.19 neutral 
SVC_classifier = SklearnClassifier(SVC())
SVC_classifier.train(training_set)
print("SVC_classifier accuracy percent:", (nltk.classify.accuracy(SVC_classifier, testing_set))*100)
#36.79 neutral 
LinearSVC_classifier = SklearnClassifier(LinearSVC())
LinearSVC_classifier.train(training_set)
print("LinearSVC_classifier accuracy percent:", (nltk.classify.accuracy(LinearSVC_classifier, testing_set))*100)
#40.40 neutral 

test_predict = [MNB_classifier.classify(t) for (t,s) in testing_set]
print ('Confusion Matrix')
print (nltk.ConfusionMatrix( test_truth, test_predict ))
#NuSVC_classifier = SklearnClassifier(NuSVC())
#NuSVC_classifier.train(training_set)
#
#print("NuSVC_classifier accuracy percent:", (nltk.classify.accuracy(NuSVC_classifier, testing_set))*100)

#test_predict = [NuSVC_classifier.classify(t) for (t,s) in testing_set]
#print nltk.ConfusionMatrix( test_truth, test_predict )

#MultinomialNB accuracy percent: 70.3703703704
#BernoulliNB accuracy percent: 71.2962962963
#LogisticRegression_classifier accuracy percent: 75.0
#SGDClassifier_classifier accuracy percent: 69.4444444444
#SVC_classifier accuracy percent: 62.962962963
#LinearSVC_classifier accuracy percent: 74.0740740741


#Test the results
testTweet = u"RT @BADPEOPLEMOVIE: Crazy ride we all are on right now. #DemsInPhilly #RNCinCLE #badpeople 😈😈😈 #RETWEET to #SupportIndieFilm &amp; #reason. htt…"

testTweet1 = u"RT @tedcruz: If we stand together and choose freedom our future will be brighter. We can do this. #RNCinCLE"


result =[]
for test in rtestData:
   testTweet = test[1]
   processedTestTweet = processTweet(testTweet)
   outcome = LogisticRegression_classifier.classify(extract_features(getFeatureVector(processedTestTweet)))
   dist = LogisticRegression_classifier.prob_classify(extract_features(getFeatureVector(processedTestTweet)))
   if(outcome!=test[2]):
    result.append({'predicted':outcome,'actual':test[2],'text':testTweet,'pos_prob':dist.prob(1),'neg_prob':dist.prob(-1)})
   
   
   result
   

from textblob import TextBlob

textBlobResult =[]
for test in rtestData:
   testTweet = test[1]
   processedTestTweet = processTweet(testTweet)
   testimonial = TextBlob(processedTestTweet)
   pol = testimonial.sentiment.polarity
   if (pol>0):
    outcome =1
   elif(pol<0):
    outcome =- 1
   elif(pol==0):
    outcome = 0
   textBlobResult.append({'predicted': outcome, 'actual':test[2],'text': processedTestTweet})
   
   
   
rawTweets
clean =[]
for raw in rawTweets:
   testTweet = raw[1]
   processedTestTweet = processTweet(testTweet)
   clean.append({'Id': raw[0], 'actual':raw[2],'text': processedTestTweet})
 

import pandas 
df = pandas.DataFrame(result)
 
df.to_excel("cleaned_labels.xlsx", sheet_name='sheet1', index=False)  
#confidence

import pymongo

db_connect = pymongo.MongoClient()
database_name = 'tweets'
database = db_connect[database_name]
collection = database.collection_names(include_system_collections=False)
for collect in collection:
    print (collect)

#elections.step1.1
#elections.test.1
#elections.step2
#elections.v1
#elections.step1
database['elections.step1'].count()#2505617

database['elections.step1.1'].count()#2504277


col =  pymongo.MongoClient()["tweets"]["elections.test.1"]
col.count()
result=[]
for tweet in col.find():
   tweetText= tweet["text"] 
   tweetId= tweet["id"] 
   processedTestTweet = processTweet(tweetText)
   outcome = LogisticRegression_classifier.classify(extract_features(getFeatureVector(processedTestTweet)))
   dist = LogisticRegression_classifier.prob_classify(extract_features(getFeatureVector(processedTestTweet)))
  # result.append({'predicted':outcome,'text':processedTestTweet,'pos_prob':dist.prob(1),'neg_prob':dist.prob(-1)})
   col.update_one({
      'id': tweetId
    },{
      '$set': {
        'predicted': outcome,
        'pos_prob': dist.prob(1),
        'neg_prob':dist.prob(-1)
      }
    }, upsert=False)




for tweet in col.find({"predicted":{'$ne': None}}):
   print (tweet["predicted"] )
   print (tweet["pos_prob"])

col.find({"predicted":-1}).count()#1974039
col.find({"predicted":1}).count()#572660

neutral 803209
neutral 1469703
neutral 273787     

neu_count =0
neg_count =0
pos_count =0
for tweet in col.find():
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

   terms_hash = 

    dates_timline1.append(tweet['created_ts'])
   elif any(("clinton" or"hillary") in s.lower() for s in terms_hash):
    dates_timline2.append(tweet['created_ts'])
from sklearn.feature_extraction.text import CountVectorizer
count_vect = CountVectorizer()
X_train_counts = count_vect.fit_transform(test[1] for test in rtestData)
X_train_counts.shape


from sklearn.feature_extraction.text import TfidfTransformer
tf_transformer = TfidfTransformer(use_idf=False).fit(X_train_counts)
X_train_tf = tf_transformer.transform(X_train_counts)
X_train_tf.shape


tfidf_transformer = TfidfTransformer()
X_train_tfidf = tfidf_transformer.fit_transform(X_train_counts)
X_train_tfidf.shape

