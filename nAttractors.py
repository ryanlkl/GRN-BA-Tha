from bee import Bee
from fitnessFunction import FitnessFunction
from resources import FitnessF

class NAttractors(FitnessFunction):
    def __init__(self, attractors, nodes, fixed_points, type):
        super().__init__(nodes, type)
        self.nr_of_points = attractors
        self.fixed_points = fixed_points
        self.tot_found = 0

    def evaluate(self, solution, synch_update):
        pnts = self.get_nr_of_points()
        stts = self.get_total_configs()
        fitness = 0.0
        states_list = [0] * stts
        score = [0] * pnts

        self.find_attractors(solution, synch_update, states_list)
        fitness = self.calculate_fitness(states_list, score, self.tot_found)

        solution.set_fitness(fitness)

    def get_nr_of_points(self):
        return self.nr_of_points
    
    def get_fixed_point(self, point):
        if point >= self.get_nr_of_points():
            raise IndexError(f"Fixed point {point} out of bounds")
        else:
            value = self.fixed_points[point]
        return value
    
    def evaluate_display(self, solution: Bee, synch_update):
        nds = solution.get_number_of_nodes()
        pnts = self.get_nr_of_points()
        stts = self.get_total_configs()
        states_list = [0] * stts
        score = [0] * pnts

        self.find_attractors(solution, synch_update, states_list)
        fitness = self.calculate_fitness(states_list, score, self.tot_found)

        solution.set_fitness(fitness)

        print(f"Fitness = {fitness}, total fixed points found = {self.tot_found}\n")
        print(f"Total number of edges = {solution.get_edges()}\n")
        print("Distribution of fixed points: \n")
        print(f"Sepal: [0 0 0 1 0 0 0 0 0 0 0 0] = {score[0]}\n")
        print(f"Petal: [0 0 0 1 0 0 0 1 0 1 1 0] = {score[1]}\n")
        print(f"Carpel: [0 0 0 0 0 0 0 0 1 0 0 0 ] = {score[2]}\n")
        print(f"Stamen: [0 0 0 0 0 0 0 1 1 1 1 0] = {score[3]}\n")
        print(f"Inflorescence: [1 1 0 0 0 0 0 0 0 0 0 0] = {score[4]}\n")
        print(f"Mutant: [1 1 0 0 0 0 0 1 0 1 1 0] = {score[5]}\n")

    def calculate_fitness(self, states_list, score, tot_found):
        pnts = self.get_nr_of_points()
        stts = self.get_total_configs()

        for i in range(pnts):
            score[i] = 0

        for i in range(stts):
            stop = False
            j = 0
            while j < pnts and not stop:
                if states_list[i] == self.get_fixed_point(j):
                    score[j] += 1
                    stop = True
        
        self.tot_found = 0
        differences = 0.0

        if self.get_funct_type() == FitnessF.ATTRACT_MATR:
            for i in range(pnts):
                self.tot_found += score[i]
                for j in range(pnts):
                    differences += abs(score[i] - score[j])

            den = differences / (self.tot_found + 1.0)
            fitness = -self.tot_found / (den + 1)
        elif self.get_funct_type() == FitnessF.ATTRACT_OPT:
            optimal = stts / pnts
            for i in range(pnts):
                self.tot_found += score[i]
                differences += abs(score[i] - optimal)
            fitness = -((2.0 * stts - differences) / 2.0)
        else:
            raise ValueError("Non existent attractor fitness functin called")
        
        return fitness