# -*- coding: utf-8 -*-
"""BDA.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1n0HDSlhUesjXBT3daRnaKUzcAA287XCe
"""

import tweepy
import pandas as pd
import matplotlib.pyplot as plt
import re
import spacy
nlp = spacy.load('en_core_web_lg')
import seaborn as sns

!python -m spacy download en_core_web_lg

consumer_key='hZb1UDr1PrjmNZOymldirg9zr' 
consumer_secret='K1qBAPAUjPG8h0qmlPehV9sO0dHT2raWPtdqatJauTZHw1jxt7'
access_token='1203193983196897280-hoqU2iEkoZVBJNLHH28ymGsTMoKE4c'
access_token_secret='OuyCBohL6i4vDazhQrNWpdWZy5c1cReX9N2pmGzDJWC9O'

auth = tweepy.OAuthHandler(consumer_key,consumer_secret)
auth.set_access_token(access_token,access_token_secret)
api=tweepy.API(auth)

# cursor = tweepy.Cursor(api.user_timeline,id='taylorswift13',tweet_mode="extended").items(1)

# cursor = tweepy.Cursor(api.search,q="mongodb",tweet_mode="extended").items(1)

# for i in cursor:
#   print(i.full_text)

number_of_tweets=200
 tweets=[]
 likes=[]
time=[]

for i in tweepy.Cursor(api.user_timeline,id='taylorswift13',tweet_mode="extended").items(number_of_tweets):
    tweets.append(i.full_text)
    likes.append(i.favorite_count)
    time.append(i.created_at)

# tweets

df=pd.DataFrame({'tweets':tweets,'likes':likes,'time':time})

df = df[~df.tweets.str.contains("RT")]

df=df.reset_index(drop=True)

df

mostlike = df.loc[df.likes.nlargest(9).index]

mostlike

#splitting the list of sentences into words
list_of_sentences = [sentence for sentence in df.tweets]

lines=[]
for sentence in list_of_sentences:
  words = sentence.split()
  for w in words:
    lines.append(w)

#Removing Punctuation

lines = [re.sub(r'[^A-Za-z0-9]+', '', x) for x in lines]

lines

lines2 = []

for word in lines:
    if word != '':
        lines2.append(word)

#This is stemming the words to their root
from nltk.stem.snowball import SnowballStemmer

# The Snowball Stemmer requires that you pass a language parameter
s_stemmer = SnowballStemmer(language='english')

stem = []
for word in lines2:
    stem.append(s_stemmer.stem(word))
    
stem

#Removing all Stop Words

stem2 = []

for word in stem:
    if word not in nlp.Defaults.stop_words:
        stem2.append(word)

stem2

df = pd.DataFrame(stem2)

df = df[0].value_counts()

#This is a simple plot that shows the top 20 words being used
#df.plot(20)

df = df[:20,]
plt.figure(figsize=(10,5))
sns.barplot(df.values, df.index, alpha=0.8)
plt.title('Top Words Overall')
plt.ylabel('Word from Tweet', fontsize=12)
plt.xlabel('Count of Words', fontsize=12)
plt.show()

def show_ents(doc):
    if doc.ents:
        for ent in doc.ents:
            print(ent.text + ' - ' + ent.label_ + ' - ' + str(spacy.explain(ent.label_)))

str1 = " " 
stem2 = str1.join(lines2)

stem2 = nlp(stem2)

label = [(X.text, X.label_) for X in stem2.ents]

df6 = pd.DataFrame(label, columns = ['Word','Entity'])

df7 = df6.where(df6['Entity'] == 'ORG')

df7 = df7['Word'].value_counts()

df = df7[:20,]
plt.figure(figsize=(10,5))
sns.barplot(df.values, df.index, alpha=0.8)
plt.title('Top Organizations Mentioned')
plt.ylabel('Word from Tweet', fontsize=12)
plt.xlabel('Count of Words', fontsize=12)
plt.show()

str1 = " " 
stem2 = str1.join(lines2)

stem2 = nlp(stem2)

label = [(X.text, X.label_) for X in stem2.ents]

df10 = pd.DataFrame(label, columns = ['Word','Entity'])

df10 = df10.where(df10['Entity'] == 'PERSON')

df11 = df10['Word'].value_counts()

df = df11[:20,]
plt.figure(figsize=(10,5))
sns.barplot(df.values, df.index, alpha=0.8)
plt.title('Top People Mentioned')
plt.ylabel('Word from Tweet', fontsize=12)
plt.xlabel('Count of Words', fontsize=12)
plt.show()