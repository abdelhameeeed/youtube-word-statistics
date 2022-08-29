#!/usr/bin/env python
# coding: utf-8

# In[1]:


from flask import Flask,request,render_template

import Utilities as utl  

app  = Flask(__name__)



@app.route('/' , methods = ['GET' , 'POST'])
def welcome_page():
    return render_template('index.html')


@app.route('/word_count' , methods = ['GET' , 'POST'] )
def word_count():
    url = request.args.get('url') 
    word = request.args.get('word')
    print( f"url is {url} and word is {word}")
    obj = utl.youtube_url_stats(url)
    word_count ,  percentage = obj.fetch_word_count(word) 
    random_sentence  = obj.fetch_random_sentence(word)
    
    return render_template( 'index.html', word_count = str(word_count) 
                           , percentage = str(percentage) 
                           , url = url 
                           , word = word 
                           , random_sentence = str(random_sentence) 
                             )



# In[ ]:



if __name__ == "__main__":
    app.run()


# In[ ]:




