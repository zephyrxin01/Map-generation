from RPGMap import RPGMap
import random
TOURNAMENT_SIZE = 5

class GeneticAlgorithm:
    def __init__(self, default_map_filename, population_size):
        # Load the default map as the base individual
        base_map = RPGMap(filename=default_map_filename)

        # Initialize population as mutated versions of the base map
        self.population = [self.mutate_map(base_map, mutation_rate=0.1) for _ in range(population_size)]

    def mutate_map(self, base_map, mutation_rate):
        """Create a mutated version of the base map."""
        new_map = RPGMap(width=base_map.width, height=base_map.height)
        new_map.map = [row[:] for row in base_map.map] 
        new_map.mutate(mutation_rate)
        return new_map
    def tournament_selection(self, population, fitness_scores, tournament_size=3):
        """Perform tournament selection to choose parents."""
        parents = []
        for _ in range(TOURNAMENT_SIZE): 
            tournament = random.sample(list(zip(fitness_scores, population)), tournament_size)
            winner = max(tournament, key=lambda t: t[0])  # Select the individual with the best fitness
            parents.append(winner[1])
        return parents
    
    def evolve(self, generations, mutation_rate):
        """Evolve the population over multiple generations."""
        for generation in range(generations):
            # Evaluate fitness
            fitness_scores = [(m.evaluate_fitness(), m) for m in self.population]
            fitness_scores.sort(reverse=True, key=lambda x: x[0])

            # Select top individuals
            parents = self.tournament_selection([ind for _, ind in fitness_scores], [score for score, _ in fitness_scores], TOURNAMENT_SIZE)

            # Crossover and Mutation
            children = []
            while len(children) < len(self.population):
                parent1, parent2 = random.sample(parents, 2)
                child = RPGMap.crossover(parent1, parent2)
                child.mutate(mutation_rate)
                children.append(child)

            self.population = children

            # Log progress
            best_fitness = fitness_scores[0][0]
            print(f"Generation {generation + 1}: Best Fitness = {best_fitness}")

        return max(self.population, key=lambda m: m.evaluate_fitness())