from bee import Bee
import numpy as np
from resources import bool_to_int, LSearch, FitnessF
import random
from nAttractors import NAttractors
from reducedMAB import ReducedMAB

class BeesAlgorithm_GRN:
    def __init__(self, file_name):
        self.T = 0
        self.ns = 0
        self.nb = 0
        self.ne = 0
        self.nrb = 0
        self.nre = 0
        self.ngh_shr = False
        self.init_ngh = 0
        self.min_ngh = 0
        self.stlim = 0
        self.sites = 0
        self.colony = None
        self.fitness_mab = None
        self.fitness_fixed_points = None
        self.best_fitness = 0
        self.solut_counter = 0
        self.synch_mode = True
        self.save_files = file_name
        self.search_threshold = 0
        self.save_threshold = 0
        self.search_type = LSearch.REINIT
        self.attr_type = FitnessF.TARGET
        self.number_of_attractors = 0

    def bees_alg_initialisation(self, file_BA_pars, file_GRN_pars):
        try:
            with open(file_BA_pars, "r") as infile_ba:
                self.T = int(infile_ba.readline().strip().split()[0])
                self.ns = int(infile_ba.readline().strip().split()[0])
                self.nb = int(infile_ba.readline().strip().split()[0])
                self.ne = int(infile_ba.readline().strip().split()[0])
                self.nrb = int(infile_ba.readline().strip().split()[0])
                self.nre = int(infile_ba.readline().strip().split()[0])
                self.ngh_shr = infile_ba.readline().strip().split()[0].lower() == "true"
                self.init_ngh = int(infile_ba.readline().strip().split()[0])
                self.min_ngh = int(infile_ba.readline().strip().split()[0])
                self.stlim = int(infile_ba.readline().strip().split()[0])
                self.synch_mode = infile_ba.readlin().strip().split()[0].lower() == "true"
                self.search_threshold = float(infile_ba.readline().strip().split()[0])
                self.save_threshold = float(infile_ba.readlin().strip().split()[0])
                self.search_type = infile_ba.readlin().strip().split()[0]

                if self.search_type not in ["delta", "reinit"]:
                    raise ValueError("Invalid SearchType parameter in BA_parameters")
        except FileNotFoundError:
            raise FileNotFoundError("Can't open BA parameter file")

        print("Read BA parameters:")
        print(f"T = {self.T}")
        print(f"ns = {self.ns}")
        print(f"nb = {self.nb}")
        print(f"ne = {self.ne}")
        print(f"nrb = {self.nrb}")
        print(f"nre = {self.nre}")
        print(f"nghShr = {self.ngh_shr}")
        if self.ngh_shr:
            print(f"initNgh = {self.init_ngh}")
            print(f"minNgh = {self.min_ngh}")
        else:
            print(f"ngh = {self.init_ngh}")
        print(f"stlim = {self.stlim}")
        print(f"synchMode = {self.synch_mode}")
        print(f"saveThreshold = {self.save_threshold}")
        print(f"local search = {self.search_type}\n")

        try:
            with open(file_GRN_pars, 'r') as infile_grn:
                number_of_nodes = int(infile_grn.readline().strip().split()[0])
                lower_extreme = int(infile_grn.readline().strip().split()[0])
                upper_extreme = int(infile_grn.readline().strip().split()[0])
        except FileNotFoundError:
            raise FileNotFoundError("Can't open GRN parameters file")
        
        print("Read GRN parameters:")
        print(f"nodes = {number_of_nodes}")
        print(f"lowerExtreme = {lower_extreme}")
        print(f"upperExtreme = {upper_extreme}")
        print(f"update mode = {'synchronous' if self.synch_mode else 'asynchronous'}\n")

        sts = self.nb + self.ns
        self.sites = sts
        self.colony = [Bee(number_of_nodes, lower_extreme, upper_extreme, self.stlim, self.init_ngh)] * sts

        self.reset_solut_counter()

    def read_attractors(self, file_attractors):
        nodes = self.get_colony_member(0).get_number_of_nodes()
        temp_point = [False] * nodes

        try:
            with open(file_attractors, "r") as infile:
                self.number_of_attractors = int(infile.readline().strip())
                fixed_points = [0] * self.number_of_attractors

                for i in range(self.number_of_attractors):
                    for j in range(nodes):
                        temp = int(infile.readline().strip())
                        temp_point[j] = temp
                    fixed_points[i] = bool_to_int(nodes, temp_point)

            return fixed_points
        except FileNotFoundError:
            raise FileNotFoundError("Can't open fixed points file")
        
    def set_obj_functions(self, target_file, attr_file):
        type_of_function = self.get_attr_type()
        fixed_points = None

        member = self.get_colony_member(0)
        target_bee = Bee(
            member.get_number_of_nodes(),
            member.get_lower_extreme(),
            member.get_upper_extreme(),
            target_file
            )
        self.fitness_mab = ReducedMAB(member.get_number_of_nodes(), target_bee, FitnessF.TARGET)

        if type_of_function == FitnessF.ATTRACT_MATR:
            fixed_points = self.read_attractors(attr_file)
            self.fitness_fixed_points = NAttractors(
                self.number_of_attractors,
                member.get_number_of_nodes(),
                fixed_points,
                type_of_function
                )
        elif type_of_function == FitnessF.ATTRACT_OPT:
            fixed_points = self.read_attractors(attr_file)
            self.fitness_fixed_points = NAttractors(
                self.number_of_attractors,
                member.get_number_of_nodes,
                fixed_points,
                type_of_function
                )
        else:
            raise ValueError("Call to non existent fitness function type in set_obj_function()")
        
    
    def pop_destructor(self):
        if self.colony is not None:
            self.colony = None

    def f_funct_destructor(self):
        self.fitness_mab = None
        self.fitness_fixed_points = None

    def get_T(self):
        return self.T
    
    def get_ns(self):
        return self.ns
    
    def get_nb(self):
        return self.nb
    
    def get_ne(self):
        return self.ne
    
    def get_nrb(self):
        return self.nrb
    
    def get_nre(self):
        return self.nre
    
    def get_ngh_shr(self):
        return self.ngh_shr
    
    def get_init_ngh(self):
        return self.init_ngh
    
    def get_min_ngh(self):
        return self.min_ngh
    
    def get_stlim(self):
        return self.stlim
    
    def get_sites(self):
        return self.sites
    
    def get_synch_mode(self):
        return self.synch_mode
    
    def get_search_threshold(self):
        return self.search_threshold
    
    def get_save_threshold(self):
        return self.save_threshold
    
    def get_search_type(self):
        return self.search_type
    
    def get_attr_type(self):
        return self.attr_type
    
    def set_colony_member(self, nr, member: Bee):
        if nr >= self.get_sites():
            raise IndexError("Size of colony exceeded")
        else:
            self.colony[nr] = member
    
    def get_colony_member(self, nr):
        if nr >= self.get_sites():
            raise IndexError("Size of colony exceeded")
        else:
            return self.colony[nr]
        
    def get_target_function(self):
        return self.fitness_mab
    
    def get_attract_function(self):
        return self.fitness_fixed_points
    
    def get_solut_counter(self):
        return self.solut_counter
    
    def reset_solut_counter(self):
        self.solut_counter = 0

    def increment_solut_counter(self):
        self.solut_counter += 1
    
    def set_solut_counter(self, solutions: int):
        self.solut_counter = solutions

    def set_best_fitness(self, new_best):
        self.best_fitness = new_best

    def get_best_fitness(self):
        return self.best_fitness
    
    def bees_algorithm(self):
        group_size = self.get_sites()
        cycles = self.get_T()

        try:
            with open("runFiles/results/progress.txt", "W") as progress_file:
                progress_file.write("iteration\tcurrent best\tbest-so-far\n")

                for i in range(group_size):
                    self.get_target_function().evaluate(self.get_colony_member(i), self.get_synch_mode)
                
                self.set_best_fitness(self.get_colony_member(0).get_fitness())
                self.bees_ranking()
                self.monitor_progress(progress_file, 0)

                for i in range(1, cycles):
                    print(f"Iteration: {i}")
                    for j in range(6):
                        member = self.get_colony_member(j)
                        print(f"Current {j}: error = {member.get_fitness()} - edges = {member.get_edges()} - ttl = {member.get_ttl()}\n")

                    print(f"Best found: error = {self.get_best_fitness()}\n\n")
                    self.waggle_dance()
                    self.local_search()
                    self.g_search()
                    self.site_abandonment()
                    self.bees_ranking()
                    self.monitor_progress(progress_file, i)

                thr = self.get_save_threshold()
                i = 0
                while i < group_size:
                    if self.get_colony_member(i).get_fitness() < thr:
                        self.save_solution(self.get_colony_member(i))
                    i += 1
        except FileNotFoundError:
            raise FileNotFoundError("Can't open 'progress' file")
        
    def bees_ranking(self):
        group_size = self.get_sites()
        temp_array = [None] * group_size

        for i in range(group_size):
            temp_array[i] = self.get_colony_member[i]

        cursor = 1
        while cursor < group_size:
            if temp_array[cursor].get_fitness() < temp_array[cursor - 1].get_fitness():
                j = 0
                while temp_array[j].get_fitness() < temp_array[cursor].get_fitness():
                    j += 1
                k = cursor
                while j < k:
                    temp_element = temp_array[k]
                    temp_array[k] = temp_array[k - 1]
                    temp_array[k - 1] = temp_element
                    k -= 1
                cursor += 1
            else:
                cursor += 1
        
        for i in range(group_size):
            self.set_colony_member(i, temp_array[i])
        
        if temp_array[0].get_fitness() < self.get_best_fitness():
            self.set_best_fitness(temp_array[0].get_fitness())

    def waggle_dance(self):
        elites = self.get_ne()
        bests = self.get_nb()
        elite_foragers = self.get_nre()
        best_foragers = self.get_nrb()

        for i in range(elites):
            self.get_colony_member(i).set_recruited(elite_foragers)
        
        for i in range(elites, bests):
            self.get_colony_member(i).set_recruited(best_foragers)

    def local_search(self):
        bests = self.get_nb()
        s_type = self.get_search_type()

        for s in range(bests):
            scout = self.get_colony_member(s)
            scout_fitness = scout.get_fitness()
            scout_edges = scout.get_edges()

            if s_type == LSearch.DELTA:
                new_scout = self.delta_search(scout)
            elif s_type == LSearch.REINIT:
                new_scout = self.reinitSearch(scout)
            else:
                raise ValueError("Wrong Lsearch type")
        
            if new_scout.get_fitness < scout_fitness:
                new_scout.set_ttl(self.get_stlim())
                self.set_colony_member(s, new_scout)
            elif new_scout.get_fitness() == scout_fitness and new_scout.get_edges() < scout_edges:
                new_scout.set_ttl(self.get_stlim())
                self.set_colony_member(s, new_scout)
            else:
                if self.get_ngh_shr() and scout.get_ngh_size() > self.get_min_ngh:
                    scout.decrease_ngh_size()
                scout.decrease_ttl()

    def reinit_search(self, scout: Bee):
        member = self.get_colony_member(0)
        nodes = member.get_number_of_nodes()
        minimum = member.get_lower_extreme()
        maximum = member.get_upper_extreme()
        scout_edges = scout.get_edges()
        neighbourhood = scout.get_ngh_size()
        s_threshold = self.get_search_threshold()
        new_scout = scout.create_copy()

        if scout.get_edges() == 0:
            scout.reinit_adj_matrix()

        o_funct = self.get_target_function()
        foragers = new_scout.get_recruited()
        scout_fitness = new_scout.get_fitness()

        for f in range(foragers):
            new_forager = new_scout.create_copy()
            for n in range(neighbourhood):
                random1 = random.randint(0,12)
                random2 = random.randint(0, nodes - 1)
                random3 = random.randint(0,4)
                if random3 == 0:
                    new_value = 0
                else:
                    new_value = random.randint(minimum, maximum)
                
                if random1 == 0:
                    new_forager.set_thr_vector_element(random2, new_value)
                else:
                    random3 = random.randint(0, nodes - 1)
                    new_forager.set_adj_matrix_element(random2, random3, new_value)
            o_funct.evaluate(new_forager, self.get_synch_mode())

            if new_forager.get_fitness() < scout_fitness:
                new_scout = new_forager
                scout_fitness = new_forager.get_fitness()
            elif new_forager.get_fitness() == scout_fitness and new_forager.get_edges() < scout_edges:
                new_scout = new_forager
            else:
                new_forager = None
        return new_scout
    
    def delta_search(self, scout: Bee):
        synch = self.get_synch_mode()
        scout_edges = scout.get_edges()
        foragers = scout.get_recruited()
        nr_of_states = self.get_target_function().get_total_configs()
        member = self.get_colony_member(0)
        nodes = member.get_number_of_nodes()
        minimum = member.get_lower_extreme()
        maximum = member.get_upper_extreme()
        neighbourhood = scout.get_ngh_size()
        s_threshold = self.get_search_threshold()
        new_scout = scout.create_copy()

        next_config = [False] * nodes
        temp_config = [False] * nodes

        if scout.get_fitness() > s_threshold:
            o_funct = self.get_target_function()
        else:
            o_funct = self.get_attract_function()

        scout_fitness = scout.get_fitness()
        for f in range(foragers):
            random_state = random.randint(0, nr_of_states - 1)
            network_state = o_funct.get_state(random_state)

            if synch:
                scout.synch_next_state(network_state, next_config)
            else:
                scout.asynch_next_state(network_state, next_config)
            
            new_forager = scout.create_copy()
            for n in range(neighbourhood):
                for i in range(nodes - 1):
                    temp_config[i] = next_config[i]
                random1 = random.randint(0, nodes - 1)
                count = 0
                stop = False

                while not stop and count < 5:
                    random2 = random.randint(0, nodes)
                    if next_config[random1]:
                        change = -1
                    else:
                        change = 1
                    
                    if random2 == 0:
                        current_value = new_forager.get_thr_vector_element(random1)
                        if current_value == minimum:
                            new_forager.set_thr_vector_element(random1, current_value + 1)
                        elif current_value == maximum:
                            new_forager.set_thr_vector_element(random1, current_value - 1)
                        else:
                            new_forager.set_thr_vector_element(random1, current_value + change)
                    else:
                        random3 = random.randint(0, nodes - 1)
                        current_value = new_forager.get_adj_matrix_element(random1, random3)

                        if current_value == minimum:
                            new_forager.set_adj_matrix_element(random1, random3, current_value + 1)
                        elif current_value == maximum:
                            new_forager.set_adj_matrix_element(random1, random3, current_value - 1)
                        else:
                            new_forager.set_adj_matrix_element(random1, random3, current_value + change)
                    
                    if synch:
                        new_forager.synch_next_state(network_state, temp_config)
                    else:
                        new_forager.asynch_next_state(network_state, temp_config)

                    if temp_config[random1] == next_config[random1]:
                        count += 1
                    else:
                        stop = True
                        n = neighbourhood
            
            o_funct.evaluate(new_forager, self.get_synch_mode())
            if new_forager.get_fitness() < scout_fitness:
                new_scout = new_forager
                scout_fitness = new_forager.get_fitness()
            elif new_forager.get_fitness() == scout_fitness and new_forager.get_edges() < scout_edges:
                new_scout = new_forager
            else:
                new_forager = None
        
        return new_scout
    
    def g_search(self):
        sts = self.get_sites()
        bst = self.get_nb()

        for s in range(bst, sts):
            self.get_colony_member(s).reinit_adj_matrix()
            self.get_colony_member(s).reinit_thr_vector()
            self.get_colony_member(s).set_ttl(self.get_stlim())
            self.get_colony_member(s).set_ngh_size(self.get_init_ngh())
            self.get_target_function().evaluate(self.get_colony_member(s), self.get_synch_mode())

    def site_abandonment(self):
        bst = self.get_nb()

        for s in range(bst):
            if self.get_colony_member(s).get_ttl() == 0:
                if self.get_colony_member(s).get_fitness() < self.get_save_threshold():
                    self.save_solution(self.get_colony_member(s))
                    self.abandon(self.get_colony_member(s))
                else:
                    self.abandon(self.get_colony_member(s))

    def abandon(self, solution: Bee):
        solution.reinit_adj_matrix()
        solution.reinit_thr_vector()
        solution.set_ttl(self.get_stlim())
        solution.set_ngh_size(self.get_init_ngh())
        self.get_target_function().evaluate(solution, self.get_synch_mode())

    def save_solution(self, solution: Bee):
        file_name = f"{self.get_save_files()}{str(self.get_solut_counter())}.txt"
        try:
            with open(file_name, "w") as file:
                self.save_solution(solution, file)
            self.increment_solut_counter()
        except FileNotFoundError:
            raise FileNotFoundError(f"Can't open {file_name}")
        
    def monitor_progress(self, out_file, iteration):
        try:
            with open(out_file, "W") as file:
                file.write(f"{iteration}\t{self.get_colony_member(0).get_fitness()}\t{self.get_colony_member(0).get_edges()}\t{self.get_best_fitness}\n")
        except FileNotFoundError:
            raise FileNotFoundError("Out file not found")
        
    def save_solution(self, solution: Bee, out_file):
        nodes = solution.get_number_of_nodes()

        for i in range(nodes):
            for j in range(nodes):
                try:
                    with open(out_file, "w") as file:
                        file.write(f"{solution.get_adj_matrix_element(i,j)}\t")
                except FileNotFoundError:
                    raise FileNotFoundError("Out file not found")
        
        for i in range(nodes):
            try:
                with open(out_file, "w") as file:
                    file.write(f"{solution.get_thr_vector_element(i)}\t")
            except FileNotFoundError:
                raise FileNotFoundError("Out file not found")
            
    def display_results(self):
        saved = self.get_solut_counter()
        o_funct = self.get_attract_function()

        print("Best solutions found: \n")
        for i in range(saved):
            file_name = f"{self.get_save_files()}{i}.txt"
            member = self.get_colony_member(0)
            solution = Bee(member.get_number_of_nodes(), member.get_lower_extreme(), member.get_upper_extreme, file_name)
            print(f"Solution {i}\n")
            o_funct.evaluate_display(solution, self.get_synch_mode())

    def get_save_files(self):
        return self.save_files

        

    