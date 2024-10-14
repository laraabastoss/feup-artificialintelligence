import copy
import math
import random
import matplotlib.pyplot as plt
from utils import *

def calculate_temperature(initial_temperature, iteration, cooling_option):
    if(cooling_option == 1):
        return initial_temperature * 0.85 ** iteration
    elif(cooling_option == 2):
        return initial_temperature / (1 + 5 * math.log(1 + iteration))
    elif(cooling_option == 3):
        return initial_temperature / (1 + 1.5 * iteration) 
    else:
        return initial_temperature / (1 + 0.5 * iteration ** 2)

def simulated_annealing(pizzas, team_sizes, iterations, cooling_option=1):
    curr_solution = randomize_deliveries(pizzas, team_sizes)
    curr_score = evaluation_function(curr_solution)
    curr_iteration = 0
    initial_temperature = 1000
    temperatures = []
    explored_nodes = []
    best_nodes = []
    best_score = curr_score
    
    while curr_iteration < iterations:
        curr_iteration += 1
        temperature = calculate_temperature(initial_temperature, curr_iteration, cooling_option)
        temperatures.append(temperature)
        if temperature == 0: break
        neighbour, neighbour_score = generate_neighbour_random(copy.deepcopy(curr_solution), curr_score)
        #neighbour_score = evaluation_function(neighbour)
        
        if neighbour_score > curr_score:
            curr_solution = neighbour
            curr_score = neighbour_score
            best_score = curr_score
        else:
            probability = math.exp((neighbour_score - curr_score) / temperature)
            if random.random() < probability:
                curr_solution = neighbour
                curr_score = neighbour_score
                
        explored_nodes.append(curr_score)
        best_nodes.append(best_score)
        
    plt.plot(range(1, len(explored_nodes) + 1), explored_nodes, label='Explored Nodes')
    plt.plot(range(1, len(best_nodes) + 1), best_nodes, label='Best Nodes')

    plt.xlabel('Iteration')
    plt.ylabel('Solution Score')
    plt.title('Evolution of the Simulated Annealing alorithm')
    plt.legend()
    plt.grid(True)
    plt.show()
    
    return curr_solution, curr_score
