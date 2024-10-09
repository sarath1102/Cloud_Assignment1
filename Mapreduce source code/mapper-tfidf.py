#!/usr/bin/env python3
"""mapper-tfidf.py"""

import sys

# input comes from STDIN (standard input)
for line in sys.stdin:
    # remove leading and trailing whitespace
    line = line.strip()
    # split the line to extract words and assign accordingly
    words = line.split("\t")
    comment_id = words[0]
    author = words[1]
    content = words[2]
    for word in content.split(" "):
        # split each word in the content and print to stdout for reducer to use it
        # we prints comment_id, author, word and total words in the comment
        if word.isalnum():
            print("{}\t{}\t{},{}\t{}".format(comment_id, author, word.rstrip(), len(content.split(" ")), 1))
