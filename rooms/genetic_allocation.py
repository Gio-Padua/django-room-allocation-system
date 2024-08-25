import random


def fitness(solution, rooms, residents):
    total_fitness = 0
    occupied_rooms = set()  # Track occupied rooms to avoid double assignment

    # Prioritize high-priority residents in high-priority rooms (double bonus)
    for resident_index, resident in enumerate(residents):
        if resident.priority:
            for room_index, room in enumerate(rooms):
                if room.priority and solution[room_index] == 0 and resident.family_size <= room.capacity and room not in occupied_rooms:
                    total_fitness += 2  # Double fitness for priority match
                    solution[room_index] = 1
                    occupied_rooms.add(room)
                    break  # Move to next resident once assigned

    # Fill remaining rooms with other residents, ensuring capacity constraints
    for room_index, room in enumerate(rooms):
        if solution[room_index] == 0:  # Only consider unassigned rooms
            for resident_index, resident in enumerate(residents):
                if not resident.assigned and resident.family_size <= room.capacity:
                    total_fitness += 1
                    solution[room_index] = 1
                    occupied_rooms.add(room)
                    resident.assigned = True
                    break  # Move to next resident once assigned

    # Check if total family size exceeds room capacity
    for room in rooms:
        if solution[rooms.index(room)] == 1:
            assigned_residents = [residents[i] for i, assigned in enumerate(solution) if assigned == 1 and i == room.id]
            total_family_size = sum(resident.family_size for resident in assigned_residents)
            if total_family_size > room.capacity:
                total_fitness -= 10  # Penalty for exceeding capacity

    return total_fitness

def genetic_algorithm(rooms, residents, population_size=100, num_generations=100, tournament_size=5, mutation_rate=0.1):
    # Initialize the population with random assignments
    population = [[random.randint(0, 1) for _ in range(len(rooms))] for _ in range(population_size)]

    for _ in range(num_generations):
        new_population = []
        fitnesses = [fitness(individual.copy(), rooms, residents) for individual in population]
        # Tournament selection
        for _ in range(population_size):
            parent1 = random.choices(population, weights=fitnesses, k=tournament_size)[0]
            parent2 = random.choices(population, weights=fitnesses, k=tournament_size)[0]

            # One-point crossover
            crossover_point = random.randint(1, len(parent1) - 1)
            child1 = parent1[:crossover_point] + parent2[crossover_point:]
            child2 = parent2[:crossover_point] + parent1[crossover_point:]

            # Mutation
            child1 = mutate(child1, mutation_rate)
            child2 = mutate(child2, mutation_rate)

            new_population.extend([child1, child2])

        population = new_population
        fitnesses = [fitness(individual.copy(), rooms, residents) for individual in population] 
    # Return the best solution and the distribution of items across the knapsacks
    
    try:
            best_solution = max(population, key=lambda x: fitness(x, rooms, residents))
            return best_solution
    except:
            # Handle exceptions or cases where no solution is found
            return []

def mutate(solution, mutation_rate):
    for i in range(len(solution)):
        if random.random() < mutation_rate:
            solution[i] = 1 - solution[i]  # Flip the bit
    return solution