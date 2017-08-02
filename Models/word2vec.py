# -*- coding: utf-8 -*-
import gensim
from io import StringIO
import numpy as np
import csv

from utils.ConfigAll import N_Topics
from utils.Logging import get_console_logger

logger = get_console_logger('Word2Vec')


def train_w2v(infile_path, model_path):
    file = open(infile_path, 'r', encoding='utf-8') if infile_path.find('\n') < 0 else StringIO(infile_path)
    sentences = []
    for sen in file.readlines():
        sentences.append(sen.strip().split(' '))
    model = gensim.models.Word2Vec(sentences, size=100, min_count=0)
    model.save(model_path+'/w2vmodel')
    model.wv.save_word2vec_format(model_path+'/vec.txt', binary=False)
    file.close()
    # print(model['['])
    return model


def load_model(path):
    model = gensim.models.word2vec.Word2Vec.load(path)
    print(model['我'])
    print(type(model['我']))
    print(model['我'].shape)
    return model


def _make_vectors_of_one_user(model, sen, seq):
    n_samples = len(seq)
    n_dims = N_Topics
    vec_of_one = []
    sen_index = 0
    for i in range(n_samples):
        if seq[i] == 0:
            vec_of_one.append(np.zeros(n_dims))
        else:
            words = sen[sen_index]
            temp_vec = np.zeros(n_dims)
            for w in words:
                temp_vec += np.array(model[w])
            vec_of_one.append(temp_vec)
            sen_index += 1
    print(np.array(vec_of_one).shape)
    return np.array(vec_of_one)


def _save_vectors(vec, path):
    shape = path.split('_')[-3:-1]
    # shape = str(shape[0]) + ' ' + str(shape[1])
    print('vec')
    print(vec.shape)
    with open(path, 'w', newline='') as fp:
        writer = csv.writer(fp)
        writer.writerow(shape)
        for i in vec:
            print(i.shape)
            writer.writerows(i)


def make_vectors_according_to_sequences(model, sentences, sequences, out_path):
    logger.info('Start Making vectors according to sequences of all users... ')
    sequences = np.array(sequences)
    n_user, n_samples = sequences.shape
    # print(n_user, n_samples)
    vec = []

    index = 0
    for i in range(n_user):
        line_seq = sequences[i, :]
        count = sum(line_seq)
        vec.append(_make_vectors_of_one_user(model, sentences[index: index+count], line_seq))
        index += count
    vec = np.array(vec)
    logger.info('Saving vectors to %s ......' % out_path)
    _save_vectors(vec, out_path)
    logger.info('Saving vectors to %s completely! ' % out_path)
    logger.info('ALl vectors are made successfully! ')
    return vec

if __name__ == '__main__':
    # train_w2v(infile_path='../Data/Text_{samples}_{topics}_{users}.txt'.format(samples=8760,topics=100,users=2),
    #           model_path='E:/StudyTime!/Causality/Projects/毕业设计/SocialNetwork_web/Data/word2vec')
    load_model('E:/StudyTime!/Causality/Projects/毕业设计/SocialNetwork_web/Data/word2vec/w2vmodel')
