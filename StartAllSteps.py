# -*- coding: utf-8 -*-
"""
Create on Sat June 24 22:39 2017

@author: Xie Yong

The code is aimed at performing all the processes in this project from getting data to eventually
obtain the result of local transfer entropy.
"""
from StartGenData import *
from Start2vecModel import *
from StartGetVectors import *
from StartLte import *


def start_all():
    u_model, id_list, samples, all_texts = start_gen_data()
    vec_model = start_2vev_model(all_texts)
    vec = start_get_vectors(vec_model,
                            FileNameTemplate.format(dataType=TextFile, samples=N_DataConfig['N_Samples'],
                                                    postfix='txt', topics=N_DataConfig['N_Dims'],
                                                    users=N_DataConfig['N_Users']),
                            samples)
    causal_network = start_lte(vec)
    print(causal_network)

if __name__ == '__main__':
    start_all()

