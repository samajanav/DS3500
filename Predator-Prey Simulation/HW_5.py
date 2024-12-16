# Importing libraries
import random as rnd
import copy
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.colors import ListedColormap
import argparse

# Using Argparse for inputs from terminal
parser = argparse.ArgumentParser(description='Simulation of foxes and rabbits in a field')

parser.add_argument('-g', '--grass_growth_rate', type=float, required=True,
                    help='Rate at which grass grows in the field')

parser.add_argument('-fs', '--field_size', type=int, required=True,
                    help='Size of the field')

parser.add_argument('-nf', '--initial_foxes', type=int, required=True,
                    help='Number of initial foxes in the field')

parser.add_argument('-nr', '--initial_rabbits', type=int, required=True,
                    help='Number of initial rabbits in the field')

parser.add_argument('-kc', '--k_count', type=int, required=True,
                    help='Foxes KCount')

parser.add_argument('-cy', '--cycle', type=int, required=True,
                    help='Number of cycles (generations) to be in the field')

args = parser.parse_args()

# Value variables

SIZE = args.field_size  # x/y dimensions of the field
WRAP = True  # When moving beyond the border, do we wrap around to the other size
GRASS_RATE = args.grass_growth_rate  # Probability of grass growing at any given location
SPEED = 2  # Number of generations per frame
OFFSPRING_RABBITS = 2  # The number of offspring when a rabbit reproduces
INIT_RABBITS = args.initial_rabbits  # Number of starting rabbits
OFFSPRING_FOXES = 1  # The number of offspring when a fox reproduces
INIT_FOXES = args.initial_foxes  # Number of starting fox
K_COUNT = args.k_count  # Foxes KCount
CYCLE = args.cycle  # Number of cycles (generations) to be in the field


# Defining Rabbit properties

class Rabbit:
    def __init__(self):
        """Initialize a rabbit with random coordinates, eaten grass count, and lifespan."""
        self.x = rnd.randrange(0, SIZE)
        self.y = rnd.randrange(0, SIZE)
        self.eaten = 0
        self.lifespan = 0

    def reproduce(self):
        """Create a new rabbit offspring with adjusted coordinates within a certain range."""
        self.eaten = 0
        self.lifespan = 0
        offspring = copy.deepcopy(self)
        offspring.x = max(0, min(SIZE - 1, self.x + rnd.randint(-10, 10)))
        offspring.y = max(0, min(SIZE - 1, self.y + rnd.randint(-10, 10)))
        return offspring

    def eat(self, amount):
        """Record the amount of grass eaten by a rabbit."""
        self.eaten += amount

    def move(self):
        """Move the rabbit within the field boundaries, updating its coordinates and lifespan."""
        if WRAP:
            self.x = (self.x + rnd.choice([-1, 0, 1])) % SIZE
            self.y = (self.y + rnd.choice([-1, 0, 1])) % SIZE
        else:
            self.x = min(SIZE - 1, max(0, (self.x + rnd.choice([-1, 0, 1]))))
            self.y = min(SIZE - 1, max(0, (self.y + rnd.choice([-1, 0, 1]))))

        self.lifespan += 1


# Defining Fox properties

class Fox:
    def __init__(self):
        """Initialize a fox with random coordinates, eaten rabbits count, hunger counter, and lifespan."""
        self.x = rnd.randrange(0, SIZE)
        self.y = rnd.randrange(0, SIZE)
        self.eaten = 0
        self.hunger_counter = 0
        self.lifespan = 0  # Initialize lifespan counter

    def reproduce(self):
        """Create a new fox offspring with adjusted coordinates within a certain range."""
        self.eaten = 0
        self.hunger_counter = 0
        self.lifespan = 0  # Reset lifespan counter
        offspring = copy.deepcopy(self)
        offspring.x = max(0, min(SIZE - 1, self.x + rnd.randint(-10, 10)))
        offspring.y = max(0, min(SIZE - 1, self.y + rnd.randint(-10, 10)))
        return offspring

    def eat(self, amount):
        """Record the amount of rabbits eaten by a fox and resets its hunger counter."""
        self.eaten += amount
        self.hunger_counter = 0

    def hungry(self):
        """Check if the fox is hungry based on its hunger counter."""
        if self.hunger_counter >= K_COUNT:
            return True
        else:
            return False

    def move(self):
        """Move the fox within the field boundaries, updating its coordinates, hunger counter, and lifespan."""
        if WRAP:
            self.x = (self.x + rnd.choice([-2, -1, 0, 1, 2])) % SIZE
            self.y = (self.y + rnd.choice([-2, -1, 0, 1, 2])) % SIZE
        else:
            self.x = min(SIZE - 1, max(0, (self.x + rnd.choice([-2, -1, 0, 1, 2]))))
            self.y = min(SIZE - 1, max(0, (self.y + rnd.choice([-2, -1, 0, 1, 2]))))

        self.hunger_counter += 1
        self.lifespan += 1


# Properties of Field (land where Rabbits and Foxes exists)
class Field:
    def __init__(self):
        """Initialize the field with empty lists for rabbits and foxes, and a grid representing the field."""
        self.rabbits = []
        self.foxes = []
        self.field = np.ones(shape=(SIZE, SIZE), dtype=int)

    def add_rabbit(self, rabbit):
        """Add a rabbit to the field."""
        self.rabbits.append(rabbit)

    def add_fox(self, fox):
        """Add a fox to the field."""
        self.foxes.append(fox)

    def move(self):
        """Move all rabbits and foxes within the field."""
        for r in self.rabbits:
            r.move()
        for f in self.foxes:
            f.move()

    def eat(self):
        """Manage the eating behavior of rabbits and foxes."""
        for r in self.rabbits:
            r.eat(self.field[r.x, r.y])
            self.field[r.x, r.y] = 0
        for f in self.foxes:
            prey = [r for r in self.rabbits if r.x == f.x and r.y == f.y]
            ate = False
            if prey:
                f.eat(1)
                ate = True
                self.rabbits.remove(prey[0])
            if not ate:
                f.eat(0)

    def survive(self):
        """Survive or die"""
        self.rabbits = [r for r in self.rabbits if (r.eaten > 0) and r.lifespan <= 10]
        self.foxes = [f for f in self.foxes if (f.eaten > 0 or not f.hungry()) and f.lifespan <= 20]

    def reproduce(self):
        """Handles reproduction of rabbits and foxes."""
        rabbits_born = []
        for r in self.rabbits:
            for _ in range(rnd.randint(1, OFFSPRING_RABBITS)):
                rabbits_born.append(r.reproduce())
        self.rabbits += rabbits_born

        foxes_born = []

        for f in self.foxes:
            for _ in range(1):
                foxes_born.append(f.reproduce())
        self.foxes += foxes_born

    def grow(self):
        """Simulates grass growth in the field."""
        growloc = (np.random.rand(SIZE, SIZE) < GRASS_RATE) * 1
        self.field = np.maximum(self.field, growloc)

    def generation(self):
        """Executes a generation cycle for the field, involving movement, eating, survival, reproduction,
        and grass growth."""
        self.move()
        self.eat()
        self.survive()
        self.reproduce()
        self.grow()

        self.field = np.ones(shape=(SIZE, SIZE), dtype=int)
        for r in self.rabbits:
            self.field[r.x, r.y] = 2
        for f in self.foxes:
            self.field[f.x, f.y] = 3


# List of colors
cmap = ListedColormap(['tan', 'green', 'blue', 'red'])


def animate(i, field, im):
    """Updates the animation frames by generating new generations of the field."""
    for _ in range(SPEED):
        field.generation()
    im.set_array(field.field)
    plt.title("Generation: " + str(i * SPEED) + " Rabbits: " + str(len(field.rabbits)) + " Foxes: " +
              str(len(field.foxes)))
    return im,


def main():

    # Create the ecosystem
    field = Field()

    # Initialize with some rabbits
    for _ in range(args.initial_rabbits):
        field.add_rabbit(Rabbit())

    # Initialize with some foxes
    for _ in range(args.initial_foxes):
        field.add_fox(Fox())

    # Setting up animations
    array = np.ones(shape=(args.field_size, args.field_size), dtype=int)
    fig = plt.figure(figsize=(10, 10))
    im = plt.imshow(array, cmap=cmap, interpolation='nearest', aspect='auto', vmin=0, vmax=3)
    anim = animation.FuncAnimation(fig, animate, fargs=(field, im), frames=CYCLE, interval=1000, repeat=True)
    plt.show()


if __name__ == '__main__':
    main()
