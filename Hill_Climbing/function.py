import numpy as np
import random

class UtilityFunc:

    values = None   # numpy array
    index = 0   #int
    length = 0  #int

    def __init__(self,Values) -> None:
        super().__init__()

        if isinstance(Values,np.ndarray):
            self.values = Values
            self.length = Values.shape[0]
        elif isinstance(Values,str):
            self.readfromfile(Values)
            self.length = self.values.shape[0]

    def readfromfile(self,fileName):
        file = open(fileName, 'r')
        self.values = np.loadtxt(file, delimiter=',')

    def randomizeindex(self):
        self.index = random.randint(0,self.length-1)

    def evaluate_at_index(self):
        return self.values[self.index,1]

    def return_x_value(self):
        return self.values[self.index,0]

    def set_index(self,x):
        if x >= self.length or x < 0:
            return False
        self.index = x
        return True

    def increment_index(self, x):
        if (self.index + x) >= self.length:
            return
        else:
            self.index += x

    def decrement_index(self, x):
        if (self.index - x) < 0:
            return
        else:
            self.index -= x

    def step_index_up(self):
        self.increment_index(1)

    def step_index_down(self):
        self.decrement_index(1)


class BackendAgnosticUtilityFunc(UtilityFunc):

    request_freq = 0 # frequency of requests for this service

    def __init__(self, Values, freq) -> None:
        super().__init__(Values)
        if freq > 0:
            self.request_freq = freq
        else:
            self.request_freq = 0

    def evaluate_at_index(self):
        #print("Hey " + str(self.index))
        tmp = self.request_freq * (1 - self.values[self.index, 1])
        return tmp
