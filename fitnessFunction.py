from resources import bool_to_int

class FitnessFunction:
    def __init__(self, number_of_nodes, type):
        self.initialise_states(number_of_nodes)
        self.funct_type = type
        self.total_configs = 0

    def initialise_states(self, number_of_nodes):
        tot_s = 1 << number_of_nodes

        self.total_configs = tot_s
        configurations = [False] * tot_s

        for i in range(tot_s):
            configurations[i] = [False] * number_of_nodes

            for j in range(number_of_nodes):
                configurations[i][j] = False
        
        for i in range(1, tot_s):
            j = number_of_nodes - 1
            while configurations[i - 1][j]:
                configurations[i][j] = not configurations[i - 1][j]
                j -= 1
            
            configurations[i][j] = not configurations[i - 1][j]
            j -= 1
            while j >= 0:
                configurations[i][j] = configurations[i - 1][j]
                j -= 1
    
    def get_total_configs(self):
        return self.total_configs
    
    def get_node_state(self, GRN_configuration, node):
        if GRN_configuration >= self.get_total_configs():
            raise ValueError("Number of possible configurations exceeded\n")
        else:
            return self.configurations[GRN_configuration][node]
    
    def get_state(self, GRN_configuration):
        if GRN_configuration >= self.get_total_configs():
            raise ValueError("Number of possible configurations exceeded\n")
        else:
            return self.configurations[GRN_configuration]
        
    def find_attractors(self, solution, synch_update, states_list):
        nds = solution.get_number_of_nodes()
        stts = self.get_total_configs()
        current_config = [False] * nds
        next_config = [False] * nds
        temp_sequence = [0] * stts

        for i in range(stts):
            states_list[i] = -1
            temp_sequence[i] = -1

        cursor_states = 0
        cursor_temp = 0

        while cursor_states < stts:
            cursor_temp = 0
            while states_list[cursor_states] != -1 and cursor_states < stts - 1:
                cursor_temps += 1
            
            stop = False
            fixed = False
            for i in range(nds):
                current_config[i] = self.get_node_state(cursor_states, i)
            
            temp_sequence[cursor_temp] = bool_to_int(nds, current_config)

            while not stop:
                if synch_update:
                    solution.synch_next_state(current_config, next_config)
                else:
                    solution.asynch_next_state(current_config, next_config)
                
                next_state = bool_to_int(nds, next_config)

                if states_list[next_state] >= 0:
                    stop = True
                    fixed = True
                    next_state = states_list[next_state]
                elif next_state == temp_sequence[cursor_temp]:
                    stop = True
                    fixed = True
                elif states_list[next_state] == - 10:
                    stop = True
                
                i = 0
                while not stop and i < cursor_temp:
                    if temp_sequence[i] == next_state:
                        stop = True
                    i += 1
                
                if stop and fixed:
                    i = 0
                    while i <= cursor_temp and i < stts:
                        states_list[temp_sequence[i]] = next_state
                elif stop:
                    i = 0
                    while i <= cursor_temp and i < stts:
                        states_list[temp_sequence[i]] = -10
                else:
                    for i in range(nds):
                        current_config[i] = next_config[i]
                    
                    cursor_temp += 1
                    if cursor_temp == stts:
                        stop = True
                    else:
                        temp_sequence[cursor_temp] = next_state
            i = 0
            while i <= cursor_temp and i < stts:
                temp_sequence[i] = -1
            cursor_states += 1
    
    def get_funct_type(self):
        return self.funct_type