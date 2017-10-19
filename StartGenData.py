# -*- coding: utf-8 -*-
"""
Created on Sat June 24 22:32 2017

@author: Xie Yong

The code is aimed at getting data from db and make it the form we want it to be.
We can obtain id list, samples, all texts after segmentation and user model list and what's more
significant is all these data are saved into files so that we can load them easily when go to next step.
"""

from utils import logging
from utils.gendata import DataGenerator
from utils.ConfigAll import FileNameTemplate

logger = logging.get_console_logger('StartGenData')


def start_gen_data():
    # Generate samples
    logger.info('Start to generate data.')
    gen = DataGenerator()
    u_model = gen.get_user_model()  # debug_option=20
    id_list, samples, all_texts = gen.save_data(u_model, fpath=FileNameTemplate)
    logger.info('Data generation ended. ')

    # # Infer causality using transfer entropy with sequence data.
    # samples = np.array(samples)
    # nnodes, tmax = samples.shape
    # print(getGraph(samples, None, None, nnodes, tmax))
    return u_model, id_list, samples, all_texts

if __name__ == '__main__':
    start_gen_data()
