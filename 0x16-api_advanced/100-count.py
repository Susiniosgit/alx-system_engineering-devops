#!/usr/bin/python3
"""This file has a recursive function that queries the Reddit API, parses
   the title of all hot articles, and prints a sorted count of given keywords
   (case-insensitive, delimited by spaces. Javascript should count as
   javascript, but java should not).
"""
import requests


def count_words(subreddit, word_list):
    """parses the title of all hot articles, and prints a sorted count
       of given keywords
    """
    try:
        url = "https://www.reddit.com/r/{}/hot.json".format(subreddit)
        r = requests.get(url, headers={'User-Agent': 'hello-student 0.5'},
                         params={'limit': 100})
        d = r.json()
        l = {}
        for i in word_list:
            l[i] = 0
        children = d['data']['children']
        for i in children:
            for j in word_list:
                if j in i['data']['title']:
                    l[j] += 1
        page = d['data']['after']
        if d['data']['after'] is None:
            return
    except KeyError:
        return None
    recursive(subreddit, word_list, page, l)
    l = sorted(l.items(), key=lambda x: x[1], reverse=True)
    for i in l:
        if i[1] != 0:
            print("{}: {}".format(i[0], i[1]))
    return l


def recursive(subreddit, word_list, page="", l=""):
    """handles the other entries"""
    if page is None:
        return
    url = "https://www.reddit.com/r/{}/hot.json".format(subreddit)
    r = requests.get(url, headers={'User-Agent': 'hello-student 0.5'},
                     params={'after': page, 'limit': 100})
    d = r.json()
    children = d['data']['children']
    for i in children:
        for j in word_list:
            if j in i['data']['title']:
                l[j] += 1
    page = d['data']['after']
    return recursive(subreddit, word_list, d['data']['after'], l)
