import utils
import copy
import matplotlib.pyplot as plt

def get_candidate_solution(neighbourhood):
    new_solution = None
    new_solution_score = 0

    for neighbour in neighbourhood:
        neighbour_score = utils.evaluation_function(neighbour)

        if neighbour_score > new_solution_score:
            new_solution = neighbour
            new_solution_score = neighbour_score

    return new_solution, new_solution_score

def penalty_function(solution, best_solution_so_far):
    penalty = 0

    for i in range(min(len(solution.solution),len(best_solution_so_far.solution) )):
        current_delivery = solution.solution[i]
        best_delivery = best_solution_so_far.solution[i]

        penalty += abs(current_delivery.team_size - best_delivery.team_size)

        current_ingredients = set()
        best_ingredients = set()

        for pizza in current_delivery.pizzas:
            current_ingredients.update(pizza.ingredients)

        for pizza in best_delivery.pizzas:
            best_ingredients.update(pizza.ingredients)

        penalty += len(current_ingredients.intersection(best_ingredients))

    return penalty

def guided_local_search(pizzas, team_sizes, iterations):
    curr_solution = utils.randomize_deliveries(pizzas, team_sizes)
    curr_score = utils.evaluation_function(curr_solution)

    best_solution = copy.deepcopy(curr_solution)
    best_score = curr_score

    explored_nodes = []
    best_nodes = []

    curr_iteration = 0

    while curr_iteration < iterations:
        neighbourhood = utils.generate_neighbourhood(curr_solution)

        new_solution, new_solution_score = get_candidate_solution(neighbourhood)

        new_solution_score_with_penalty = new_solution_score - penalty_function(new_solution, best_solution)
        curr_score_with_penalty = curr_score - penalty_function(curr_solution, best_solution)

       
        if new_solution is not None and new_solution_score_with_penalty>curr_score_with_penalty:
            curr_solution = new_solution
            curr_score = new_solution_score

            if curr_score > best_score:
                best_solution = copy.deepcopy(curr_solution)
                best_score = curr_score
       

        explored_nodes.append(curr_score)
        best_nodes.append(best_score)

        curr_iteration += 1

    plt.plot(range(1, len(explored_nodes) + 1), explored_nodes, label='Explored Nodes')
    plt.plot(range(1, len(best_nodes) + 1), best_nodes, label='Best Nodes')

    plt.xlabel('Iteration')
    plt.ylabel('Solution Score')
    plt.title('Evolution of the Guided Local Search Algorithm')
    plt.legend()
    plt.grid(True)
    plt.show()

    return best_solution, best_score

