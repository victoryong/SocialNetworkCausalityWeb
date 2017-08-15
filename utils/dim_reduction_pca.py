from sklearn.decomposition import PCA
import csv
import numpy as np

pca_transformer = PCA(n_components=50)


def dimension_reduction(data):
    return pca_transformer.fit_transform(data)


def _save_vectors(vec, path):
    size = path.split('_')[-3:-1]
    # size = str(size[0]) + ' ' + str(size[1])
    print('vec')
    print(vec.shape)
    with open(path, 'w', newline='') as fp:
        writer = csv.writer(fp)
        writer.writerow(size)
        for i in vec:
            print(i.shape)
            writer.writerows(i)

if __name__ == "__main__":
    from utils.ConfigAll import *
    import numpy as np
    with open("../" + FileNameTemplate.format(dataType=VecFile.format(modelType='doc2vec' if w2v_or_d2v else 'word2vec'),
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
                vec_user_list.append(dimension_reduction(vec_list))
                vec_list = []

    _save_vectors(np.asarray(vec_user_list, dtype=float), "../" +
                  FileNameTemplate.format(dataType=PcaVecFile.format(modelType='doc2vec' if w2v_or_d2v else 'word2vec'),
                                          samples=N_DataConfig['N_Samples'],
                                          topics=N_DataConfig['N_Dims'],
                                          users=N_DataConfig['N_Users'],
                                          postfix='csv'))
