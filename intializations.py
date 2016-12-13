import re
import nltk
import os
import sys
import readline
import json
import datetime
import random
import wikipedia
import praw
from fuzzywuzzy import process

reload(sys)
sys.setdefaultencoding("utf-8")

## Initializing all tokenizers and taggers  ##
sent_tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')
word_tokenizer = nltk.tokenize.TreebankWordTokenizer()
tagger = nltk.data.load(nltk.tag._POS_TAGGER)

## neccesary lists of elements and grammars
qWords = ["what","who","why","when","how","whom","which","whenever","is","are","do","does","did","give","tell"]
replacements = {"'s": " is","'re": " are", "'nt": " not"}

grammar = r"""
        NP: {<NNP>+}
        QP: {<W.*>}
"""
parser = nltk.RegexpParser(grammar)

## list of stop words being used
stop = [u'all', u'just', u'being', u'over', u'both', u'through', u'yourselves',
     u'its', u'before', u'o', u'hadn', u'herself', u'll', u'had', u'should', u'to',
     u'only', u'won', u'under', u'ours', u'has', u'do', u'them', u'his', u'very',
      u'they', u'not', u'during', u'now', u'him', u'nor', u'd', u'did', u'didn',
      u'this', u'she', u'each', u'further', u'where', u'few', u'because', u'doing',
       u'some', u'hasn', u'are', u'our', u'ourselves', u'out', u'for', u'while',
       u're', u'does', u'above', u'between', u'mustn', u't', u'be', u'we', u'who', u'were',
       u'here', u'shouldn', u'hers', u'by', u'on', u'about', u'couldn', u'of',
       u'against', u's', u'isn', u'or', u'own', u'into', u'yourself', u'down', u'mightn',
        u'wasn', u'your', u'from', u'her', u'their', u'aren', u'there', u'been',
         u'too', u'wouldn', u'themselves', u'weren', u'was', u'until', u'more', u'himself',
          u'that', u'but', u'don', u'with', u'than', u'those', u'he', u'me', u'myself',
           u'ma', u'these', u'up', u'will', u'below', u'ain', u'can', u'theirs', u'my',
           u'and', u've', u'then', u'is', u'am', u'it', u'doesn', u'an', u'as', u'itself',
            u'at', u'have', u'in', u'any', u'if', u'again', u'no', u'same', u'other',
             u'you', u'shan', u'needn', u'haven', u'after', u'most', u'such', u'a', u'off',
              u'i', u'm', u'yours', u'so', u'y', u'the', u'having', u'once']

# Reddit API initializations

my_user_agent = 'ubuntu16.04:com.example.myredditapp:v1.2.3 (by /u/vshan)'
my_client_id = 'zqyYfR04L0AcSA'
my_client_secret = 'Q9rfrUdoJ5iqZwGZ4Wc-Am0oXJE'
my_username = 'vshan'
my_password = 'ashandpikaftw14'

reddit = praw.Reddit(user_agent=my_user_agent,
                     client_id=my_client_id,
                     client_secret=my_client_secret,
                     username=my_username,
                     password=my_password)

subreddit = reddit.subreddit('askreddit')
