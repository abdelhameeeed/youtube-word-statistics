#!/usr/bin/env python
# coding: utf-8

# In[31]:


from youtube_transcript_api import YouTubeTranscriptApi
import re
import nltk
from collections import Counter
import itertools
from nltk.corpus import stopwords
# import string 
import pafy
import random

# !pip install youtube-dl
# !pip install git+https://github.com/Cupcakus/pafy

# nltk.download('omw-1.4')

class youtube_url_stats:
    
    def __init__(self , url  ):
        self.url = url 
        id = self.fetch_id( url  ) 
        self.subtitles = self.fetch_trasncripts( id )
        
    def fetch_id(self , url , ues_pafy = False ):
        if ues_pafy == True:
            return pafy.new(url).videoid
        return re.search("(v=)(.*)(&)", url).groups()[1] 
    
    def fetch_trasncripts(self , id ):
        return YouTubeTranscriptApi.get_transcript( id , languages=['en'])  
    
    def fetch_word_count(self , word ):
        
        lines = [  i['text'] for i in self.subtitles ]
        # generate tokens
        nltk_tokens = [ nltk.word_tokenize(line) for line in lines ]
        words = list(itertools.chain(*nltk_tokens))
        words = [ word.lower() for word in words ]
        frequency = Counter( words )
        return frequency[word.lower()] , frequency[word.lower()] / sum(list(frequency.values())) 
    
    def fetch_random_sentence(self , word ):
        
        lines = [''] + [i['text'] for i in self.subtitles] + ['']
        
        lines = [  lines[i-1] + ' ' + lines[i] + ' ' +lines[i+1] for i in range( 0 , len(lines ) ) if word in lines[i] ]
        if len(lines) == 0 : 
            return None 
        
        return lines[random.choice(range(0, len(lines)))].strip()

    def most_least_frequent_words(self):
        
        lines = [  i['text'] for i in self.subtitles ]
        #Stop words.
        stop_words = set(stopwords.words('english'))
        stop_words.add('na')
        stop_words.add('gon')
        stop_words.add('youre')
        stop_words.add('im')
        stop_words.add('dont')
        stop_words.add('got')
        stop_words.add('go')
        stop_words.add('thats')
        # remove punctuation 
        lines = [ line.translate(str.maketrans( '' , '' , string.punctuation) )  for line in lines ]
        # generate tokens
        nltk_tokens = [ nltk.word_tokenize(line) for line in lines ]
        # change to lowercase and remove stop words.
        nltk_tokens_filtered = [ word for line in nltk_tokens for word in line if not word.lower() in stop_words ]
        frequency = Counter( nltk_tokens_filtered )
        return frequency.most_common(5),list(reversed(frequency.most_common()))[0:5]
    
    def some_stats(self):
        
        """
        returns more info about the video.
        """
        video = pafy.new(self.url)
        return video 
        



