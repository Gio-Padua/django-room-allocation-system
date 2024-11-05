import random

def fitness(solution, rooms, residents):
    total_fitness = 0
    room_assignments = {room.id: [] for room in rooms}

    # Step 1: Assign residents to rooms based on the solution
    for resident_index, room_index in enumerate(solution):
        room = rooms[room_index]
        resident = residents[resident_index]
        room_assignments[room.id].append(resident)

    # Step 2: Evaluate fitness based on room assignments
    for room in rooms:
        assigned_residents = room_assignments[room.id]
        total_family_size = sum(resident.family_size for resident in assigned_residents)

        # Penalize if the total family size exceeds room capacity
        if total_family_size > room.capacity:
            total_fitness -= 10 * (total_family_size - room.capacity)  # Penalty for exceeding capacity

        # Reward or penalize based on priority matching
        for resident in assigned_residents:
            if room.priority and resident.priority:
                total_fitness += 2  # Bonus for priority match
            elif room.priority and not resident.priority:
                total_fitness -= 5  # Penalty if non-priority resident is in priority room
            else:
                total_fitness += 1  # Basic fitness for valid non-priority assignment

    return max(total_fitness, 0)  # Ensure non-negative fitness


def create_valid_solution(rooms, residents):
    room_capacities = {room.id: room.capacity for room in rooms}
    room_assignments = {room.id: [] for room in rooms}

    solution = [-1] * len(residents)  # Placeholder for resident assignments

    # Assign priority residents first
    priority_residents = [i for i, resident in enumerate(residents) if resident.priority]
    non_priority_residents = [i for i, resident in enumerate(residents) if not resident.priority]

    all_residents = priority_residents + non_priority_residents

    for resident_index in all_residents:
        resident = residents[resident_index]

        # Try to assign resident to a room without exceeding capacity
        possible_rooms = list(range(len(rooms)))
        random.shuffle(possible_rooms)

        for room_index in possible_rooms:
            room = rooms[room_index]
            assigned_residents = room_assignments[room.id]
            total_family_size = sum(r.family_size for r in assigned_residents)

            # Only assign resident if it doesn't exceed the room's capacity
            if total_family_size + resident.family_size <= room.capacity:
                room_assignments[room.id].append(resident)
                solution[resident_index] = room_index
                break

    return solution


def genetic_algorithm(rooms, residents, population_size=100, num_generations=100, tournament_size=5, mutation_rate=0.1):
    # Step 1: Create initial population with capacity constraints
    population = [create_valid_solution(rooms, residents) for _ in range(population_size)]

    # Step 2: Evolve the population over multiple generations
    for _ in range(num_generations):
        new_population = []
        fitnesses = [fitness(individual, rooms, residents) for individual in population]

        # Handle all-zero fitness case
        if max(fitnesses) == 0:
            fitnesses = [1] * len(fitnesses)  # Set minimum fitness to 1 if all fitnesses are zero

        # Step 3: Selection and crossover
        for _ in range(population_size):
            parent1 = random.choices(population, weights=fitnesses, k=1)[0]
            parent2 = random.choices(population, weights=fitnesses, k=1)[0]

            crossover_point = random.randint(1, len(parent1) - 1)
            child1 = parent1[:crossover_point] + parent2[crossover_point:]
            child2 = parent2[:crossover_point] + parent1[crossover_point:]

            # Mutate the children, ensuring valid assignments with room capacity limits
            child1 = mutate(child1, rooms, residents, mutation_rate)
            child2 = mutate(child2, rooms, residents, mutation_rate)

            new_population.extend([child1, child2])

        population = new_population

    # Return the best solution based on fitness
    best_solution = max(population, key=lambda x: fitness(x, rooms, residents))
    return best_solution


# Mutation function that mutates room assignments while respecting room capacities
def mutate(solution, rooms, residents, mutation_rate):
    room_capacities = {room.id: room.capacity for room in rooms}
    room_assignments = {room.id: [] for room in rooms}

    for i, room_index in enumerate(solution):
        resident = residents[i]
        if random.random() < mutation_rate:
            possible_rooms = list(range(len(rooms)))
            random.shuffle(possible_rooms)

            # Try to find a new valid room assignment without exceeding capacity
            for new_room_index in possible_rooms:
                new_room = rooms[new_room_index]
                assigned_residents = room_assignments[new_room.id]
                total_family_size = sum(r.family_size for r in assigned_residents)

                # Only reassign resident if it doesn't exceed the new room's capacity
                if total_family_size + resident.family_size <= new_room.capacity:
                    solution[i] = new_room_index
                    break

    return solution
