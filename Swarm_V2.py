import numpy as np
import matplotlib.pyplot as plt
import random
from matplotlib.animation import FuncAnimation

class NectarSource:
    def __init__(self, position, initial_quality):
        self.position = position
        self.quality = initial_quality

    def marker_size(self):
        return max(self.quality * 30, 30)  # Minimum marker size for visibility

class Bee:
    def __init__(self, id, hive_bounds):
        self.id = id
        self.state = 'in_hive'
        self.position = self.random_hive_position(hive_bounds)
        self.nectar_load = 0
        self.source = None
        self.hive_bounds = hive_bounds
        self.path = [self.position]
        self.target_position = None

    def random_hive_position(self, bounds):
        x = random.uniform(bounds[0][0], bounds[0][1])
        y = random.uniform(bounds[1][0], bounds[1][1])
        return (x, y)

    def transition(self, nectar_sources):
        if self.state == 'in_hive':
            self.start_scouting()
        elif self.state == 'scouting':
            self.scout(nectar_sources)
        elif self.state == 'on_source':
            self.load_nectar()
        elif self.state == 'returning':
            self.return_to_hive()
        elif self.state == 'unloading':
            self.unload_nectar()
        elif self.state == 'dancing':
            self.dance()
        elif self.state == 'following':
            self.follow_dance(nectar_sources)
        elif self.state == 'foraging':
            self.forage()

    def start_scouting(self):
        self.state = 'scouting'
        self.nectar_load = 0
        print(f'Bee {self.id} is starting to scout.')

    def scout(self, nectar_sources):
        if nectar_sources:
            self.source = random.choice(nectar_sources)
            self.target_position = self.source.position
            self.state = 'on_source'
            print(f'Bee {self.id} found a nectar source at {self.source.position} with quality {self.source.quality}.')

    def load_nectar(self):
        if self.source and self.source.quality > 0:
            self.nectar_load = min(self.source.quality, 1.0)
            self.source.quality -= self.nectar_load
            self.state = 'returning'
            self.target_position = self.random_hive_position(self.hive_bounds)
            print(f'Bee {self.id} is returning with nectar load {self.nectar_load}. Source quality now {self.source.quality}.')
        else:
            self.state = 'scouting'

    def return_to_hive(self):
        self.state = 'unloading'
        print(f'Bee {self.id} is returning to the hive.')

    def unload_nectar(self):
        if random.random() < 0.8:
            self.state = 'dancing'
            print(f'Bee {self.id} is unloading nectar and starting to dance.')
        else:
            self.state = 'in_hive'
            print(f'Bee {self.id} is unloading nectar and staying in hive.')

    def dance(self):
        if random.random() < 0.6:
            self.state = 'following'
            print(f'Bee {self.id} is dancing and will be followed.')
        else:
            self.state = 'in_hive'
            print(f'Bee {self.id} is dancing but no one is following.')

    def follow_dance(self, nectar_sources):
        if random.random() < 0.7:
            if nectar_sources:
                self.source = random.choice(nectar_sources)
                self.target_position = self.source.position
                self.state = 'foraging'
                print(f'Bee {self.id} is following a dance and going to forage.')
        else:
            self.state = 'in_hive'
            print(f'Bee {self.id} is following a dance but returns to hive.')

    def forage(self):
        if self.source and self.source.quality > 0:
            self.state = 'on_source'
            print(f'Bee {self.id} is foraging and successfully loaded nectar.')
        else:
            self.state = 'returning'
            self.nectar_load = 0
            self.target_position = self.random_hive_position(self.hive_bounds)
            print(f'Bee {self.id} found the source depleted and returns to hive.')

    def move_smoothly(self, steps=10):
        if self.target_position is None:
            return []

        current_position = np.array(self.position)
        target_position = np.array(self.target_position)
        direction = (target_position - current_position) / steps
        return [current_position + i * direction for i in range(1, steps + 1)]

def plot_bee_movements(bees, nectar_sources, hive_bounds, num_steps):
    fig, ax = plt.subplots(figsize=(10, 10))
    hive_rect = plt.Rectangle((hive_bounds[0][0], hive_bounds[1][0]),
                              hive_bounds[0][1] - hive_bounds[0][0],
                              hive_bounds[1][1] - hive_bounds[1][0],
                              edgecolor='red', facecolor='none', lw=2, label='Hive')
    ax.add_patch(hive_rect)

    nectar_positions = np.array([ns.position for ns in nectar_sources])
    nectar_sizes = [ns.marker_size() for ns in nectar_sources]
    nectar_scatters = ax.scatter(nectar_positions[:, 0], nectar_positions[:, 1], s=nectar_sizes, color='green', label='Nectar Sources')
    
    scatters = [ax.scatter(*bee.position, label=f'Bee {bee.id}') for bee in bees]
    def update(frame):
        global nectar_sources
        for bee, scatter in zip(bees, scatters):
            if frame % 10 == 0:
                bee.transition(nectar_sources)
                if bee.state in ['on_source', 'returning', 'foraging']:
                    bee.path.extend(bee.move_smoothly(steps=10))
            if bee.path:
                next_position = bee.path.pop(0)
                bee.position = tuple(next_position)
                scatter.set_offsets(next_position)

        # Remove depleted nectar sources and add new ones
        nectar_sources = [ns for ns in nectar_sources if ns.quality > 0]
        while len(nectar_sources) < num_nectar_sources:
            new_source = NectarSource((random.uniform(-10, 10), random.uniform(-10, 10)), random.uniform(1.0, 10.0))
            nectar_sources.append(new_source)
            print(f'Added new nectar source at {new_source.position} with quality {new_source.quality}.')

        nectar_positions = np.array([ns.position for ns in nectar_sources])
        nectar_sizes = [ns.marker_size() for ns in nectar_sources]
        nectar_scatters.set_offsets(nectar_positions)
        nectar_scatters.set_sizes(nectar_sizes)
        
        return scatters + [nectar_scatters]

    ani = FuncAnimation(fig, update, frames=num_steps * 10, blit=True, repeat=False)

    plt.title('Bee Movements')
    plt.xlabel('X Position')
    plt.ylabel('Y Position')
    plt.legend()
    plt.grid(True)
    plt.show()

def run_simulation(num_bees, num_steps, num_nectar_sources):
    global nectar_sources
    hive_bounds = [(-2, 2), (-2, 2)]
    bees = [Bee(i, hive_bounds) for i in range(num_bees)]
    nectar_sources = [NectarSource((random.uniform(-10, 10), random.uniform(-10, 10)), random.uniform(1.0, 10.0)) for _ in range(num_nectar_sources)]

    plot_bee_movements(bees, nectar_sources, hive_bounds, num_steps)

if __name__ == "__main__":
    num_bees = 10
    num_steps = 50
    num_nectar_sources = 5
    run_simulation(num_bees, num_steps, num_nectar_sources)