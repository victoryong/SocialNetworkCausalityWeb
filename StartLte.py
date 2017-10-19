# -*- coding: utf-8 -*-
"""
Created on Mon June 26 09:20 2017

@author: Xie Yong

The code is aimed at calculating local transfer entropy of all users according to their vectors of texts.
Vectors are generated in last step StartW2vModel.
"""
import numpy as np
import csv
from utils.ConfigAll import N_DataConfig, FileNameTemplate, VecFile, PcaVecFile, ResultFile, w2v_or_d2v, use_pca_vec
from utils.logging import get_console_logger
from utils.lte import LocalTransferEntropy, LocalTransferEntropyPy

logger = get_console_logger('StartLte')


def start_lte(vec):
    logger.info('Start to calculate local transfer entropy of each pair of users...')
    print(vec.shape)
    n_user = vec.shape[0]
    lte = LocalTransferEntropy(jar_location='./lib/infodynamics.jar').set_lte_property()
    # lte = LocalTransferEntropyPy().set_properties()
    result = np.zeros((n_user, n_user))
    # a = vec[0].tolist()
    # b = vec[10].tolist()
    # lte.calculate_lte(b, a)

    for i in range(n_user):
        for j in range(i):
            a = vec[i].tolist()
            b = vec[j].tolist()
            result[i][j], result[j][i] = lte.compute_lte(a, b)
    logger.info('Calculation ended completely! ')
    print(result)
    save_result(result)
    return result


def save_result(result):
    result1 = np.array(result)
    result2 = np.array(result)
    result1[result1 >= 0.02] = 1
    result1[result1 < 0.02] = 0
    result2[result1 >= 0.03] = 1
    result2[result1 < 0.03] = 0

    with open(FileNameTemplate.format(dataType=ResultFile.format(modelType='doc2vec' if w2v_or_d2v else 'word2vec'), samples=N_DataConfig['N_Samples'],
                                      topics=N_DataConfig['N_Dims'], users=N_DataConfig['N_Users'], postfix='csv'),
              'w', newline='') as fp:
        writer = csv.writer(fp)
        writer.writerows(result)
        writer.writerows(result1)
        writer.writerows(result2)


if __name__ == '__main__':
    # Read csv file of vectors and put the vectors to method start_lte.
    vectors = []
    this_vec_type = VecFile
    if use_pca_vec:
        this_vec_type = PcaVecFile
    logger.info('Start to recover the vectors of all users. ')
    with open(FileNameTemplate.format(dataType=this_vec_type.format(modelType='doc2vec' if w2v_or_d2v else 'word2vec'),
                                      samples=N_DataConfig['N_Samples'],
                                      topics=N_DataConfig['N_Dims'],
                                      users=N_DataConfig['N_Users'],
                                      postfix='csv'), 'r') as fp:
        shape = fp.readline().split(',')
        shape = [int(x) for x in shape]

        lines = fp.readlines()
        vec_list = []
        vec_user_list = []
        idx = 0
        for line in lines:
            vector = np.array(line.strip().split(',')).astype(float)
            vec_list.append(vector)
            idx += 1
            if idx % shape[0] == 0:
                vec_user_list.append(vec_list)
                vec_list = []

        logger.info('Recover vectors completely! ')
        vec_user_list = np.array(vec_user_list)
        start_lte(vec_user_list)

