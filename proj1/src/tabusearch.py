import utils
import copy
import matplotlib.pyplot as plt


"""
    Tabu Search Algorithm
    Parameters:
        pizzas: list of pizzas
        team_sizes: list of team sizes
        iterations: number of iterations to run the algorithm
        tabu_tenure: number of iterations a solution stays in tabu lits
    Returns:
        final_solution: the best solution found
"""

def update_tabu_list(tabu_list, curr_solution,tabu_tenure):

    tabu_list[curr_solution] = tabu_tenure

    for sol in list(tabu_list.keys()):
        tabu_list[sol] -= 1
        if tabu_list[sol] <= 0:
            del tabu_list[sol]
    return tabu_list


def get_cadidate_solution(neighbourhood,tabu_list):
     
    new_solution = None
    new_solution_score = 0 
     
    for neighbour in neighbourhood:
        neighbour_score = utils.evaluation_function(neighbour)

        if (neighbour_score > new_solution_score) and (neighbour not in tabu_list):
            new_solution = neighbour
            new_solution_score = neighbour_score

    return  new_solution, new_solution_score

        

def tabu_search(pizzas, team_sizes, iterations, tabu_tenure):

    curr_solution = utils.randomize_deliveries(pizzas, team_sizes)
    curr_score = utils.evaluation_function(curr_solution)
  
    best_solution = copy.deepcopy(curr_solution)
    best_score = curr_score
    
    tabu_list = {}
    explored_nodes = []  
    best_nodes = []     

    curr_iteration = 0

    while curr_iteration < iterations:

        tabu_list = update_tabu_list(tabu_list,curr_solution,tabu_tenure)
        
        neighbourhood = utils.generate_neighbourhood(curr_solution)

        new_solution, new_solution_score = get_cadidate_solution(neighbourhood,tabu_list)
  
        if new_solution is not None:
            curr_solution = new_solution
            curr_score = new_solution_score
   
            if curr_score > best_score:
             
                best_solution = copy.deepcopy(curr_solution)
                best_score = curr_score

        else:

            curr_solution = utils.randomize_deliveries(pizzas, team_sizes)
            curr_score =  utils.evaluation_function(curr_solution)
  
        explored_nodes.append(curr_score) 
        best_nodes.append(best_score)

        curr_iteration += 1
    

    print(curr_solution)
    print(curr_score)

    plt.plot(range(1, len(explored_nodes) + 1), explored_nodes, label='Explored Nodes')
    plt.plot(range(1, len(best_nodes) + 1), best_nodes, label='Best Nodes')

    plt.xlabel('Iteration')
    plt.ylabel('Solution Score')
    plt.title('Evolution of the Tabu Search Algorithm')
    plt.legend()
    plt.grid(True)
    plt.show()

    return best_solution, best_score

