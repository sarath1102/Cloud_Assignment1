#!/usr/bin/env python3
"""reducer.py"""

from operator import itemgetter
import sys

current_comment_id = None
max_top_users = 10
max_top_words = 10
user_map = {}
user_count_map = {}
corpus_word_count = 0
old_word = None
word_stats_dict = {}
corpus_word_count_dict = {}
num_documents = 0

# input comes from STDIN
for line in sys.stdin:
    # remove leading and trailing whitespace
    line = line.strip()
    # parse the input we got from our tf-idf mapper file
    comment_id, author, word_stat, count = line.split('\t')
    try:
        count = int(count)
    except ValueError:
        # count was not a number, so silently
        # ignore/discard this line
        continue

    ws = word_stat.split(",")
    word = ws[0]
    max_words = ws[1]

    # setup the user map dictionaries
    if not author in user_map:
        user_map[author] = {}
    if current_comment_id != comment_id:
        # we are receving a new stream for a new comment, increment
        # the author counter used to track how many comments a user made
        user_count_map[author] = user_count_map.get(author, 0) + 1
        current_comment_id = comment_id
        num_documents += 1

    # also update user -> different word count tracker dict
    user_map[author][word] = user_map.get(author).get(word, 0) + count

    # store the word stats for each incoming word
    if old_word != word:
        if old_word:
            corpus_word_count_dict[old_word] = corpus_word_count
            corpus_word_count = 0
        old_word = word
    try:
        corpus_word_count += int(count)
        if word in word_stats_dict.keys():
            word_stats_dict[word].append(comment_id + "," + str(count) + "," + max_words)
        else:
            word_stats_dict[word] = list()
            word_stats_dict[word].append(comment_id + "," + str(count) + "," + max_words)
    except:
        continue
corpus_word_count_dict[old_word] = corpus_word_count

# sort the users to start iterate from the user who had more comments
sorted_users = {k: v for k, v in sorted(user_count_map.items(), reverse=True, key=lambda item: item[1])}
print("sorted user dictionary where users are soreted based on total spam count {}\n\n".format(sorted_users))
user_counter = 0
word_counter = 0
for user, count in sorted_users.items():
    if user_counter >= max_top_users:
        break
    user_counter += 1
    user_map_count = user_map.get(user, {})
    # for each user, sort our user -> word count tracker to get the top words
    sorted_word_count = {k: v for k, v in sorted(user_map_count.items(), reverse=True, key=lambda item: item[1])}
    for u, c in sorted_word_count.items():
        if word_counter >= max_top_words:
            break
        word_counter += 1
        word_stats_list = word_stats_dict[u]
        # for each word, compute the tf-idf
        print("\n\ngenerating tf-idf for word {} for user {}\n\n".format(u, user))
        for word_stats in word_stats_list:
            word_stats = word_stats.split(",")
            try :
                term_frequency = int(word_stats[1])/int(word_stats[2])
                inverse_doc_freq = num_documents / corpus_word_count_dict[u]
                tf_idf = term_frequency * inverse_doc_freq
                print_key = u + "," + word_stats[0]
                print("%s\t%s" % (print_key, tf_idf))
            except ZeroDivisionError as ex:
                print(word_stats[2])
                print("Error", ex)
    else:
        continue
    word_counter = 0
