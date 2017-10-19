"""Mines text from Project Gutenburg. Performs word frequency and sentiment analysis
on text and generates a word cloud from most common words.

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
    if not exists(file_name):
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
    Converts all words to lowercase. Returns a list of the words used in the string
    with stop words removed.

    Args:
        text: a string of text, such as the filtered text from a Project Gutenberg book

    Returns:
        a list of words, all lowercase, from the string with stop words removed
    """
    text = text.lower()
    word_list = text.split()

    for i in range(len(word_list)):
        word_list[i] = word_list[i].strip(string.punctuation)

    stop_words = get_stop_words('en')
    stop_words_2 = ["a", "about", "above", "across", "after", "afterwards", "again", "against", "all",
    "almost", "alone", "along", "already", "also", "although", "always", "am", "among", "amongst", "amoungst",
    "amount", "an", "and", "another", "any", "anyhow", "anyone", "anything", "anyway", "anywhere", "are",
    "around", "as", "at", "back", "be", "became", "because", "become", "becomes", "becoming", "been", "before",
    "beforehand", "behind", "being", "below", "beside", "besides", "between", "beyond", "bill", "both",
    "bottom", "but", "by", "call", "can", "cannot", "cant", "co", "con", "could", "couldnt", "cry", "de",
    "describe", "detail", "do", "done", "down", "due", "during", "each", "eg", "eight", "either", "eleven",
    "else", "elsewhere", "empty", "enough", "etc", "even", "ever", "every", "everyone", "everything",
    "everywhere", "except", "few", "fifteen", "fify", "fill", "find", "fire", "first", "five", "for",
    "former", "formerly", "forty", "found", "four", "from", "front", "full", "further", "get", "give", "go",
    "had", "has", "hasnt", "have", "he", "hence", "her", "here", "hereafter", "hereby", "herein", "hereupon",
    "hers", "herself", "him", "himself", "his", "how", "however", "hundred", "ie", "if", "in", "inc",
    "indeed", "interest", "into", "is", "it", "its", "itself", "keep", "last", "latter", "latterly", "least",
    "less", "ltd", "made", "many", "may", "me", "meanwhile", "might", "mill", "mine", "more", "moreover",
    "most", "mostly", "move", "much", "must", "my", "myself", "name", "namely", "neither", "never",
    "nevertheless", "next", "nine", "no", "nobody", "none", "noone", "nor", "not", "nothing", "now", "nowhere",
    "of", "off", "often", "on", "once", "one", "only", "onto", "or", "other", "others", "otherwise", "our",
    "ours", "ourselves", "out", "over", "own","part", "per", "perhaps", "please", "put", "rather", "re",
    "same", "see", "seem", "seemed", "seeming", "seems", "serious", "several", "she", "should", "show",
    "side", "since", "sincere", "six", "sixty", "so", "some", "somehow", "someone", "something", "sometime",
    "sometimes", "somewhere", "still", "such", "system", "take", "ten", "than", "that", "the", "their",
    "them", "themselves", "then", "thence", "there", "thereafter", "thereby", "therefore", "therein",
    "thereupon", "these", "they", "thick", "thin", "third", "this", "those", "though", "three", "through",
    "throughout", "thru", "thus", "to", "together", "too", "top", "toward", "towards", "twelve", "twenty",
    "two", "un", "under", "until", "up", "upon", "us", "very", "via", "was", "we", "well", "were", "what",
    "whatever", "when", "whence", "whenever", "where", "whereafter", "whereas", "whereby", "wherein",
    "whereupon", "wherever", "whether", "which", "while", "whither", "who", "whoever", "whole", "whom",
    "whose", "why", "will", "with", "within", "without", "would", "yet", "you", "your", "yours", "yourself",
    "yourselves", "the"]

    filtered_word_list = [word for word in word_list if word not in stop_words and word not in stop_words_2]

    return filtered_word_list


def get_histogram(word_list):
    """Takes a list of words as input and returns a dictionary with all the unique
    words and their word counts

    Args:
        word_list: a list of words (assumed to all be in lower case with no punctuation)

    Returns:
        a histogram; a dictionary with all the unique words and their word counts
    """
    word_counts = dict()

    for word in word_list:
        if word != '':
            word_counts[word] = word_counts.get(word, 0) + 1

    return word_counts


def get_top_n_words(word_list, n):
    """Takes a list of words as input and returns a list of the n most frequently
    occurring words ordered from most to least frequently occurring.

    Args:
        word_list: a list of words (assumed to all be in lower case with no punctuation)
        n: the number of words to return

    Returns:
        a list of n most frequently occurring words ordered from most to least frequently occurring
    """
    word_counts = get_histogram(word_list)

    ordered_by_frequency = sorted(word_counts, key=word_counts.get, reverse=True)

    return ordered_by_frequency[:n]


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
    wordcloud = WordCloud(width = 1000, height = 500, background_color="white").generate(text)
    wordcloud.to_file('%s_wf.png' % title)


if __name__ == "__main__":
    titles = ('Frankenstein',
                'Paradise_Lost',
                'The_Romance_of_Lust',
                )

    url = {'Frankenstein': 'http://www.gutenberg.org/cache/epub/84/pg84.txt',
            'Paradise_Lost': 'http://www.gutenberg.org/cache/epub/20/pg20.txt',
            'The_Romance_of_Lust': 'http://www.gutenberg.org/cache/epub/30254/pg30254.txt',
            }

    # for each title
    for title in titles:
        # get the text from url and strip the header comments
        text = filter_PG_text(get_cache(url['%s' % title], '%s.txt' % title))
        # get a list of the filtered words from the text
        word_list = get_word_list(text)
        # top n words
        n = 50
        # get a list of the top n words
        top_n_words = (get_top_n_words(word_list, n))
        # print the top n words
        print('Top %d Words in %s:' % (n, title))
        print(top_n_words, '\n')
        # print the sentiment of the top n words
        print('Sentiment of Top %d Words in %s:' % (n, title))
        print(sentiment_analyzer(top_n_words), '\n')
        # print the sentiment of the whole text
        print('Sentiment of %s:' % title)
        print(sentiment_analyzer(text), '\n\n')
        # generate a wordcloud with the filtered words from the text
        word_cloud(word_list, title)
