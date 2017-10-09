# TextMining

This is the base repo for the text mining and analysis project for Software Design at Olin College.

[Project Writeup and Reflection](https://github.com/vivienyuwenchen/TextMining/blob/master/Project%20Writeup%20and%20Reflection.md)

Required packages:
- pip install nltk requests vaderSentiment
- pip install stop_words
- pip install wordcloud
  - might have to install Microsoft Visual C++ 2015, in which case there will be an error message with a link to the download page
- pip install textblob

To run the text mining code with word frequency analysis:
- python text_mining.py

To run the text mining code with TF-IDF:
- python text_mining_tfidf.py
