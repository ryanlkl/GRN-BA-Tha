from fitnessFunction import FitnessFunction
from bee import Bee

class ReducedMAB(FitnessFunction):
    def __init__(self, number_of_nodes, target_GRN, types):
        super().__init__(number_of_nodes, types)
        self.target = target_GRN

    def evaluate(self, solution: Bee, synch_update):
        nds = solution.get_number_of_nodes()
        stts = self.get_total_configs()
        next_config = [False] * nds
        next_target_config = [False] * nds
        target = self.get_target()
        fitness = 0.0


        for i in range(stts):

            current_config = self.get_state(i)
            if synch_update:
                solution.synch_next_state(current_config, next_config)
                target.synch_next_state(current_config, next_target_config)
            else:
                solution.asynch_next_state(current_config, next_config)
                target.asynch_next_state(current_config, next_target_config)

            fitness += sum(next_config[j] != next_target_config[j] for j in range(nds))

        solution.set_fitness(fitness / nds)

    def get_target(self):
        return self.target