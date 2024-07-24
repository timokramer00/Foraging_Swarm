import numpy as np
import random
import matplotlib.pyplot as plt

class Bee:
    def __init__(self, position, memory):
        self.position = position
        self.memory = memory
        self.fitness = 0.0  # Ensure fitness is a float for precision
        self.position_history = []  # Track position history

    def move(self, environment):
        direction = np.array(environment.nearest_nectar(self.position)) - np.array(self.position)
        if np.linalg.norm(direction) > 20:  # Random move 
            step = np.random.randint(-1, 3, 2)
        else:
            direction = np.array(environment.nearest_nectar(self.position)) - np.array(self.position)
            if np.linalg.norm(direction) != 0:
                step = direction / np.linalg.norm(direction)
                #step = np.round(step).astype(int)  # Convert step to integer
            else:
                step = np.array([0, 0])  # Default step if direction vector norm is zero

        #print(step)\
        self.position = self.position+step
        
        self.position = np.clip(self.position, 0, environment.size - 1)  # Keep within bounds

    def evaluate_fitness(self, environment):
        nearest_nectar_dist = np.min([np.linalg.norm(np.array(self.position) - np.array(nectar)) for nectar in environment.nectar_sources])
        hive_distance = np.linalg.norm(np.array(self.position) - np.array(environment.hive_position))
        self.fitness += 1 / (nearest_nectar_dist + 1) + 1 / (hive_distance + 1)
        #print(f"Bee at {self.position} has fitness {self.fitness} (nearest nectar dist: {nearest_nectar_dist}, hive dist: {hive_distance})")

    def record_position(self):
        self.position_history.append(self.position)  # Record current position
        #print(self.position_history)

class Environment:
    def __init__(self, size, nectar_sources, hive_position):
        self.size = size
        self.nectar_sources = nectar_sources
        self.hive_position = hive_position

    def nearest_nectar(self, position):
        distances = [np.linalg.norm(np.array(position) - np.array(nectar)) for nectar in self.nectar_sources]
        return self.nectar_sources[np.argmin(distances)]

def initialize_population(pop_size, environment):
    population = []
    for _ in range(pop_size):
        position = [0,0]
        memory = []  # Bees can have memory of good nectar spots
        bee = Bee(position, memory)
        bee.evaluate_fitness(environment)  # Evaluate initial fitness
        population.append(bee)
    return population

def evaluate_population(population, environment):
    for bee in population:
        bee.move(environment)
        bee.evaluate_fitness(environment)
        bee.record_position()  # Record the bee's position after moving
        #print(f"Evaluated Bee fitness: {bee.fitness}")

def select(population):
    population.sort(key=lambda bee: bee.fitness, reverse=True)
    selected_population = population[:len(population)//2]
    #print(f"Selected Bees (Top Half): {[bee.fitness for bee in selected_population]}")  # Debug statement
    return selected_population

def crossover(parent1, parent2):
    child_position = (np.array(parent1.position) + np.array(parent2.position)) // 2
    child_memory = list(set(parent1.memory + parent2.memory))
    return Bee(child_position, child_memory)

def mutate(bee, environment, mutation_rate=0.2):
    if random.random() < mutation_rate:
        bee.position = [0,0]
    return bee

def run_evolution(pop_size, generations, environment):
    population = initialize_population(pop_size, environment)
    for generation in range(generations):
        #print(f"\nGeneration {generation}")  # Debug statement
        evaluate_population(population, environment)
        selected = select(population)
        # new_population = []
        # while len(new_population) < pop_size:
        #     parent1, parent2 = random.sample(selected, 2)
        #     child = crossover(parent1, parent2)
        #     #child = mutate(child, environment)
        #     child.evaluate_fitness(environment)  # Evaluate fitness of the new child
        #     new_population.append(child)
        # print(child.position)
        # population = new_population
        # evaluate_population(population, environment)
        best_fitness = max(bee.fitness for bee in population)
        print(f"Best Fitness of Generation {generation}: {best_fitness}")  # Debug statement
        #print(f"Population Fitness: {[bee.fitness for bee in population]}")  # Debug statement
    return population


def plot_bee_movement(population, environment):
    fig, ax = plt.subplots(figsize=(8, 8))
    ax.set_xlim(0, environment.size)
    ax.set_ylim(0, environment.size)
    ax.set_title('Bee Movement')
    ax.set_xlabel('X Position')
    ax.set_ylabel('Y Position')
    ax.grid(True)

    for bee in population:
        positions = np.array(bee.position_history)

        if len(positions) > 0:  # Check if there are recorded positions
            ax.plot(positions[:, 0], positions[:, 1], label=f'Bee Fitness: {bee.fitness:.2f}')
            ax.scatter(bee.position[0], bee.position[1], color='red', marker='o', s=50)

    ax.scatter(environment.hive_position[0], environment.hive_position[1], color='green', marker='s', s=100, label='Hive')

    for nectar in environment.nectar_sources:
        ax.scatter(nectar[0], nectar[1], color='orange', marker='^', s=100, label='Nectar Source')

    ax.legend()
    plt.show()

# Example usage
environment = Environment(size=100, nectar_sources=[(90, 60), (50, 80), (100, 50)], hive_position=(0, 0))
population = run_evolution(pop_size=5, generations=500, environment=environment)

plot_bee_movement(population, environment)