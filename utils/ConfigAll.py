# -*- coding: utf-8 -*-
"""
Created on Wed June 21 ‎20:16:53 2017

@author: Xie Yong

Global configurations of the whole project.
"""

from datetime import datetime
import os

# Mongodb client information
ClientIp = "10.21.25.40"
Port = 27017
DbName = "Sina_cw1"
CollectionTweets = 'Tweets'

# Time range of data
StartTime = '2013-01-01 00:00'
EndTime = '2014-01-01 00:00'
TimeFormat = '%Y-%m-%d %H:%M'
StartDatetime = datetime.strptime(StartTime, TimeFormat)
EndDatetime = datetime.strptime(EndTime, TimeFormat)

# Time series config
Duration = 1
N_Topics = 100

# Data cleaning config
ScreeningCount = 200


# Default user accounts
DefaultAccounts = ['1192329374', '1214750000', '1252384200', '1256032500', '1497882593',
                   '1640601392', '1642512402', '1642635773', '1644114654', '1651474200',
                   '1657421782', '1736302500', '1771661200', '1784473157', '1873416700',
                   '2149354000', '2259741800', '2292571800', '2385873600', '2651674300',
                   '2859290700',
                   ]
UseDefaultAccounts = True

# Data saving directory. root: Data/
FileNameTemplate = 'Data/{dataType}_{samples}_{topics}_{users}.{postfix}'
UidFile = 'UserId'
SeqFile = 'Sequence'
VecFile = '{modelType}/Vectors'
TextFile = 'Text'
ResultFile = '{modelType}/Result'

N_DataConfig = {'N_Samples': 8760, 'N_Dims': 100, 'N_Users': 21}

# 2vec model dir
w2vDir = 'E:/StudyTime!/Causality/Projects/SocialNetwork_web/Data/word2vec'
d2vDir = 'E:/StudyTime!/Causality/Projects/SocialNetwork_web/Data/doc2vec'
# w2vDir = '~/xy/PycharmProject/SocialNetwork_web/Data/word2vec' # Linux
# d2vDir = '~/xy/PycharmProject/SocialNetwork_web/Data/doc2vec' # Linux
w2v_or_d2v = 1  # 0 for w2v and others for d2v
# w2v_or_d2v = 0

if __name__ == '__main__':
    os.mkdir(w2vDir)

