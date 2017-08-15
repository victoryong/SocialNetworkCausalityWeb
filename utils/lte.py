# -*- coding: utf-8 -*-
import random
from jpype import *
import numpy as np

from utils.ConfigAll import N_Topics
from utils.knn.te_multivar_ksg import TECalculatorMultiVarKraskov


class LocalTransferEntropy:
    def __init__(self, jar_location="../lib/infodynamics.jar"):
        self.jar_location = jar_location
        self.teCalc = None

        startJVM(getDefaultJVMPath(), "-ea", "-Djava.class.path=" + self.jar_location)
        # print(isJVMStarted())

    def set_lte_property(self, package_name="infodynamics.measures.continuous.kraskov", k=3):
        # Create a TE calculator and run it:
        te_calc_class = JPackage(package_name).TransferEntropyCalculatorMultiVariateKraskov
        self.teCalc = te_calc_class()  # te_calc_class.COND_MI_CALCULATOR_KRASKOV2
        self.teCalc.setProperty("PROP_K", '3')  # Use Kraskov parameter K=4 for 4 nearest points
        self.teCalc.setProperty("PROP_KRASKOV_ALG_NUM", "1")
        self.teCalc.setProperty("NOISE_LEVEL_TO_ADD", "1e-18")
        # self.teCalc.initialise(k, source_k, dest_k)
        print(self.teCalc.props)
        return self

    def compute_lte(self, source, dest):
        # Perform calculation with correlated source:
        if not len(source) or not len(dest):
            print("ERROR!!")
            return
        source_k = len(source[0])
        dest_k = len(dest[0])

        self.teCalc.initialise(1, source_k, dest_k)
        self.teCalc.setObservations(source, dest)
        result1 = self.teCalc.computeAverageLocalOfObservations()
        result = self.teCalc.computeLocalOfPreviousObservations()
        print(result1)
        print(result)

        self.teCalc.initialise(1, dest_k, source_k)
        self.teCalc.setObservations(dest, source)
        result2 = self.teCalc.computeAverageLocalOfObservations()
        result = self.teCalc.computeLocalOfPreviousObservations()
        print(result2)
        print(result)
        return result1, result2

    def close(self):
        shutdownJVM()


class LocalTransferEntropyPy:
    def __init__(self):
        self.teCalc = TECalculatorMultiVarKraskov()

    def set_properties(self, **kwargs):
        self.teCalc.set_property("k", "3")
        self.teCalc.set_property("normtype", "np.inf")
        self.teCalc.set_property("PROP_KRASKOV_ALG_NUM", "1")
        self.teCalc.set_property("PROP_ADD_NOISE", "1e-18")
        for i in kwargs:
            self.teCalc.set_property(str(i), str(kwargs.get(i)))
        return self

    def compute_lte(self, source, dest):
        if not len(source) or not len(dest):
            raise Exception("Length of source or destination is 0. ")
        source_k = len(source[0])
        dest_k = len(dest[0])

        self.teCalc.initialise(source_k, dest_k, 1, 1, 1, 1, 1)
        self.teCalc.set_observations(source, dest)
        result1 = self.teCalc.compute_average_local()
        result = self.teCalc.compute_local()
        print(result1)
        print(result)

        self.teCalc.initialise(dest_k, source_k, 1, 1, 1, 1, 1)
        self.teCalc.set_observations(dest, source)
        result2 = self.teCalc.compute_average_local()
        result = self.teCalc.compute_local()
        print(result2)
        print(result)
        return result1, result2

if __name__ == '__main__':
    a = [[1., 550., 1.], [0., 450., 1.], [0., 0., 0.], [0., 0., 1.], [0., 0., 0.], [0., 0., 1.], [0., 0., 0.], [0., 0., 1.],
         [0., 0., 0.], [0., 200., 1.], [0., 10., 0.], [0., 0., 1.], [0., 0., 0.], [0., 0., 1.], [0., 0., 0.], [0., 0., 1.], [0., 0., 0.],
         [0., 0., 1.], [0., 0., 0.], [0., 0., 1.], [0., 0., 0.], [0., 0., 1.], [0., 0., 0.], [0., 0., 1.], [0., 0., 0.], [0., 0., 1.],
         [0., 0., 0.], [0., 0., 1.], [0., 0., 0.], [0., 0., 0.]]
    b = [[4., 1., 0.], [0., 1., 5.], [6., 1., 1.], [0., 0., 1.], [0., 0., 0.], [0., 0., 1.], [0., 0., 0.], [0., 0., 1.], [0., 0., 0.],
         [0., 0., 1.], [0., 0., 0.], [0., 0., 1.], [0., 0., 0.], [0., 0., 1.], [0., 0., 0.], [0., 0., 1.], [0., 0., 0.], [0., 0., 1.],
         [0., 0., 0.], [0., 55., 1.], [0., 0., 0.], [0., 0., 1.], [0., 0., 0.], [0., 0., 1.], [0., 0., 0.], [0., 0., 1.],
         [0., 0., 0.], [0., 0., 1.], [0., 0., 0.], [0., 0., 1.]]
    c = [[4., 1., 0.], [0., 1., 5.], [6., 1., 1.], [0., 0., 1.], [0., 0., 0.], [0., 0., 1.], [0., 0., 0.], [0., 0., 1.],
         [0., 0., 0.],
         [0., 0., 1.], [0., 0., 0.], [0., 0., 1.], [0., 0., 0.], [0., 0., 1.], [0., 0., 0.], [0., 0., 1.], [0., 0., 0.],
         [0., 0., 1.],
         [0., 0., 0.], [0., 55., 1.], [0., 0., 0.], [0., 0., 1.], [0., 0., 0.], [0., 0., 1.], [0., 0., 0.],
         [0., 0., 1.],
         [0., 0., 0.], [0., 0., 1.], [0., 0., 0.], [0., 0., 1.]]
    lte = LocalTransferEntropy(jar_location="../lib/infodynamics.jar").set_lte_property()
    lte.calculate_lte(a, b)
    lte.calculate_lte(b, a)
    lte.calculate_lte(b, c)
    # lte.experiment()
    # lte.close()
