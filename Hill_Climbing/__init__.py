import numpy as np
from function import UtilityFunc, BackendAgnosticUtilityFunc
from hillClimb import *

def getCurves():

    list_of_mrc_files = []
    for e in range (1,9):
        name = ("C:\\Users\\jorge\\PycharmProjects\\Optimization\\data\\Miss_Rate_Curves\\MRC_epoch_00001_slab_0%d.csv"%(e))
        list_of_mrc_files.append(name)
    #g = open("C:\\Users\\jorge\\PycharmProjects\\Optimization\\data\\Miss_Rate_Curves\\MRC_epoch_00001_slab_01.csv", "r")



    MRC_curves =[]

    for e in list_of_mrc_files:
        file = open(e,'r')
        tmp_array =np.loadtxt(file, delimiter=',')
        MRC_curves.append(tmp_array)

    return MRC_curves

MRC_files = getCurves()
MRCs = []
counter = 1
frequency = 1

for e in MRC_files:
    MRCs.append( (BackendAgnosticUtilityFunc(e, frequency), counter) )
    counter+=20

x = HillClimbingSolver(MRCs, 1000000)

print(x.evaluate_function())
#x.rand_indeces()
print(x.evaluate_function())

print("Solver!!!")

y = x.search_max()

print("Solved!!")
print(y)
print(x.evaluate_function())
print("Total Memory = %d"%(x.get_sum_of_x()))


z = x.search_min()
print("Solved again!!")
print(z)

print(x.evaluate_function())

