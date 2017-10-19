# -*- coding: utf-8 -*-
"""
Created on Sat June 24 20:20 2017

@author: Xie Yong

"""
import jieba
# import os

from utils.logging import get_console_logger

logger = get_console_logger('WordsSegmentation')


def tokenize(sentences, output_path=None, keep_tokens=None, filter_tokens=None):
    """
    Accept a list of original texts and return a list of texts after segmentation.
    :param sentences: List of text before segmentation.
    :param output_path: Path that the result locate.
    :param keep_tokens:  List of tokens that will be kept.
    :param filter_tokens: List of tokens that will be filtered.
    :return List of Text after segmentation.
    """
    # Load user-defined dictionary
    # for fname in os.listdir('/home/yr/myfile/dataspace/medical/KB/dict2'):
    #     jieba.load_userdict('/home/yr/myfile/dataspace/medical/KB/dict2/'+fname)

    seg_sen = []
    logger.info('segment sentence...')
    if filter_tokens and keep_tokens:
        for line in sentences:
            seg = jieba.lcut(line.replace(r'\r?\n', ''))
            filter_seg = []
            for token in seg:
                if token not in filter_tokens:
                    if token in keep_tokens:
                        filter_seg.append(token)
            seg_sen.append(filter_seg)
    elif filter_tokens:
        for line in sentences:
            seg = jieba.lcut(line.replace('\n', ''))
            filter_seg = []
            for token in seg:
                if token not in filter_tokens:
                    filter_seg.append(token)
            seg_sen.append(filter_seg)
    elif keep_tokens:
        for line in sentences:
            seg = jieba.lcut(line.replace('\n', ''))
            filter_seg = []
            for token in seg:
                if token.decode().encode('utf-8') in keep_tokens:
                    filter_seg.append(token)
            seg_sen.append(filter_seg)
    else:
        for sen in sentences:
            seg = jieba.lcut(sen.replace(r'(\r)?\n', ''))
            seg_sen.append(seg)
    # if output_path:
    #     f = open(output_path, 'w')
    #     for sen in seg_sen:
    #         f.write(' '.join(sen)+'\n')
    seg_sen = [' '.join(sen) for sen in seg_sen]
    logger.info('Segment words successfully! ')
    return seg_sen

if __name__ == '__main__':
    logger.info('Start testing words segmentation.')
    text = tokenize(['我爱北京天安门，',
                     '天安门上太阳升',
                     '伟大领袖毛主席',
                     '指引我们向前进',
                     '我来到你的城市',
                     '走过你来时的路',
                     '和我在成都的街头走一走',
                     '直到所有的灯都熄灭了也不停留',
                     '你会挽着我的衣袖',
                     '我会把手揣进裤兜'])
    print(text)
    print(''.join(text))
    # for sen in seg_sen:
    #     print(' '.join(sen)+'\n')
    logger.info('End testing.')

