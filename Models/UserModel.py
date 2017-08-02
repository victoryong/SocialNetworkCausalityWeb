# -*- coding: utf-8 -*-
"""
Created on Sat Apr 15 16:20:40 2017

@author: Xie Yong
"""
import math
from datetime import datetime

# from Models.TopicModel import TopicModel
from utils import Logging
from utils.ConfigAll import StartDatetime, EndDatetime, Duration, N_Topics, TimeFormat
from utils.WordsSegmentation import tokenize

logger = Logging.get_console_logger('UserActivity')


class UserActivity:
    """Object of an user's activities information"""
    def __init__(self, user_id, activities=None):
        """
        Init an UserActivity object
        # :param nick: Nickname of the user
        :param user_id: Id of the user
        :param activities: An ActivityInfo array, contains all activities' information of the user
        """
        # self.nick = nick
        self.userId = user_id
        self.sequence = []
        self.topics = []
        if activities is None:
            self.activities = []
        else:
            self.activities = activities
        self.textList = []

    def make_sequence(self):
        """
        Make the sequence data according to ActivityInfo array.
        :return: Array of binary data.
        """
        if not len(self.activities):
            logger.error('No any activity exist! Cannot make sequence. ')
            return []

        dur_sec = Duration * 3600
        se_len = int(math.ceil((EndDatetime - StartDatetime).total_seconds() / dur_sec))
        se = [0] * se_len

        self.topics = [[0] * N_Topics for i in range(se_len)]
        curr = -1
        text_list = []

        for i in self.activities:
            delta = (EndDatetime - i.datetime).total_seconds()
            d = int(delta/dur_sec)
            i.index = d
            se[d] = 1
            if d > curr:
                text_list.append(i.content.replace(u'\u200b', ''))
                curr = i.index

        self.textList = tokenize(text_list)
        self.sequence = se

    def __str__(self):
        """
        Define the print string of UserActivity object.
        :return: A string for print.
        """
        # ua_str = 'Nick: ' + self.nick + '\nuserId: ' + self.userId + '\n'
        ua_str = 'userId: ' + self.userId + '\n'
        for i in self.activities:
            ua_str += i.__str__() + '\n'
        return ua_str

    @staticmethod
    def content_filter(content):
        return content.replace('@', '[metion]').replace('[a-zA-Z]+://[^\s]*', '[url]')


class ActivityInfo:
    """Object of an activity, includes useful information of one activity"""
    def __init__(self, p_time='2017-03-31 00:00', content=''):
        self.pubTime = p_time
        self.content = content
        self.index = -1

    @property
    def datetime(self):
        """
        Get a datetime object that represents the date and time when released
        :return:Release datetime object
        """
        return datetime.strptime(self.pubTime, TimeFormat)

    def __str__(self):
        """
        Define the print string of ActivityInfo object.
        :return: A string for print.
        """
        return self.pubTime + '\n' + self.content

if __name__ == '__main__':
    logger.info('Test Module UserActivity')
    # print ActivityInfo().datetime
    print(UserActivity('', '').make_sequence())
