# Project Writeup and Reflection

### Project Overview [Maximum 100 words]

*What data source(s) did you use and what technique(s) did you use analyze/process them? What did you hope to learn/create?*

For this project, I wanted to compare the word frequency and sentiment of novels with very different genres. I pickled the novels from Project Gutenberg and performed word frequency analysis on each of them after filtering out stop words [1, 2]. I performed sentiment analysis for the most common words in each novel as well as for the entire novel. Then I created a word cloud [3] of the most common words. In my second iteration, I implemented TF-IDF features [4] in order to compare the "most important words" of each novel. I also performed sentiment analysis and created a word cloud for those words.

From this project, I hoped to learn more about parsing and storing text from the Internet, using dictionaries, creating functions, applying different computational methods to compare my text, implementing relevant libraries, and figuring out how to use those libraries for my purposes. I also wanted to compare the results of using word frequency analysis and TF-IDF.

### Implementation [~2-3 paragraphs]

*Describe your implementation at a system architecture level. You should NOT walk through your code line by line, or explain every function (we can get that from your docstrings). Instead, talk about the major components, algorithms, data structures and how they fit together. You should also discuss at least one design decision where you had to choose between multiple alternatives, and explain why you made the choice you did.*

I began with a simple word frequency analyzer. This consisted of three parts: grab the text from a url and store it in a cache, filter the text (strip away header comments, punctuation, etc.) and return individual words in a list, and find the frequency of each unique word and sort the words by frequency. This could have been done with three functions or even less, but I thought it would give me more room to play with the code in the future if I split the functions as I did. With the main portion done, I added a sentiment analyzer and a word cloud generator to obtain visual data.

At first, I manually plugged in the title and url of each novel I wanted to analyze, but eventually I made a tuple with all the titles and a dictionary that matched the title with its url. I used placeholders for the title and number of words to analyze to minimize the manual work when I wanted to analyze a different text and use a different word count. Because I tested my code as a whole at each stage instead of writing doctests, I ran the frequency analyzer, sentiment analyzer, and word cloud functions from the main code instead of writing another function to run them.

There were many instances in which I had to decide on the data structure to use. I decided to use a dictionary for the histogram because it would match each unique word with its word count. In turn, I decided to return a word list after filtering the text because it would be easier to find the frequency of each unique word in a list with a dictionary. However, sentiment analyzer and word count required the input to be a string, so I added a conditional to those functions that would convert the input to a string if it were originally a list. Most of my decisions were made based on how little I needed to change the code to make it work. Since I implemented a lot of libraries, which I decided to do because the details of those functions I felt were outside the scope of this project, I chose to treat each one as a black box and figure out how to work around it instead of mess too much with it.

At some point, while I was still fixing up the word frequency analysis script, I decided to try to implement TF-IDF. I considered importing the functions from the original file I was working with, but I didn't want to mess anything up by accident, so I copied over what I had into another file. Googling led me to a very helpful tutorial [4], which I used as reference to write a function to calculate the TF-IDF score. I very much wanted the rest of my code to stay as close to the original as possible, but calculating the TF-IDF scores for every word in the entire text proved too time-consuming. I left the code running for over an hour before deciding that it wasn't worth the time. I went back and changed the get_top_n_words function to output a string with the top n words scaled for the number of times each word occurs (e.g. 'three three three' if the word 'three' appears three times). Then I used that to calculate the TF-IDF scores. It still took a while, but definitely not as long as before for it to be worth figuring out how to make the code run faster. Finally, I changed the outputs to show the top words, sentiment, and word cloud for the text based on the TF-IDF scores.

### Results [~2-3 paragraphs + figures/examples]

*Present what you accomplished:*
- *If you did some text analysis, what interesting things did you find? Graphs or other visualizations may be very useful here for showing your results.*
- *If you created a program that does something interesting (e.g. a Markov text synthesizer), be sure to provide a few interesting examples of the program’s output.*

I compared three novels: Frankenstein, Paradise Lost, and The Romance of Lust. Essentially, as a "feel-good" novel, The Romance of Lust is overall the most positive and the least negative. Even calculated with the top 50 words (using either word frequency analysis or TF-IDF), The Romance of Lust contains the highest positive score. On the other end of the spectrum, Frankenstein is the most negative, which makes sense because it's of a depressing horror genre. Meanwhile, Paradise Lost is the most neutral, not falling into either extreme of erotica or horror.

In terms of the comparison between word frequency analysis and TF-IDF, each has its pros and cons. Word frequency analysis is significantly easier to implement than TF-IDF and hard-coding a list or two of known stop words weeds out most of the irrelevant words. TF-IDF, however, generates words very unique to each text by comparing their appearance in other texts. As a result, the top 50 words and resulting word cloud generated with TF-IDF are much more exciting to look at than those generated with word frequency analysis. However, depending on how you calculate the TF-IDF score, the algorithm can often overlook motifs of a text that offhandedly appear in other texts. For example, "man", "life", and "father" are very important words in Frankenstein, but as they are words common to most other texts, they are deemed less important in TF-IDF and don't show up in the top 50 words.

One interesting thing to note: with TF-IDF, the compound score, or sentiment intensity, for each novel also has more variety. Frankenstein, in particular, has a compound score of -0.7184, showing that it is indeed uniquely depressing in its genre (top words include "miserable", "misery", "despair", "horror", "tears", and "grief", just like my life).

The top 50 words, sentiments, and word clouds for each novel are included below.

Also, going totally off topic: if you pickle the HTML text from https://google.com and open the .txt file, the encoded characters are a hodgepodge of questionable Chinese characters and radioactive symbols. If you copy it into Google translate and try to translate it into English, you end up with more repeating Chinese characters as well as gems such as:

- "This item is eligible for Free International Shipping This item is eligible for Free International Shipping This item is eligible for Free International Shipping This item is eligible for Free International Shipping Important information about purchasing this product: This product is out of print and no longer available from the publisher Related promotions"
- "The King of Cream is a kind of a cup of coffee and a cup of rice and a cup of rice."
- "In this case, you will not be able to do so. If you have any questions, please do not hesitate to do so. If you have any questions, please do not hesitate to contact us."
- "The United States of America" x100

**Overall**

Sentiment of Frankenstein:

- {'neg': 0.139, 'neu': 0.7, 'pos': 0.162, 'compound': 1.0}

Sentiment of Paradise_Lost:

- {'neg': 0.12, 'neu': 0.724, 'pos': 0.157, 'compound': 1.0}

Sentiment of The_Romance_of_Lust:

- {'neg': 0.089, 'neu': 0.707, 'pos': 0.204, 'compound': 1.0}

**Computed Using Word Frequency Analysis**

Top 50 Words in Frankenstein:

- ['man', 'life', 'father', 'shall', 'eyes', 'said', 'time', 'saw', 'night', 'elizabeth', 'mind', 'day', 'felt', 'death', 'heart', 'feelings', 'thought', 'dear', 'soon', 'friend', 'passed', 'miserable', 'heard', 'like', 'love', 'place', 'little', 'human', 'appeared', 'clerval', 'misery', 'friends', 'justine', 'country', 'nature', 'words', 'cottage', 'feel', 'great', 'old', 'away', 'hope', 'felix', 'return', 'happiness', 'know', 'despair', 'days', 'voice', 'long']

Sentiment of Top 50 Words in Frankenstein:

- {'neg': 0.169, 'neu': 0.492, 'pos': 0.339, 'compound': 0.9201}

![Frankenstein WF Word Cloud](https://github.com/vivienyuwenchen/TextMining/blob/master/Frankenstein_wf.png)

Top 50 Words in Paradise_Lost:

- ['thir', 'thy', 'thou', 'thee', "heav'n", 'shall', 'th', 'god', 'earth', 'man', 'high', 'great', 'death', 'till', 'hath', 'hell', 'stood', 'day', 'good', 'like', 'things', 'night', 'light', 'farr', 'love', 'eve', 'o', 'world', 'adam', 'soon', 'let', 'hee', 'son', 'life', 'know', 'place', 'long', 'forth', 'self', 'mee', 'ye', 'way', 'power', 'hand', 'new', 'deep', 'end', 'fair', 'men', 'satan']

Sentiment of Top 50 Words in Paradise_Lost:

- {'neg': 0.122, 'neu': 0.573, 'pos': 0.305, 'compound': 0.8957}

![Paradise Lost WF Word Cloud](https://github.com/vivienyuwenchen/TextMining/blob/master/Paradise_Lost_wf.png)

Top 50 Words in The_Romance_of_Lust:

- ['prick', 'dear', 'time', 'delicious', 'cunt', 'said', 'little', 'oh', 'aunt', 'hand', 'miss', 'way', 'pleasure', 'doctor', 'shall', 'quite', 'long', 'night', 'head', 'delight', 'took', 'great', 'excited', 'bed', 'felt', 'day', 'away', 'gave', 'let', 'told', 'lay', 'mrs', 'arms', 'mamma', 'fuck', 'frankland', 'soon', 'room', 'mother', 'clitoris', 'came', 'boy', 'exquisite', 'come', 'moment', 'lips', 'darling', 'began', 'mouth', 'course']

Sentiment of Top 50 Words in The_Romance_of_Lust:

- {'neg': 0.141, 'neu': 0.501, 'pos': 0.358, 'compound': 0.9548}

![The Romance of Lust WF Word Cloud](https://github.com/vivienyuwenchen/TextMining/blob/master/The_Romance_of_Lust_wf.png)

**Computed Using TF-IDF**

Top 50 Words in Frankenstein:

- ['elizabeth', 'feelings', 'miserable', 'sometimes', 'clerval', 'misery', 'friends', 'justine', 'country', 'several', 'cottage', 'felix', 'despair', 'scene', 'horror', 'creature', 'ice', 'affection', 'months', 'countenance', 'soul', 'possessed', 'geneva', 'mountains', 'journey', 'forever', 'hours', 'around', 'believe', 'discovered', 'resolved', 'remained', 'tale', 'cold', 'tears', 'sensations', 'existence', 'family', 'monster', 'appearance', 'companion', 'arrived', 'letter', 'read', 'science', 'girl', 'grief', 'endeavoured', 'wind', 'beauty']

Sentiment of Top 50 Words in Frankenstein:

- {'neg': 0.257, 'neu': 0.571, 'pos': 0.171, 'compound': -0.7184}

![Frankenstein TF-IDF Word Cloud](https://github.com/vivienyuwenchen/TextMining/blob/master/Frankenstein_tfidf.png)

Top 50 Words in Paradise_Lost:

- ['thir', 'thou', 'thee', "heav'n", 'th', 'though', "'d", 'o', 'till', 'hath', 'hell', 'things', 'farr', 'eve', 'adam', 'hee', 'self', 'mee', 'ye', 'fair', 'call', 'satan', 'gods', 'hast', 'paradise', "heav'ns", 'onely', 'spake', 'wide', 'fruit', 'bright', 'least', 'oft', 'angel', 'thence', 'warr', 'tree', 'works', 'behold', 'taste', 'seat', 'king', 'ere', 'angels', 'throne', 'created', 'eternal', 'divine', "heav'nly", 'fall']

Sentiment of Top 50 Words in Paradise_Lost:

- {'neg': 0.073, 'neu': 0.687, 'pos': 0.24, 'compound': 0.8555}

![Paradise Lost TF-IDF Word Cloud](https://github.com/vivienyuwenchen/TextMining/blob/master/Paradise_Lost_tfidf.png)

Top 50 Words in The_Romance_of_Lust:

- ['prick', 'delicious', 'cunt', 'aunt', 'miss', 'doctor', 'quite', 'bottom', 'excited', 'bed', 'told', 'mrs', 'mamma', 'fuck', 'frankland', 'clitoris', 'boy', 'exquisite', 'darling', 'mouth', 'got', 'charming', 'charlie', 'lust', 'three', 'get', 'legs', 'excitement', 'harry', 'evelyn', 'fucking', 'passions', 'ellen', 'fucked', 'count', 'cock', 'mary', 'lizzie', 'done', 'exciting', 'wife', 'movements', 'fine', 'belly', 'begged', 'lascivious', 'dale', 'gently', 'together', 'sisters']

Sentiment of Top 50 Words in The_Romance_of_Lust:

- {'neg': 0.21, 'neu': 0.434, 'pos': 0.356, 'compound': 0.9137}

![The Romance of Lust TF-IDF Word Cloud](https://github.com/vivienyuwenchen/TextMining/blob/master/The_Romance_of_Lust_tfidf.png)

### Reflection [~1 paragraph]

*From a process point of view, what went well? What could you improve? Other possible reflection topics: Was your project appropriately scoped? Did you have a good plan for unit testing? How will you use what you learned going forward? What do you wish you knew before you started that would have helped you succeed?*

I got more than what I hoped for to work. Originally, I was just thinking of comparing the most common words and sentiments of novels of various genres and making an aesthetically pleasing word cloud for each novel. I started the project early enough to get that code working, so I decided to try to implement TF-IDF as well. I ended up relying quite heavily on a python tutorial to figure out what TF-IDF even was (I have a keeping myself awake when faced with Wikipedia articles; hence, my project involved text from Project Gutenberg and not Wikipedia). However, the tutorial helped me a lot with figuring out new syntax, so that was great. I also spent a lot of time working with the code because I didn't want to change my original code too much, so I feel like I have a strong grasp on the concept now. Going forward, I will likely use the idioms I learned and the libraries I found. I kind of wish I had more of a direction for my project before I started, but I nevertheless had a good time figuring things out along the way. As a result, though, I ended up running my functions from the main code instead of thinking of doctests, although I found it easier than doctests in this case because I already had a working output from my Word Frequency Toolbox to compare my results to. I ended up improving upon the code I had written for the toolbox as well. I kind of want to consolidate my code further and try out different sources and analyses, but at this point, I feel that I've spent too much time on this project and will leave that endeavor for future, bored me.

### References

[1] https://pypi.python.org/pypi/stop-words

[2] http://xpo6.com/list-of-english-stop-words/

[3] https://github.com/amueller/word_cloud

[4] http://stevenloria.com/finding-important-words-in-a-document-using-tf-idf/
