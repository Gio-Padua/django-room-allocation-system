import random

# Problem parameters
num_knapsacks = 6
knapsack_capacities = [20, 20, 20, 20 ,20, 20]

item_weights = [8, 3, 5, 7, 4, 3, 6, 1, 3, 15, 10, 20, 5, 8, 19]
item_values = [60, 100, 120, 160, 180, 200, 220, 240, 260, 280, 290, 300, 280, 200, 300, 100]
num_items = len(item_weights)
# Fitness function
def fitness(solution, knapsack_capacities, item_weights, item_values):
    total_value = 0
    for i in range(len(solution)):
        if solution[i] == 1: # If the item is included in the knapsack
            total_value += item_values[i]
    return total_value

# Tournament selection
def tournament_selection(population, fitnesses, tournament_size):
    selected = []
    for _ in range(tournament_size):
        index = random.randint(0, len(population) - 1)
        selected.append(population[index])
    return max(selected, key=lambda x: fitnesses[population.index(x)])

# One-point crossover
def one_point_crossover(parent1, parent2):
    crossover_point = random.randint(1, len(parent1) - 1)
    child1 = parent1[:crossover_point] + parent2[crossover_point:]
    child2 = parent2[:crossover_point] + parent1[crossover_point:]
    return child1, child2

# Mutation
def mutate(solution, mutation_rate):
    for i in range(len(solution)):
        if random.random() < mutation_rate:
            solution[i] = 1 - solution[i] # Flip the bit
    return solution

# Genetic algorithm
def genetic_algorithm(population_size, num_generations, tournament_size, mutation_rate):
    # Initialize the population
    population = [[random.randint(0, 1) for _ in range(num_items)] for _ in range(population_size)]
    fitnesses = [fitness(individual, knapsack_capacities, item_weights, item_values) for individual in population]

    for _ in range(num_generations):
        new_population = []
        for _ in range(population_size):
            # Selection
            parent1 = tournament_selection(population, fitnesses, tournament_size)
            parent2 = tournament_selection(population, fitnesses, tournament_size)

            # Crossover
            child1, child2 = one_point_crossover(parent1, parent2)

            # Mutation
            child1 = mutate(child1, mutation_rate)
            child2 = mutate(child2, mutation_rate)

            new_population.extend([child1, child2])

        population = new_population
        fitnesses = [fitness(individual, knapsack_capacities, item_weights, item_values) for individual in population]
        #print(f"Population fitness: {fitnesses}")

    # Return the best solution and the distribution of items across the knapsacks
    best_solution = max(population, key=lambda x: fitness(x, knapsack_capacities, item_weights, item_values))
    return best_solution, distribute_items(best_solution, knapsack_capacities, item_weights)

# Function to distribute items across the knapsacks
def distribute_items(solution, knapsack_capacities, item_weights):
    knapsack_contents = [[] for _ in range(num_knapsacks)]
    knapsack_weights = [0 for _ in range(num_knapsacks)]

    for i, item in enumerate(solution):
        if item == 1:
            for j in range(num_knapsacks):
                if knapsack_weights[j] + item_weights[i] <= knapsack_capacities[j]:
                    knapsack_contents[j].append(i)
                    knapsack_weights[j] += item_weights[i]
                    break
            print(f"Knapsack {j+1}: Items {knapsack_contents}, Total Weight {sum(knapsack_weights)}")

    return knapsack_contents, knapsack_weights

# Run the genetic algorithm
best_solution, distribution = genetic_algorithm(population_size=100, num_generations=100, tournament_size=5, mutation_rate=0.1)
print("Best solution:", best_solution)
print("Distribution of items across the knapsacks:")
for i, (contents, weight) in enumerate(zip(distribution[0], distribution[1])):
    print(f"Knapsack {i+1}: Items {contents}, Total Weight {weight}")