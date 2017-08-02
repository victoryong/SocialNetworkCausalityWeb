# # -*- coding: utf-8 -*-
# from jpype import *
# from sklearn import preprocessing
#
# package_name="infodynamics.measures.continuous.kraskov"
# startJVM(getDefaultJVMPath(), "-ea", "-Djava.class.path=./lib/infodynamics.jar")
#
#
# a = [[1., 550., 1.], [0., 450., 1.], [0., 0., 0.], [0., 0., 1.], [0., 0., 0.], [0., 0., 1.], [0., 0., 0.], [0., 0., 1.],
#      [0., 0., 0.], [0., 200., 1.], [0., 10., 0.], [0., 0., 1.], [0., 0., 0.], [0., 0., 1.], [0., 0., 0.], [0., 0., 1.], [0., 0., 0.],
#      [0., 0., 1.], [0., 0., 0.], [0., 0., 1.], [0., 0., 0.], [0., 0., 1.], [0., 0., 0.], [0., 0., 1.], [0., 0., 0.], [0., 0., 1.],
#      [0., 0., 0.], [0., 0., 1.], [0., 0., 0.], [0., 0., 0.]]
# b = [[4., 1., 0.], [0., 1., 5.], [6., 1., 1.], [0., 0., 1.], [0., 0., 0.], [0., 0., 1.], [0., 0., 0.], [0., 0., 1.], [0., 0., 0.],
#      [0., 0., 1.], [0., 0., 0.], [0., 0., 1.], [0., 0., 0.], [0., 0., 1.], [0., 0., 0.], [0., 0., 1.], [0., 0., 0.], [0., 0., 1.],
#      [0., 0., 0.], [0., 55., 1.], [0., 0., 0.], [0., 0., 1.], [0., 0., 0.], [0., 0., 1.], [0., 0., 0.], [0., 0., 1.],
#      [0., 0., 0.], [0., 0., 1.], [0., 0., 0.], [0., 0., 1.]]
# c = [[4., 1., 0.], [0., 1., 5.], [6., 1., 1.], [0., 0., 1.], [0., 0., 0.], [0., 0., 1.], [0., 0., 0.], [0., 0., 1.],
#      [0., 0., 0.],
#      [0., 0., 1.], [0., 0., 0.], [0., 0., 1.], [0., 0., 0.], [0., 0., 1.], [0., 0., 0.], [0., 0., 1.], [0., 0., 0.],
#      [0., 0., 1.],
#      [0., 0., 0.], [0., 55., 1.], [0., 0., 0.], [0., 0., 1.], [0., 0., 0.], [0., 0., 1.], [0., 0., 0.],
#      [0., 0., 1.],
#      [0., 0., 0.], [0., 0., 1.], [0., 0., 0.], [0., 0., 1.]]
# print(len(a), len(a[0]))
# a = preprocessing.maxabs_scale(a, axis=0)
# b = preprocessing.maxabs_scale(b, axis=0)
# print(a)
# print(b)
#
# te_calc_class = JPackage(package_name).TransferEntropyCalculatorMultiVariateKraskov
# mi_calc_class = JPackage(package_name).MutualInfoCalculatorMultiVariateKraskov
# teCalc = te_calc_class()  #
# teCalc.setProperty(mi_calc_class.PROP_K, '3')  # Use Kraskov parameter K=4 for 4 nearest points
# teCalc.setProperty("PROP_K", '3')  # Use Kraskov parameter K=4 for 4 nearest points
# teCalc.setProperty(te_calc_class.PROP_KRASKOV_ALG_NUM, "1")
# teCalc.setProperty("NORMALISE", "true")
# print(teCalc.props)
#
# teCalc.initialise(1, 3, 3)
# teCalc.setObservations(a, b)
# result1 = teCalc.computeAverageLocalOfObservations()
# result = teCalc.computeLocalOfPreviousObservations()
# # print("TE result %.4f nats." % result)
# print(result1)
# print(result)
#
# teCalc.initialise(1, 3, 3)
# teCalc.setObservations(a, b)
# result2 = teCalc.computeAverageLocalOfObservations()
# result = teCalc.computeLocalOfPreviousObservations()
# print(result2)
# print(result)
#
# teCalc.initialise(1, 3, 3)
# teCalc.setObservations(a, b)
# result2 = teCalc.computeAverageLocalOfObservations()
# result = teCalc.computeLocalOfPreviousObservations()
# print(result2)
# print(result)

from utils.ConfigAll import *
a = FileNameTemplate.format(dataType=VecFile.format(modelType='doc2vec' if w2v_or_d2v else 'word2vec'),
                            postfix='csv',
                            samples=N_DataConfig['N_Samples'],
                            users=N_DataConfig['N_Users'],
                            topics=N_DataConfig['N_Dims'])
print(a)
