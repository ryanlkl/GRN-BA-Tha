from fitnessFunction import FitnessFunction
from bee import Bee

class ReducedMAB(FitnessFunction):
    def __init__(self, number_of_nodes, target_GRN, type):
        super().__init__(number_of_nodes, type)
        self.target = target_GRN

    def evaluate(self, solution: Bee, synch_update):
        nds = solution.get_number_of_nodes()
        stts = self.get_total_configs()
        current_config = None
        next_config = [False] * nds
        next_target_config = [False] * nds
        fitness = 0.0


        for i in range(stts):
            current_config = self.get_state(i)
            if synch_update:
                solution.synch_next_state(current_config, next_config)
                self.get_target().synch_next_state(current_config, next_target_config)
            else:
                solution.asynch_next_state(current_config, next_config)
                self.get_target().asynch_next_state(current_config, next_target_config)
            
            for j in range(nds):
                fitness += abs(next_config[j] - next_target_config[j])

        solution.set_fitness(fitness / nds)

    def get_target(self):
        return self.target