# -*- coding: utf-8 -*-

import jieba.posseg as pseg
from sklearn.decomposition import LatentDirichletAllocation as LDA
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np

from functools import reduce


class TopicModelLDA(LDA):
    def __init__(self, n_topics=100, max_iter=1500, random_state=1):
        LDA.__init__(self, n_topics=n_topics, max_iter=max_iter, random_state=random_state)
        self._super = super(TopicModelLDA, self)

    @staticmethod
    def _words_segmentation(doc_list):
        doc_list = doc_list or ['我爱北京天安门，',
                                '天安门上太阳升',
                                '',
                                '',
                                '伟大领袖毛主席',
                                '指引我们向前进',
                                '我来到你的城市',
                                '走过你来时的路',
                                '和我在成都的街头走一走',
                                '直到所有的灯都熄灭了也不停留',
                                '你会挽着我的衣袖',
                                '我会把手揣进裤兜']
        if not len(doc_list):
            return []
        doc = []
        for line in doc_list:
            words = pseg.cut(line)
            word_list = [w.word for w in words]
            if not len(word_list):
                continue
            sentence = reduce(lambda xx, y: xx + ' ' + y, word_list)
            doc.append(sentence)
            # print(sentence)

        # try:
        #     print(doc)
        # except UnicodeEncodeError:b
        #     print(x.encode('utf-8') for x in doc)
        return doc

    @staticmethod
    def _tfidf(doc):
        if not len(doc):
            return [], []
        # print(doc)
        vectorizer = TfidfVectorizer()  # 该类会将文本中的词语转换为词频矩阵，矩阵元素a[i][j] 表示j词在i类文本下的词频
        transformer = TfidfTransformer()  # 该类会统计每个词语的tf-idf权值
        try:
            tfidf = transformer.fit_transform(vectorizer.fit_transform(doc))
        except ValueError :
            return [], []
        word = vectorizer.get_feature_names()  # 获取词袋模型中的所有词语
        weight = tfidf.toarray()  # 将tf-idf矩阵抽取出来，元素a[i][j]表示j词在i类文本中的tf-idf权重
        #  打印每类文本的tf-idf词语权重，第一个for遍历所有文本，第二个for便利某一类文本下的词语权重
        # for i in range(len(weight)):
        #         print("-------这里输出第", i, "类文本的词语tf-idf权重------")
        #         for j in range(len(word)):
        #             print(word[j], weight[i][j])
        # print(weight.shape)
        return word, weight

    def fit_doc(self, doc_list):
        vocab, X = self._tfidf(self._words_segmentation(doc_list))
        if not len(vocab):
            return
        # X = np.asarray(weight)

        # vocab = tuple(word)
        # model = LDA(n_topics=5, max_iter=1500, random_state=1)
        self.fit(X)  # model.fit_transform(X) is also available
        # topic_word = self.components_  # model.components_ also works
        # n_top_words = 5
        # for i, topic_dist in enumerate(topic_word):
        #     topic_words = np.array(vocab)[np.argsort(topic_dist)][:-n_top_words:-1]
            # print('Topic %d:  %s' % (i, ' '.join(topic_words)))

    def transform_doc(self, doc_list):
        vocab, X = self._tfidf(self._words_segmentation(doc_list))
        if not len(vocab):
            return [0]*self.n_topics
        doc_topic = self.transform(X)
        # print(doc_topic)

        # std_deviations = np.std(doc_topic, axis=0)
        # # print(std_deviations)
        # active_topics_vector = [1 if x > 0.05 else 0 for x in std_deviations]
        # # print(active_topics_vector)
        # return active_topics_vector
        return doc_topic
    
    def estimate(self, doc_list):
        self.fit_doc(doc_list)
        return self.transform_doc(doc_list)


if __name__ == '__main__':
    result = TopicModelLDA().estimate(None)
    print(result)
    print(len(result))
