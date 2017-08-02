# -*- coding: utf-8 -*-
import gensim
import numpy as np
import csv

from utils.ConfigAll import N_Topics, d2vDir
from utils.Logging import get_console_logger

logger = get_console_logger('Doc2Vec')


def train_d2v(infile_path, model_path):
    """
    Input a path of texts and train the doc2vec model. It can only accept file path as it's input rather than
    content texts.
    :param infile_path: Path of input text.
    :param model_path: Path where the result will be restored.
    :return: A model has been trained.
    """
    # file = open(infile_path, 'r', encoding='utf-8') if infile_path.find('\n') < 0 else StringIO(infile_path)
    documents = gensim.models.doc2vec.TaggedLineDocument(infile_path)
    model = gensim.models.Doc2Vec(documents, size=100, min_alpha=0.025, workers=4, min_count=0)
    model.save(model_path+'/d2vmodel')
    model.wv.save_word2vec_format(model_path+'/vec.txt', binary=False)
    # file.close()
    # print(model['['])
    return model


def load_model(path):
    model = gensim.models.doc2vec.Doc2Vec.load(path)
    model.delete_temporary_training_data(keep_doctags_vectors=True, keep_inference=True)
    print(model.docvecs[0])
    print(type(model.docvecs[0]))
    print(model.docvecs[0].shape)
    return model


def _make_vectors_of_one_user(model, seq, index):
    n_samples = len(seq)
    n_dims = N_Topics
    vec_of_one = []
    for i in range(n_samples):
        if seq[i] == 0:
            vec_of_one.append(np.zeros(n_dims))
        else:
            vec_of_one.append(model.docvecs[index])
            index += 1
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
    model = load_model(d2vDir + '/d2vmodel')
    sequences = np.array(sequences)
    n_user, n_samples = sequences.shape
    # print(n_user, n_samples)
    vec = []

    index = 0
    for i in range(n_user):
        line_seq = sequences[i, :]
        count = sum(line_seq)
        vec.append(_make_vectors_of_one_user(model, line_seq, index))
        index += count
    vec = np.array(vec)
    logger.info('Saving vectors to %s ......' % out_path)
    _save_vectors(vec, out_path)
    logger.info('Saving vectors to %s completely! ' % out_path)
    logger.info('ALl vectors are made successfully! ')
    return vec

if __name__ == '__main__':
    # train_d2v(infile_path='../Data/Text_{samples}_{topics}_{users}.txt'.format(samples=8760, topics=100, users=2),
    #           model_path=d2vDir)
    load_model(d2vDir + '/d2vmodel')
