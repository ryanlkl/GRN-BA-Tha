from beesAlgorithm_GRN import BeesAlgorithm_GRN
import resources
from nAttractors import NAttractors
from reducedMAB import ReducedMAB

def main():
    stop = False
    file_BA_pars = "runFiles/parameters/BA_parameters.txt"
    file_GRN_pars = "runFiles/parameters/GRN_pars.txt"
    target_file = "runFiles/parameters/RMAB.txt"
    attractor_file = "runFiles/parameters/FixedPoints.txt"
    save_files = "runFiles/results/solution_"

    solver = BeesAlgorithm_GRN(save_files)
    solver.bees_alg_initialisation(file_BA_pars, file_GRN_pars)
    solver.set_obj_functions(target_file, attractor_file)


    while not stop:
        answer = input("Do you want to run the BA or test the results? (run/test)")
        if answer.lower() == "run":
            stop = True
            solver.bees_algorithm()
            solver.display_results()
        elif answer.lower() == "test":
            stop = True
            solutions = input("How many solutions? ")
            solver.set_solut_counter(int(solutions))
            solver.display_results()
        else:
            print("Please select a valid option")

    print("Done")

if __name__ == "__main__":
    main()