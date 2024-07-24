import numpy as np
import random
import matplotlib.pyplot as plt

P_follow=0.8
P_hear=0.8
P_scout=1-P_follow

def vector(position,destination):
    distance_vector=np.subtract(position,destination)
    distance=np.sqrt(distance_vector[0]**2+distance_vector[1]**2)

    direction = distance_vector/distance
    return direction

class Bee:
    def __init__(self, position, memory):
        self.position = position
        self.memory = memory
        self.fitness = 0.0  # Ensure fitness is a float for precision
        self.position_history = []  # Track position history
        self.direction = random.uniform(0,2*np.pi())

    def move(self, environment):
        direction = np.array(environment.nearest_nectar(self.position)) - np.array(self.position)
        if np.linalg.norm(direction) > 20:  # Random move 
            step = np.random.randint(-1, 4, 2)
        else:
            direction = np.array(environment.nearest_nectar(self.position)) - np.array(self.position)
            if np.linalg.norm(direction) != 0:
                step = direction / np.linalg.norm(direction)
                step = np.round(step).astype(int)  # Convert step to integer
            else:
                step = np.array([0, 0])  # Default step if direction vector norm is zero

        self.position += step
        self.position = np.clip(self.position, 0, environment.size - 1)  # Keep within bounds
    
    def dance(self,environment):
        self.direction=random.uniform(0,2*np.pi())
        step = [np.cos(self.direction),np.sin(self.direction)]
        self.position = self.position+step
        self.position = np.clip(self.position, 1, environment.hive_size - 1)  # Keep within bounds
    
        return ...
    
    def follow(self,information):
        if random.random() < P_hear:
            self.memory = [information]
        else:
            self.memory = []
    
    def scout(self,environment):
        return ...
    
    def forage(self,environment):
        direction = np.array(environment.nearest_nectar(self.position)) - np.array(self.position)
        if np.linalg.norm(direction) != 0:
            step = direction / np.linalg.norm(direction)
        else:
            direction = vector(self.position,environment.hive_size/2)
            step = direction
            self.position += step














class Environment:
    def __init__(self, size, nectar_sources, hive_position, hive_size):
        self.size = size
        self.nectar_sources = nectar_sources
        self.hive_position = hive_position
        self.hive_size = hive_size

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

