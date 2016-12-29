# -*- coding: utf-8 -*-
"""
Created on Fri Dec 02 00:13:35 2016

@author: bus-superbowl
"""
import pymongo
import pandas

destIP = "155.97.56.145"# server 7           
col =  pymongo.MongoClient(destIP,27017)["tweets"]["elections.test.1"]
col.count()
    

d = []
for tweet in col.aggregate([ {"$sample": { "size": 500 } } ]):
 if tweet["lang"] in "en":
    d.append({'id':  "'"+ str(tweet["id"]), 'text': tweet["text"],})

df = pandas.DataFrame(d)

df.to_excel('tweet4.xlsx', sheet_name='sheet1', index=False)



 
for tweet in col.aggregate([ {"$sample": { "size": 250 } } ]):
 if tweet["lang"] in "en":
  print (tweet["text"])

for tweet in col.find({'text': {'$exists': True}, '$where': "this.name.length > 40"}).limit(2): 
 print (tweet["text"])
