# -*- coding: utf-8 -*-
"""
Created on Sat Apr 15 15:31:40 2017

@author: Xie Yong

The code is aimed at generating data from original data scrawled on Tweet and saving data
of user id list, sequences and text list(after segmentation) to files.
"""
import sys
import csv
import threading
import time
import re

import pymongo

from Models.UserModel import ActivityInfo
from Models.UserModel import UserActivity
from utils import logging
from utils.ConfigAll import *


logger = logging.get_console_logger('GenData')
totalCount = 0
totalFinishCount = 0
db_client = None


def check_for_tweets(uid, user_model):
    """
    Read all tweets of a user from db and make array of ActivityInfo objects. Callable for thread.
    :param uid: User's id
    :param user_model: Array that contains all users' info and activities.
    :return: A UserActivity object with generated activity sequences
    """
    global totalFinishCount, totalCount
    logger.info('Run task %s. Checking for %s\'s tweets' % (uid, uid))
    start = time.time()
    ai_list = []

    db = db_client[DbName]
    tweets_db = db[CollectionTweets]
    tweets = tweets_db.find({'UserId': int(uid)}, sort=[('PublishTime', pymongo.DESCENDING)])

    if totalCount == 0:
        totalCount = tweets_db.count()
    totalFinishCount += tweets.count()

    logger.info('Finished percentage: %0.3f%%' % (100.0 * totalFinishCount / totalCount))
    if tweets.count() < ScreeningCount:
        logger.info('%s\'s tweets is less than %d.' % (uid, ScreeningCount))
        return None
    for t in tweets:
        ai = ActivityInfo(p_time=t['PublishTime'], content=t['Text'])
        if StartDatetime < ai.datetime < EndDatetime:
            ai_list.append(ai)

    ua = UserActivity(uid, activities=ai_list)
    ua.make_sequence()

    end = time.time()
    logger.info('Task %s runs %0.4f seconds' % (uid, end - start))
    # print ua
    user_model.append(ua)
    return ua


def get_user_tweet_indices():
    with open(sys.path[1] + '/Data/Indices.txt', 'r') as fp:
        indices = fp.readlines()
        # print(indices)
        return list(map(lambda x: int(x.strip()), indices))


class DataGenerator:
    """Object that contains some methods for generating data."""
    def __init__(self):
        """
        Init an object by connecting to mongodb server.
        """
        global db_client
        db_client = pymongo.MongoClient(ClientIp, Port)  # lab
        logger.info('Connect to Mongodb server successfully. %s' % db_client)
        self.threads = []

    def get_user_model(self, debug_option=0):
        """
        Read data from database and form the UserActivity array, which contains user info and user activities' data
        :return: Array of UserActivity objects
        """
        global db_client

        # Get data from database using thread
        user_model = []
        logger.info('Start thread! ')
        debug = 0

        if UseDefaultAccounts:
            from utils.ConfigAll import DefaultAccounts
            users = DefaultAccounts
        else:
            db = db_client[DbName]
            db_tweets = db[CollectionTweets]
            logger.info('Get handler for Database "%s", open collection "%s"' % DbName, CollectionTweets)
            users = db_tweets.find({'UserId'}, {}, no_cursor_timeout=True).distinct()

        for uid in users:
            t = threading.Thread(target=check_for_tweets, name=uid, args=(uid, user_model,))
            self.threads.append(t)
            t.start()
            t.join()

            debug += 1
            if debug == debug_option:
                break
        return user_model

    def save_data(self, user_model, fpath='../' + FileNameTemplate):
        """
        Save user model to files. Including user id, sequence and text after segmentation.
        :param user_model: All user's models.
        :param fpath: Path format of files.
        """

        n_users = len(user_model)
        if not n_users:
            logger.error('No user model! ')
            return

        user_tweet_indices = ['0\n']
        total = 0
        for item in user_model:
            total += sum(item.sequence)
            user_tweet_indices.append(str(total) + '\n')
        with open(sys.path[1] + '/Data/Indices.txt', 'w') as fp:
            fp.writelines(user_tweet_indices)

        n_samples = len(user_model[0].sequence)
        samples = []
        all_texts = ''
        id_list = [int(x.userId) for x in user_model]

        with open(fpath.format(dataType=UidFile, samples=n_samples, users=n_users, topics=N_Topics, postfix='csv'),
                  'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            logger.info('Start writing users information to %s...' % csvfile.name)
            writer.writerow(id_list)
            logger.info('Successfully wrote to %s!' % csvfile.name)

        with open(fpath.format(dataType=SeqFile, samples=n_samples, users=n_users, topics=N_Topics, postfix='csv'),
                  'w', newline='') as fseq, \
                open(fpath.format(dataType=TextFile, samples=n_samples, users=n_users, topics=N_Topics, postfix='txt'),
                     'w', encoding='utf-8') as ftxt:
            logger.info('Start writing samples, topic vectors and text after segmentation into files...')
            seqwriter = csv.writer(fseq)
            for um in user_model:
                samples.append(um.sequence)
                seqwriter.writerow(um.sequence)
                str_text = '\n'.join(um.textList) + '\n'
                ftxt.write(str_text)
                # ftxt.writelines(um.textList)
                all_texts += str_text

            logger.info('Successfully wrote to %s, %s!' % (fseq.name, ftxt.name))
            return id_list, samples, all_texts


if __name__ == '__main__':
    logger.info('Test module GenSequences')
    gen = DataGenerator()
    u_model = []
    u_model = gen.get_user_model(debug_option=2)
    gen.save_data(u_model)
    print(get_user_tweet_indices())
