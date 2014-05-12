#!/usr/bin/python

#           Author: Ryan Miling
#    Last Contrib.: 2014/05/12
#            Desc.: JSON parsing library to filter & validate Twitter posts
#   Time Committed: ~4hrs, took a bit longer than anticipated from struggling with my C compiler and testing
#        Reasoning: For fuzzy-string matching our tweet posts I went with Levenshtein's algorithm. It
#                     was extremely performant and after scanning the results, was pleased with its
#                     grouping. In re to bucketing our posts, the first unique post I find (Levenschtein distance > thresh.)
#                     becomes the gold-standard of the group. We could def. make this smarter by comparing all
#                     members of the group and determine the best standard, but that's a lot of overhead
#                     and not performant. I'd like to play a bit more with the DIST_THRESHOLD to find our "Goldilocks
#                     number," but 10 seems to work.
#
#                   simplejson is a lightweight library to convert our json object to Python so I went with
#                     this module. Putting our json files in a separate dir. allows for easily adding more
#                     files for testing or to allow scanning multiple-files at ease.

# NOTE The exercise questions 1) and 2) are in block comments in this script.
# NOTE Feel free to modify static variables throughout to adjust the output you expect:
# NOTE     DIST_THRESHOLD -- the maximum Levenshtein distance to differentiate alike tweets
# NOTE   DISPLAY_RANKINGS -- view the top n rankings, based on popularity (i.e. RT count)

import os
import sys
import editdistance

sys.path.append(os.path.join(os.getcwd(),"lib"))

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
        group_standards = [] # [<"post">], index of insertion is our group_standard_i
        group_standard_i = 0 # index of insertion for group_standards & grouped_posts
        DIST_THRESHOLD = 10  # shooting for < n differences

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
                    distance = editdistance.eval(post, gst)
                    # if we find one that's similar, let's bucket there
                    if distance < DIST_THRESHOLD:
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

    """
        2) Ranking these groups of Twitter posts by popularity.
    """
    print
    print "#) Count -- Tweet (standard of group)"
    print
    for i,p in enumerate(popular_posts,start=1):
        if i > DISPLAY_RANKINGS:
            break
        print "%i) %i -- %s" % (i,len(p),p[0]['text']) # read the first tweet
        print
