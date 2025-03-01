from bee import Bee
from fitnessFunction import FitnessFunction
from resources import FitnessF

class NAttractors(FitnessFunction):
    def __init__(self, attractors, nodes, fixed_points, types):
        super().__init__(nodes, types)
        self.nr_of_points = attractors
        self.fixed_points = fixed_points
        self.tot_found = 0
        self.score = [0] * self.nr_of_points

    def _common_evaluate(self, solution, synch_update):
        pnts = self.get_nr_of_points()
        stts = self.get_total_configs()

        self.find_attractors(solution, synch_update)
        fitness = self.calculate_fitness()

        return fitness
    
    def evaluate(self, solution, synch_update):
        fitness, _ = self._common_evaluate(solution, synch_update)
        solution.set_fitness(fitness)

    def evaluate_display(self, solution: Bee, synch_update):
        fitness = self._common_evaluate(solution, synch_update)
        solution.set_fitness(fitness)

        print(f"Fitness = {fitness}, total fixed points found = {self.tot_found}\n")
        print(f"Total number of edges = {solution.get_edges()}\n")
        print("Distribution of fixed points: \n")

        point_names = [
            "Sepal: [0 0 0 1 0 0 0 0 0 0 0 0]",
            "Petal: [0 0 0 1 0 0 0 1 0 1 1 0]",
            "Carpel: [0 0 0 0 0 0 0 0 1 0 0 0]",
            "Stamen: [0 0 0 0 0 0 0 1 1 1 1 0]",
            "Inflorescence: [1 1 0 0 0 0 0 0 0 0 0 0]",
            "Mutant: [1 1 0 0 0 0 0 1 0 1 1 0]"
            ]
        
        for i, name in enumerate(point_names):
            print(f"{name} = {self.score[i]}")

    def calculate_fitness(self):
        print("Calculate Fitness")
        pnts = self.get_nr_of_points()
        stts = self.get_total_configs()

        for state in self.states_list:
            for j, fixed_point in enumerate(self.fixed_points):
                if state == fixed_point:
                    self.score[j] += 1
                    break
            
        self.tot_found = 0
        differences = 0.0

        if self.get_funct_type() == FitnessF.ATTRACT_MATR:
            for i in range(pnts):
                self.tot_found = self.score[i]
                for j in range(pnts):
                    differences += abs(self.score[i] - self.score[j])

            den = differences / (self.tot_found + 1.0)
            fitness = -self.tot_found / (den + 1.0)
        
        elif self.get_funct_type() == FitnessF.ATTRACT_OPT:
            optimal = stts / pnts
            for i in range(pnts):
                self.tot_found += self.score[i]
                differences += abs(self.score[i] - optimal)
            fitness = -((2.0 * stts - differences) / 2.0)
        
        else:
            raise ValueError("Non-existent attractor fitness function called")
        
        return fitness

    def get_nr_of_points(self):
        return self.nr_of_points
    
    def get_fixed_point(self, point):
        value = 0

        if point >= self.get_nr_of_points():
            raise IndexError(f"Fixed point {point} out of bounds")
        else:
            value = self.fixed_points[point]
        return value