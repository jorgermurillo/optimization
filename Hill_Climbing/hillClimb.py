from function import UtilityFunc
class HillClimbingSolver:

    utilityFunctions = None # List of tuples!
    max_memory = 0

    def __init__(self, list, max_memory):
        super().__init__()
        # list should be a list of tuples (UtilityFunction, float)
        for e in list:
            # assert( issubclass(e[0],UtilityFunc) )
            #e[0].randomizeindex()
            e[0].set_index(0)
            try:
                float(e[1])
            except TypeError:
                print("Error with the Type of one of the weights")
        self.utilityFunctions = list
        self.max_memory = max_memory
        #print("Sum of x values: %f"%(self.get_sum_of_x()))
        # Initialize the indices of each function
        while True:
            #print("H")
            for e in list:
                # assert( issubclass(e[0],UtilityFunc) )

                #e[0].randomizeindex()
                e[0].set_index(0)
            if self.get_sum_of_x() <= self.max_memory:
                break


        list = None


    def rand_indeces(self):
        if len(self.utilityFunctions) == 0:
            return
        for e in self.utilityFunctions:
            e[0].randomizeindex()

    def search_max(self):
        if len(self.utilityFunctions) == 0:
            return

        index_changed = False

        current_max = self.evaluate_function()
        current_state = [x[0].index for x in self.utilityFunctions]
        candidate_values = [x[0].index for x in self.utilityFunctions]
        candidate_max_value = float("-inf")

        while True:
            for e in self.utilityFunctions:
                e[0].step_index_up()
                tmp = self.evaluate_function()
                # check whether the change increased the sum of utility functions and whether the mx amount of memory
                # surpassed
                if tmp > current_max and self.get_sum_of_x() <= self.max_memory and tmp > candidate_max_value:
                    #print("sum of x values: %7d \nValue of function: %4f."%(self.get_sum_of_x(),self.evaluate_function()))
                    candidate_values = [x[0].index for x in self.utilityFunctions]
                    index_changed = True
                    candidate_max_value = tmp
                e[0].step_index_down()

            for e in self.utilityFunctions:
                e[0].step_index_down()
                tmp = self.evaluate_function()
                if tmp > current_max and self.get_sum_of_x() <= self.max_memory and tmp > candidate_max_value:
                    #print("sum of x values: %7d \nValue of function: %4f."%(self.get_sum_of_x(),self.evaluate_function()))
                    candidate_values = [x[0].index for x in self.utilityFunctions]
                    index_changed = True
                    candidate_max_value = tmp
                e[0].step_index_up()

            if index_changed:
                for i in range(len(self.utilityFunctions)):
                    self.utilityFunctions[i][0].index = candidate_values[i]

                current_state = candidate_values
                #print(current_state)
                current_max = self.evaluate_function()
                index_changed = False
            else:
                # Iteration is over
                r = [x[0].return_x_value() for x in self.utilityFunctions]
                # Here we are leaving the index of each function to the value that maximizes the sum
                for i in range(len(self.utilityFunctions)):
                    self.utilityFunctions[i][0].index = current_state[i]
                #current_state are the indeces of each function, NOT the x values
                return current_state
                #return r

    def search_min(self):
        if len(self.utilityFunctions) == 0:
            return

        index_changed = False

        current_min = self.evaluate_function()
        current_state = [x[0].index for x in self.utilityFunctions]
        candidate_values = [x[0].index for x in self.utilityFunctions]
        candidate_min_value = float("inf")

        while True:
            for e in self.utilityFunctions:
                e[0].step_index_up()
                tmp = self.evaluate_function()
                # check whether the change increased the sum of utility functions and whether the mx amount of memory
                # surpassed
                if tmp < current_min and self.get_sum_of_x() <= self.max_memory and tmp < candidate_min_value:
                    #print("sum of x values: %7d \nValue of function: %4f."%(self.get_sum_of_x(),self.evaluate_function()))
                    candidate_values = [x[0].index for x in self.utilityFunctions]
                    index_changed = True
                    candidate_min_value = tmp
                e[0].step_index_down()

            for e in self.utilityFunctions:
                e[0].step_index_down()
                tmp = self.evaluate_function()
                if tmp < current_min and self.get_sum_of_x() <= self.max_memory and tmp < candidate_min_value:
                    #print("sum of x values: %7d \nValue of function: %4f."%(self.get_sum_of_x(),self.evaluate_function()))
                    candidate_values = [x[0].index for x in self.utilityFunctions]
                    index_changed = True
                    candidate_min_value = tmp
                e[0].step_index_up()

            if index_changed:
                for i in range(len(self.utilityFunctions)):
                    self.utilityFunctions[i][0].index = candidate_values[i]

                current_state = candidate_values
                #print(current_state)
                current_max = self.evaluate_function()
                index_changed = False
            else:
                # Iteration is over
                r = [x[0].return_x_value() for x in self.utilityFunctions]
                # Here we are leaving the index of each function to the value that maximizes the sum
                for i in range(len(self.utilityFunctions)):
                    self.utilityFunctions[i][0].index = current_state[i]

                return current_state
                #return r


    def get_sum_of_x(self):
        sum = 0
        for e in self.utilityFunctions:
            sum += e[0].return_x_value()
        return sum

    def get_x_values(self):
        x_values = [x[0].return_x_value() for x in self.utilityFunctions]
        return x_values

    def evaluate_function(self):
        sum = 0
        for e in self.utilityFunctions:
            sum += (e[0].evaluate_at_index())*e[1]
        return sum

class HillClimbingSolverRedis(HillClimbingSolver):

    def search_max(self):
        if len(self.utilityFunctions) == 0:
            return

        index_changed = False

        current_max = self.evaluate_function()
        current_state = [x[0].index for x in self.utilityFunctions]
        candidate_values = [x[0].index for x in self.utilityFunctions]
        candidate_max_value = float("-inf")

        while True:
            for e in self.utilityFunctions:
                e[0].step_index_up()
                tmp = self.evaluate_function()
                # check whether the change increased the sum of utility functions and whether the mx amount of memory
                # surpassed
                if tmp > current_max and self.get_sum_of_x() <= self.max_memory and tmp > candidate_max_value:
                    #print("sum of x values: %7d \nValue of function: %4f."%(self.get_sum_of_x(),self.evaluate_function()))
                    candidate_values = [x[0].index for x in self.utilityFunctions]
                    index_changed = True
                    candidate_max_value = tmp
                e[0].step_index_down()

            for e in self.utilityFunctions:
                e[0].step_index_down()
                tmp = self.evaluate_function()
                if tmp > current_max and self.get_sum_of_x() <= self.max_memory and tmp > candidate_max_value:
                    #print("sum of x values: %7d \nValue of function: %4f."%(self.get_sum_of_x(),self.evaluate_function()))
                    candidate_values = [x[0].index for x in self.utilityFunctions]
                    index_changed = True
                    candidate_max_value = tmp
                e[0].step_index_up()

            if index_changed:
                for i in range(len(self.utilityFunctions)):
                    self.utilityFunctions[i][0].index = candidate_values[i]

                current_state = candidate_values
                #print(current_state)
                current_max = self.evaluate_function()
                index_changed = False
            else:
                # Iteration is over


                # Here we are leaving the index of each function to the value that maximizes the sum
                for i in range(len(self.utilityFunctions)):
                    self.utilityFunctions[i][0].index = current_state[i]

                r = [(x[0].service_id,x[0].return_x_value()) for x in self.utilityFunctions]

                #current_state are the indeces of each function, NOT the x values
                return r
                #return r
