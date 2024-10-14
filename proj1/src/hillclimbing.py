import utils, copy
import matplotlib.pyplot as plt

"""
    Hill Climbing Algorithm
    Parameters:
        num_iterations: number of iterations to run the algorithm
        log: if True, prints the solution and score at each iteration
    Returns:
        final_solution: the best solution found
"""

def hill_climbing(pizzas,team_sizes,iterations, improving_iterations=False):
    
    total_iterations = 1
    scores = []
    curr_solution = utils.randomize_deliveries(pizzas,team_sizes)
    curr_score = utils.evaluation_function(curr_solution)

    curr_iteration = 0
    
    while curr_iteration < iterations:
        total_iterations += 1
        curr_iteration += 1
        neighbour, neighbour_score  = utils.generate_neighbour_random(copy.deepcopy(curr_solution), curr_score)
        if neighbour_score > curr_score: 
            scores.append(neighbour_score)
            curr_solution = neighbour
            curr_score = neighbour_score
            if improving_iterations == True:
                curr_iteration = 0
        else:
            scores.append(curr_score)
                
    plt.plot((range(1,total_iterations )), scores)
    plt.xlabel('Iteration')
    plt.ylabel('Score')
    plt.title('Algorithm Performance')
    plt.show()
    print(curr_score)
    return curr_solution, curr_score

 