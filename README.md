# tweet clustering
Our tweet-handler is responsible for reading over a collection of tweets in a file
  format (e.g. json) and grouping them by similar content, also allowing
  sub-filtering based on retweets.

Prerequisites:
  + Python 2.7
  + EditDistance module - https://pypi.python.org/pypi/editdistance/0.2
    - install via `pip install editdistance`,
       or look at the src files I included in lib/ and add it to the py-path yourself

Usage Instructions:
  Run tweet_handler.py from its source directory and behold the glory.
