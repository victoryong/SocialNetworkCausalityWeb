# -*- coding: utf-8 -*-
"""
Created on Sun June 09:36 2017

@author: Xie Yong

The code is aimed at making vectors for each user's texts by using the word2vec model trained.
"""
from io import StringIO

import numpy as np

from utils.ConfigAll import w2vDir, d2vDir, w2v_or_d2v, N_DataConfig, SeqFile, TextFile, FileNameTemplate, VecFile


def start_get_vectors(w2v_model, txt_file_path, all_seq):
    file = open(txt_file_path, 'r', encoding='utf-8') if txt_file_path.find('\n') < 0 else StringIO(txt_file_path)
    sentences = []
    for sen in file.readlines():
        sentences.append(sen.strip().split(' '))
    file.close()
    if w2v_or_d2v:
        from Models.doc2vec import make_vectors_according_to_sequences
    else:
        from Models.word2vec import make_vectors_according_to_sequences
    all_vectors = make_vectors_according_to_sequences(w2v_model, sentences, all_seq,
                                                      FileNameTemplate.format(dataType=VecFile.format(modelType='doc2vec' if w2v_or_d2v else 'word2vec'),
                                                                              postfix='csv',
                                                                              samples=N_DataConfig['N_Samples'],
                                                                              users=N_DataConfig['N_Users'],
                                                                              topics=N_DataConfig['N_Dims']))
    return all_vectors


if __name__ == '__main__':
    n_words = 0
    n_topics = 0
    vec_dict = {}

    model_dir = w2vDir if w2v_or_d2v == 0 else d2vDir
    with open(model_dir + '/vec.txt', encoding='utf-8') as fp:
        shape = fp.readline().rstrip().split(' ')
        n_words = int(shape[0])
        n_topics = int(shape[1])

        for i in range(n_words):
            word_value = fp.readline().rstrip().split(' ')
            word = word_value[0]
            values = np.array(word_value[1:]).astype(float)
            vec_dict[word] = values
            # dic = {word: values}
            # print(dic)

        print(n_words, n_topics)
        # print(len(vec_dict))

    seq_list = []
    with open(FileNameTemplate.format(dataType=SeqFile, samples=N_DataConfig['N_Samples'], postfix='csv',
                                      topics=N_DataConfig['N_Dims'], users=N_DataConfig['N_Users']), 'r') as fp:
        for line in fp.readlines():
            seq_list.append([int(l) for l in line.rstrip().split(',')])

    start_get_vectors(vec_dict,
                      FileNameTemplate.format(dataType=TextFile, samples=N_DataConfig['N_Samples'],
                                              postfix='txt', topics=N_DataConfig['N_Dims'],
                                              users=N_DataConfig['N_Users']),
                      seq_list)



