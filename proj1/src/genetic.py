import utils, copy
import matplotlib.pyplot as plt
import random
from tqdm.auto import tqdm
import numpy as np

"""
    Genetic Algorithm
    Parameters:

    Returns:
        final_solution: the best solution found
"""

MUTATION_PROB = 0.05

def genetic_algorithm(pizzas,team_sizes,iterations, parent_selection, population_size=60):
    population = initialize_population(pizzas, team_sizes, population_size)
    best_scores = []
    all_scores = []
    avg_scores = []
    infeasible_points = 0

    for individual in population:
        all_scores.append(utils.evaluation_function(individual))

    for i in tqdm(range(iterations)):

        p1, p2 = select_parents(population, parent_selection)

        avg_score = np.mean(all_scores)
        avg_scores.append(avg_score)
        best_solution = max(population, key=lambda x: utils.evaluation_function(x))
        best_scores.append(utils.evaluation_function(best_solution))

        child = crossover(p1, p2)

        if utils.is_feasible(child, team_sizes.copy()):
            random_index = random.randint(0, population_size-1)
            population[random_index] = child
            all_scores[random_index] = utils.evaluation_function(child)
        else:
            infeasible_points += 1

        population, mutated = mutate(population)




    best_solution = max(population, key=lambda x: utils.evaluation_function(x))
    best_score = utils.evaluation_function(best_solution)
    print(best_score)
    print(infeasible_points)



    show_graph(best_scores, avg_scores)

    return best_solution, best_score

def initialize_population(pizzas, team_sizes, population_size):
    population = []
    for _ in range(population_size):
        population.append(utils.randomize_deliveries(pizzas, team_sizes.copy()))
    return population


def select_parents(population, parent_selection):
    
    if(parent_selection == "Tournament"):
        return tournament(population)
    
    
    return roulette(population) 


def roulette(population):   
    scores = []
    
    for solution in population:
        score = utils.evaluation_function(solution)
        scores.append(score)
    
    soma_scores = sum(scores)
    
    probabilities = [score_fit / soma_scores for score_fit in scores]
        
    rand1 = random.random()
    cumulative_probability = 0    
    for i, probability in enumerate(probabilities):
        cumulative_probability += probability
        if rand1 <= cumulative_probability:
            p1 = population[i]
    
    rand2 = random.random()
    cumulative_probability = 0
    for j, probability2 in enumerate(probabilities):
        cumulative_probability += probability2
        if rand2 <= cumulative_probability:
            p2 = population[j]
    
    return p1, p2

def tournament(population):
    scores = []
    selected_individuals = []
    population_size = len(population)
    for solution in population:
        score = utils.evaluation_function(solution)
        scores.append(score)
    while len(selected_individuals) < 2:
        tournament = random.sample(range(population_size), population_size)

        winners_indices = sorted(tournament, key=lambda i: scores[i], reverse=True)[:2]

        selected_individuals.extend([population[i] for i in winners_indices])

    return selected_individuals[0], selected_individuals[1]
    


def crossover(p1, p2):
    child = copy.deepcopy(p1)
    max_length = min(len(p1.solution), len(p2.solution))
    
    assigned_pizzas = set(pizza.index for delivery in p1.solution for pizza in delivery.pizzas)
    
    for i in range(max_length):
        parent = p1 if random.random() > 0.5 else p2

        pizza_free = True
        space_free = True

        if i < len(parent.solution):

            for pizza in parent.solution[i].pizzas:
                if pizza.index in assigned_pizzas:
                    pizza_free = False
                    break         
            if pizza_free:
                for pizza in parent.solution[i].pizzas:
                    assigned_pizzas.add(pizza.index)
            
            if pizza_free:
                if parent.solution[i].team_size == 2:
                    if child.free[0] == 0 and child.solution[i].team_size == 2 and parent.solution[i].team_size == 2:
                        pass
                    elif child.free[0] > 0:
                        child.free[0] -= 1
                        child.free[parent.solution[i].team_size - 2] += 1
                    else:
                        space_free = False

                if parent.solution[i].team_size == 3:
                    if child.free[1] == 0 and child.solution[i].team_size == 3 and parent.solution[i].team_size == 3:
                        pass
                    elif child.free[1] > 0:
                        child.free[1] -= 1
                        child.free[parent.solution[i].team_size - 2] += 1
                    else:
                        space_free = False

                if parent.solution[i].team_size == 4:
                    if child.free[2] == 0 and child.solution[i].team_size == 4 and parent.solution[i].team_size == 4:
                        pass
                    elif child.free[2] > 0:
                        child.free[2] -= 1
                        child.free[parent.solution[i].team_size - 2] += 1
                    else:
                        space_free = False
                
                         
            if pizza_free and space_free:
                child.solution[i] = parent.solution[i]

    return child
 

def mutate(population):
    mutated = False
    for i in range(len(population)):
        if random.random() < MUTATION_PROB:
            population[i] , _ = utils.generate_neighbour_random(population[i])
            mutated = True
    return population, mutated


def show_graph(best_scores, avg_scores):
    plt.plot(range(1, len(best_scores) + 1), best_scores, label='Best Individual Score')
    plt.plot(range(1, len(avg_scores) + 1), avg_scores, linestyle='--', color='red', label='Average Population Score')
    plt.xlabel('Iteration')
    plt.ylabel('Score')
    plt.title('Algorithm Performance')
    plt.legend()
    plt.show()