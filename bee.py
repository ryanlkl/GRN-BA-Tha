import random

class Bee:
    def __init__(self, number_of_nodes, minimum, maximum, stlim, ngh):
        self.nodes = number_of_nodes
        self.edges = 0
        self.extremes = [minimum, maximum]
        self.adj_matrix = [[0] * number_of_nodes for _ in range(number_of_nodes)]
        self.thr_vector = [0] * number_of_nodes
        self.random_seed_GRN()
        self.ttl = stlim
        self.ngh_size = ngh
        self.recruited = 0
        self.fitness = 0.0

    def random_seed_grn(self):
        self.reinit_adj_matrix()
        self.reinit_thr_vector()

    def reinit_adj_matrix(self):
        nds = self.get_number_of_nodes()
        minimum = self.get_lower_extreme()
        maximum = self.get_upper_extreme()

        for i in range(nds):
            for j in range(nds):
                random_no = random.randint(0,3)
                if random_no == 0:
                    self.set_adj_matrix_element(i, j, random.randint(minimum, maximum))
                else:
                    self.set_adj_matrix_element(i, j, 0)

    def set_adj_matrix_element(self, row, column, new_value):
        old_value = self.get_adj_matrix_element(row, column)

        if row >= self.get_number_of_nodes():
            raise IndexError("Adjacent Matrix row index overflown")
        elif column >= self.get_number_of_nodes():
            raise IndexError("Adjacent Matrix column index overflown")
        elif new_value > self.get_upper_extreme() or new_value < self.get_lower_extreme():
            raise IndexError("Adjacent Matrix value out of boundary")
        else:
            self.adj_matrix[row][column] = new_value

        if old_value == 0 and new_value != 0:
            self.increment_edges()
        elif old_value != 0 and new_value == 0:
            self.decrement_edges()

    def reinit_thr_vector(self):
        nds = self.get_number_of_nodes()
        minimum = self.get_lower_extreme()
        maximum = self.get_upper_extreme()

        for i in range(nds):
            random_no = random.randint(0,3)
            if random_no == 0:
                self.set_thr_vector_element(i, random.randint(minimum, maximum))
            else:
                self.set_thr_vector_element(i, 0)

    def read_target(self, file_target: str):
        number_of_nodes = self.get_number_of_nodes()
        try:
            with open(file_target, "r") as infile:
                for i in range(number_of_nodes):
                    for j in range(number_of_nodes):
                        temp = int(infile.readline().strip())
                        self.set_adj_matrix_element(i,j,temp)
                
                for i in range(number_of_nodes):
                    temp = int(infile.readline().strip())
                    self.set_thr_vector_element(i, temp)
        except FileNotFoundError:
            raise FileNotFoundError("Can't open target GRN file")
        
    def set_thr_vector_element(self, element, new_value):
        if element >= self.get_number_of_nodes():
            raise IndexError("Out of bound ThrVector element")
        elif new_value > self.get_upper_extreme() or new_value < self.get_lower_extreme():
            raise IndexError("Adjacent Matrix value out of boundary")
        else:
            self.thr_vector[element] = new_value
    
    def get_number_of_nodes(self):
        return self.nodes
    
    def get_lower_extreme(self):
        return self.extremes[0]
    
    def get_upper_extreme(self):
        return self.extremes[1]
    
    def get_adj_matrix_element(self, row, column):
        output = 0

        if row >= self.get_number_of_nodes():
            raise IndexError("Adjacent Matrix row index overflown")
        elif column >= self.get_number_of_nodes():
            raise IndexError("Adjacent Matrix column index overflown")
        else:
            output = self.adj_matrix[row][column]
        
        return output
    
    def get_thr_vector_element(self, element):
        output = 0

        if element >= self.get_number_of_nodes():
            raise IndexError("Out of bound ThrVector element")
        else:
            output = self.thr_vector[element]
        
        return output
    
    def count_edges(self):
        nodes = self.get_number_of_nodes()
        self.edges = 0

        for i in range(nodes):
            for j in range(nodes):
                if self.get_adj_matrix_element(i,j) != 0:
                    self.edges += 1

    def increment_edges(self):
        self.edges += 1

    def decrement_edges(self):
        self.edges -= 1

    def get_edges(self):
        return self.edges
    
    def set_ngh_size(self, size):
        self.ngh_size = size

    def decrease_ngh_size(self):
        if self.ngh_size > 2:
            self.ngh_size -= 1

    def get_ngh_size(self):
        return self.ngh_size
    
    def set_ttl(self, remaining):
        self.ttl = remaining

    def decrease_ttl(self):
        if self.ttl > 0:
            self.ttl -= 1

    def get_ttl(self):
        return self.ttl
    
    def set_fitness(self, evaluation):
        self.fitness = evaluation

    def get_fitness(self):
        return self.fitness
    
    def set_recruited(self, foragers):
        self.recruited = foragers

    def get_recruited(self):
        return self.recruited
    
    def synch_next_state(self, current_state, next_state):
        nds = self.get_number_of_nodes()

        for i in range(nds):
            total = 0
            for j in range(nds):
                total += self.get_adj_matrix_element(i,j) * current_state[j]
            
            total -= self.get_thr_vector_element(i)
            next_state[i] = total > 0

    def asynch_next_state(self, current_state, next_state):
        nds = self.get_number_of_nodes()
        temp_state = [False] * nds

        # EMF1, TFL1
        for i in range(nds):
            temp_state[i] = next_state[i] = current_state[i]

        for i in range(2):
            total = 0
            for j in range(nds):
                total += self.get_adj_matrix_element(i,j) * temp_state[j]
            total -= self.get_thr_vector_element(i)
            next_state[i] = total > 0

        # LFY, AP1, CAL
        for i in range(2):
            temp_state[i] = next_state[i]

        for i in range(2, 5):
            total = 0
            for j in range(nds):
                total += self.adj_matrix_element(i,j) * temp_state[j]
            
            total -= self.get_thr_vector_element(i)
            next_state[i] = total > 0

        # LUG, UFO, BFU
        for i in range(2, 5):
            temp_state[i] = next_state[i]

        for i in range(5, 8):
            total = 0
            for j in range(nds):
                total += self.get_adj_matrix_element(i,j) * temp_state[j]
            total -= self.get_thr_vector_element(i)
            next_state[i] = total > 0

        # AG, AP3, PI
        for i in range(5,8):
            temp_state[i] = next_state[i]

        for i in range(8, 11):
            total = 0
            for j in range(nds):
                total += self.get_adj_matrix_element(i,j) * temp_state[j]

            total -= self.get_thr_vector_element(i)
            next_state[i] = total  > 0

        # SUP.
        total = 0
        for j in range(nds):
            total += self.get_adj_matrix_element(11,j) * next_state[j]

        total -= self.get_thr_vector_element(11)
        next_state[11] = total > 0

    def create_copy(self):
        # Create and return a copy of the current Bee instance
        copy = Bee(self.nodes, self.extremes[0], self.extremes[1], self.ttl, self.ngh_size)
        copy.adj_matrix = [row[:] for row in self.adj_matrix]
        copy.thr_vector = self.thr_vector[:]
        copy.set_fitness(self.fitness)
        copy.set_recruited(self.recruited)
        return copy


