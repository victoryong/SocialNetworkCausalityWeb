# -*- coding: utf-8 -*-
"""
Created on Sat June 24 22:43 2017

@author: Xie Yong

The code is aimed at training the word2vec model with all text data after segmentation and then
saving the model into a binary file and the vocabulary-vector dict into a txt file. All-text data
may be read from a certain file or from last step(startGenData).
"""
from Models import word2vec, doc2vec
from utils.ConfigAll import w2vDir, d2vDir, N_DataConfig, w2v_or_d2v


def start_2vev_model(path_or_text):
    if w2v_or_d2v:
        return doc2vec.train_d2v(path_or_text, d2vDir)
    else:
        return word2vec.train_w2v(path_or_text, w2vDir)


if __name__ == '__main__':
    filename = 'Data/Text_{samples}_{topics}_{users}.txt'.format(samples=N_DataConfig['N_Samples'],
                                                                 topics=N_DataConfig['N_Dims'],
                                                                 users=N_DataConfig['N_Users'])
    start_2vev_model(filename)


