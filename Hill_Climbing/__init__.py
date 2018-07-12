import numpy as np
import sys
from function import UtilityFunction, BackendAgnosticUtilityFunction
from hillClimb import *
from collections import OrderedDict

import redis


def getCurves():

    list_of_mrc_files = []
    for e in range (1,9):
        #name = ("C:\\Users\\jorge\\PycharmProjects\\Optimization\\data\\Miss_Rate_Curves\\MRC_epoch_00001_slab_0%d.csv"%(e))
        name = "/home/jorge/optimization/data/Miss_Rate_Curves/MRC_epoch_00001_slab_0%d.csv"%(e)
        list_of_mrc_files.append(name)
    #g = open("C:\\Users\\jorge\\PycharmProjects\\Optimization\\data\\Miss_Rate_Curves\\MRC_epoch_00001_slab_01.csv", "r")



    MRC_curves =[]

    for e in list_of_mrc_files:
        file = open(e,'r')
        tmp_array =np.loadtxt(file, delimiter=',')
        MRC_curves.append(tmp_array)

    return MRC_curves

def getMRCcurves():
    list_of_mrc_files = sys.argv[1:]

    MRC_curves = []
    Redis_instance_dict = {}



    for e in list_of_mrc_files:
        file = open(e, 'r')
        print(file.readline())
        #tmp_array = np.loadtxt(file, delimiter=',', skiprows=1)
        tmp_array = np.loadtxt(file, delimiter=',')
        print(tmp_array)
        MRC_curves.append(tmp_array)

    return MRC_curves


def getMRCcurves2():
    list_of_mrc_files = sys.argv[1:]

    MRC_curves = []
    Redis_instance_dict = {}

    for e in list_of_mrc_files:

        tmp_dict={}

        file = open(e, 'r')
        id = int(file.readline().split(':')[1])
        freq = int(file.readline().split(':')[1])

        tmp_dict['frequency'] = freq
        tmp_array = np.loadtxt(file, delimiter=',')
        tmp_dict['mrc'] = tmp_array

        Redis_instance_dict[id] = tmp_dict
        #print(tmp_array)


    return Redis_instance_dict
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~`


for e in sys.argv[1:]:
    print(e)

HOST = "127.0.0.1"


MRC_files = getMRCcurves2()

weight = 1
frequency = 1
#Total_memory is given in bytes
Total_memory = 524288000 # 500MB
#Total_memory = 1048576000 #1000 MB
redis_instances = OrderedDict()

#total number of keys across all Redis instances
total_objects = 0

#total memory used by the datasets across all Redis instances
cumulative_memory = 0

for k, v in MRC_files.items():
    instance = {}
    instance["function"]= BackendAgnosticUtilityFunction(v['mrc'], v['frequency'])
    weight+=0
    instance["weight"] = weight
    port = k

    r = redis.Redis(host=HOST, port=port)
    _dbsize = r.dbsize()
    # Add the number of keys in this Redis instance to the total count
    total_objects += _dbsize

    instance['dbsize'] = _dbsize
    print("PORT: " + str(port))

    _info = r.info(section="memory")

    dataset_size = _info['used_memory_dataset']
    #Add the amount of memory used by this Redis dataset to the total amount
    cumulative_memory += dataset_size
    per_datum_size = float(dataset_size) / _dbsize

    instance['dataset_size'] = dataset_size
    instance['per_datum_size'] = per_datum_size

    print("Average object size: " + str(per_datum_size))
    print(instance)
    redis_instances[port] = instance

print(redis_instances)

#average_memory_per_object = float(cumulative_memory)/total_objects

print("Total objects across all instances: " + str(total_objects))

average_memory_per_object = float(cumulative_memory)/total_objects
print("Average size of each object: " + str(average_memory_per_object))

for k in redis_instances.keys():
    first_port = k
    print(k)
    break
print("First port: " + str(first_port))

#x = HillClimbingSolverRedis(MRCs, int(total_objects_per_system))

Total_blocks_solver = int(Total_memory / average_memory_per_object)
print("Number of blocks for the solver: %f" % (Total_blocks_solver))
solver = HillClimbingSolver( Total_blocks_solver)

min_memory = 0

for key in redis_instances:

    solver.add_function(redis_instances[key]["function"],key,min_memory)



print("Solver!!!")

solution = solver.search_max_with_ids()
Optimized_blocks = [x[1] for x in solution]
print(Optimized_blocks)

print("Solved!!")
print("Block allocation: " + str(Optimized_blocks))
print("Value of sumation function: " + str(solver.evaluate_list(Optimized_blocks)))
print("Total Blocks = %d" % ( sum(solver.get_x_values( Optimized_blocks ) )))
#Remaining memory after allocation (in certain cases not all the memory is partitioned, when the MRCs have few lines with small sizes for cache memory)
remaining = int(Total_blocks_solver - sum(solver.get_x_values( Optimized_blocks )))
print("Remaining blocks: %d"%(remaining))
#added_blocks is the amount of extra blocks that each instance gets when
added_blocks = int(remaining / len(Optimized_blocks))
print("Extra blocks per instance: %d"%(added_blocks))
print("\n")
for e in solution:

    r = redis.Redis(host=HOST, port=e[0])

    print("Instance with port: " + str(e[0]))


    if added_blocks > 1:
        alloc = int(e[1]) + added_blocks
    else:
        alloc = int(e[1])
    # This shows how many 'blocks' we should allocate to each Redis instance
    print("Block allocation: " + str(alloc))
    # This shows how much memory we should allocate to each Redis instance
    Total_blocks_solver =  int(alloc * average_memory_per_object)

    print("New memory: %d  (%f  mb)" % (Total_blocks_solver, float(Total_blocks_solver) / 1024 / 1024))
    r.config_set("maxmemory", str(Total_blocks_solver))
    print("\n")
    





