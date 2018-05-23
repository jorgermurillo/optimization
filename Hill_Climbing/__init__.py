import numpy as np
import sys
from function import UtilityFunc, BackendAgnosticUtilityFunc
from hillClimb import *
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
MRCs = []
weight = 1
frequency = 1
#Total_memory is given in bytes
Total_memory = 524288000 # 500MB

redis_instances = {}

#total number of keys across all Redis instances
total_objects = 0

#total memory used by the datasets across all Redis instances
cumulative_memory = 0

for k, v in MRC_files.items():
    instance = {}
    MRCs.append( (BackendAgnosticUtilityFunc(v['mrc'], v['frequency'], k), weight) )
    weight+=0
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

#average_memory_per_object = float(cumulative_memory)/total_objects

print("Total objects across all instances: " + str(total_objects))

average_memory_per_object = float(cumulative_memory)/total_objects
print("Average size of each object: " + str(average_memory_per_object))

first_port = MRCs[0][0].service_id
print("First port: " + str(first_port))


'''
r = redis.Redis(host=HOST, port=first_port)
total_memory = r.info(section = "memory")['total_system_memory']
print("Total memory of the system: " + str(total_memory) )

total_objects_per_system = float(total_memory)/average_memory_per_object

print('Total objects per system: ' + str(total_objects_per_system))
print("Average memory per object: "+ str(average_memory_per_object))
'''
#x = HillClimbingSolverRedis(MRCs, int(total_objects_per_system))

memory = Total_memory/average_memory_per_object
print("Max memory (number of objects) for the solver: %f"%(memory))
x = HillClimbingSolverRedis(MRCs, memory)

print("Solver!!!")

Optimized_memories = x.search_max()

print("Solved!!")
print("Memory allocation: " + str(Optimized_memories))
print("Value of sumation function: " + str(x.evaluate_function()))
print("Total Blocks = %d"%(x.get_sum_of_x()))


print("\n")
for e in Optimized_memories:

    #r = redis.Redis(host=HOST, port=e[0])

    print("Instance with port: " + str(e[0]))



    alloc = int(e[1])
    # This shows how many 'blocks' we should allocate to each Redis instance
    print("Block allocation: " + str(alloc))
    # This shows how much memory we should allocate to each Redis instance
    memory =  int(alloc*average_memory_per_object)

    print("New memory: %d  (%f  mb)"%(memory, float(memory)/1024/1024))
    #r.config_set("maxmemory", str(memory))
    print("\n")



