#           Author: Ryan Miling
#    Last Contrib.: 2014/05/10
#            Desc.: JSON parsing library to filter & validate Twitter posts

import os
import sys

sys.path.append(os.path.join(os.getcwd(),"lib"))

from levenshtein import levenshtein
import simplejson


JSON_DIR = "json" # rel-path to json files


class TweetHandler(object):
    # list of posts in the format of {"text": <str>, "created_date": <int>, "author": <obj>}
    posts = []

    def __init__(self,json_file):
        self._load_json(json_file)

    # Loads the json-file from the file-system
    def _load_json(self, json_file):
        file_path = os.path.join(JSON_DIR,json_file)
        json_obj = simplejson.load(open(file_path))

        self.tweets = json_obj['tweets']


    """
       1) Finding the "true" number of posts, by grouping the Twitter posts together
            if they are retweeting or commenting on the same message. Your method
            should be robust to small changes, so that if someone introduces a small
            typo or uses a retweet prefix or postfix that's not in the set of data
            provided, your technique for grouping would still work.
    """
    # bucket similar posts by their content
    def group_true_posts(self):

        # We know it's a RT when it contains the string RT,
        #   but keep in mind we aren't guaranteed to have the original
        #   so string-matching is increased by a degree of n.

        grouped_posts = []   # LoL of posts, grouped by similarity
        group_standards = [] # [<"post">], index is our group_standard_i
        group_standard_i = 0 # index of insertion for group_standards & grouped_posts
        dist_threshold = 10  # shooting for < n differences

        for tweet in self.tweets:
            post = tweet["text"].strip()

            if post[0:2] == "RT":
                post = post[2:].lower()

                # on first iter.
                if group_standard_i == 0:
                    group_standards.append(post)
                    grouped_posts.append([tweet])

                    group_standard_i += 1
                    continue

                matching_gst_i = -1
                for gst_i,gst in enumerate(group_standards):
                    distance = levenshtein(post, gst)
                    # if we find one that's similar, let's bucket there
                    if distance < dist_threshold:
                        matching_gst_i = gst_i
                        break

                if matching_gst_i != -1:
                    grouped_posts[matching_gst_i].append(tweet)
                else:
                    group_standards.append(post)
                    grouped_posts.append([tweet])

                    group_standard_i += 1

        return grouped_posts


if __name__ ==  "__main__":
    th = TweetHandler('tweets.json')
    print "%i total tweets" % len(th.tweets)

    grouped_posts = th.group_true_posts()
    print "%i retweets (RTs)" % (sum(len(x) for x in grouped_posts))

    popular_posts = sorted(grouped_posts, key=len, reverse=True)
    DISPLAY_RANKINGS = 5

    if DISPLAY_RANKINGS:
        print
        print "Top %i Tweets:" % DISPLAY_RANKINGS

    for i,p in enumerate(popular_posts,start=1):
        if i > DISPLAY_RANKINGS:
            break
        print "%i) %s" % (i,p[0]['text']) # read the first tweet
        print

