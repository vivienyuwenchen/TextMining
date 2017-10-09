"""Mines text from Project Gutenburg. Performs TF-IDF and sentiment analysis
on text and generates a word cloud from most important words.

@author: Vivien Chen

"""

import requests
import string
import math
from pickle import dump, load
from os.path import exists
from stop_words import get_stop_words       # pip install stop_words
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from wordcloud import WordCloud             # pip install wordcloud
from textblob import TextBlob as tb         # pip install textblob


def get_cache(url, file_name):
    """Writes text from url into file_name and returns text if file_name does not exist.
    Otherwise, simply returns text from file_name. Assumes that text from file_name
    matches text from url if file_name exists.

    Args:
        url: url you want to read text from
        file_name: name of file you want to write to/read from

    Returns:
        text from url
    """
    if exists(file_name) == False:
        file_ = open(file_name, 'wb')
        text = requests.get(url).text
        dump(text, file_)

    return open(file_name, 'r', encoding='utf-8', errors='ignore')


def filter_PG_text(text):
    """Takes the raw text of a Project Gutenberg book as input. Strips away header
    comments and returns the book portion of the text.

    Args:
        text: the raw text from a Project Gutenberg book

    Returns:
        the book portion of the Project Gutenberg book
    """
    lines = text.readlines()

    start_line = 0
    while lines[start_line].find('START OF THIS PROJECT GUTENBERG EBOOK') == -1:
        start_line += 1
    lines = lines[start_line+1:]

    end_line = 0
    while lines[end_line].find('END OF THIS PROJECT GUTENBERG EBOOK') == -1:
        end_line += 1
    lines = lines[:end_line-3]

    return ' '.join(lines)


def get_word_list(text):
    """Takes a string of text as input. Strips away punctuation and whitespace.
    Converts all words to lowercase. Returns a list of the words used in the string.

    Args:
        text: a string of text, such as the filtered text from a Project Gutenberg book

    Returns:
        a list of words, all lowercase, from the string
    """
    text = text.lower()
    text = text.split()
    for i in range(len(text)):
        text[i] = text[i].strip(string.punctuation)

    return text


def get_histogram(word_list):
    """Takes a list of words as input and returns a dictionary with all the unique
    words and their word counts with stop words removed.

    Args:
        word_list: a list of words (assumed to all be in lower case with no punctuation)

    Returns:
        a histogram; a dictionary with all the unique words and their word counts
    """
    word_counts = dict()
    stop_words = get_stop_words('en')

    for word in word_list:
        if word not in stop_words and word != '':
            word_counts[word] = word_counts.get(word, 0) + 1

    return word_counts


def get_top_n_words(word_list, n):
    """Takes a list of words as input and returns a string of the n most frequently
    occurring words, adjusted for the number of times each word occurs, ordered from
    most to least frequently occurring.

    Args:
        word_list: a list of words (assumed to all be in lower case with no punctuation)
        n: the number of words to consider

    Returns:
        a string of n most frequently occurring words, adjusted for the number of times
        each word occurs, ordered from most to least frequently occurring
    """
    word_counts = get_histogram(word_list)

    ordered_by_frequency = sorted(word_counts, key=word_counts.get, reverse=True)
    ordered_by_frequency = ordered_by_frequency[0:n]

    list_ = []
    for word in ordered_by_frequency:
        list_.append((word + ' ') * word_counts[word])

    return ' '.join(list_)


def sentiment_analyzer(text):
    """Takes a string of text as input and returns the sentiment analysis of the text.
    Converts text to string if text is not already a string.

    Args:
        text: a string of text to be analyzed

    Returns:
        a sentiment analysis of the text
    """
    if type(text) != str:
        text = ' '.join(text)
    analyzer = SentimentIntensityAnalyzer()
    return analyzer.polarity_scores(text)


def word_cloud(text, title):
    """Takes a string of text and a title as input and saves the generated wordcloud as a png
    with the title as the file name. Converts text to string if text is not already a string.

    Args:
        text: a string of text used to generate a wordcloud
        title: the file name of the generated wordcloud

    Returns:
        nothing; saves the wordcloud to title.png
    """
    if type(text) == list:
        text = ' '.join(text)
    wordcloud = WordCloud(width = 1000, height = 500, background_color="black").generate(text)
    wordcloud.to_file('%s_tfidf.png' % title)


def tfidf(word, text, text_list):
    """Calculates and returns the TF-IDF score of a word from the text by computing
    the TF score from the text and the IDF score from all the texts combined.

    Args:
        word: a given word from the text
        text: a string of text from which the TF-IDF score of each word is calculated
        text_list: a list of all the texts to compare with

    Returns:
        the TF-IDF score of a word from the text
    """
    tf = text.words.count(word) / len(text.words)
    n_containing = sum(1 for text in text_list if word in text.words)
    idf = math.log(len(text_list) / (1 + n_containing))
    return tf * idf


if __name__ == "__main__":
    titles = ('Frankenstein',
                'Paradise_Lost',
                'The_Romance_of_Lust',
                )

    url = {'Frankenstein': 'http://www.gutenberg.org/cache/epub/84/pg84.txt',
            'Paradise_Lost': 'http://www.gutenberg.org/cache/epub/20/pg20.txt',
            'The_Romance_of_Lust': 'http://www.gutenberg.org/cache/epub/30254/pg30254.txt',
            }

    text_list = []

    for title in titles:
        text = filter_PG_text(get_cache(url['%s' % title], '%s.txt' % title))
        text_list.append(tb(get_top_n_words(get_word_list(text), 500)))

    list_ = [[],[],[]]
    n = 50

    for i, text in enumerate(text_list):
        print('Top %d words in %s with TF-IDF Scores:' % (n, titles[i]))
        scores = {word: tfidf(word, text, text_list) for word in text.words}
        sorted_words = sorted(scores.items(), key=lambda x: x[1], reverse=True)
        for word, score in sorted_words[:n]:
            print('\tWord: {}, TF-IDF: {}'.format(word, round(score, 10)))
            list_[i].append(word)
        print('')

    print('')

    for i, title in enumerate(titles):
        text = filter_PG_text(get_cache(url['%s' % title], '%s.txt' % title))
        print('Top %d Words in %s:' % (n, title))
        print(list_[i], '\n')
        print('Sentiment of Top %d Words in %s:' % (n, title))
        print(sentiment_analyzer(list_[i]), '\n')
        print('Sentiment of %s:' % title)
        print(sentiment_analyzer(text), '\n\n')
        word_cloud(list_[i], title)
