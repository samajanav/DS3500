import random as rnd
import copy
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.colors import ListedColormap

SIZE = 400    # x/y dimensions of the field
WRAP = True  # When moving beyond the border, do we wrap around to the other size
GRASS_RATE = 0.1  # Probability of grass growing at any given location, e.g., 2%
SPEED = 1  # Number of generations per frame
OFFSPRING_RABBITS = 2  # The number of offspring when a rabbit reproduces
INIT_RABBITS = 1 # Number of starting rabbits
OFFSPRING_FOXES = 1 # The number of offspring when a rabbit reproduces
INIT_FOXES = 1 # Number of starting rabbits


class Rabbit:
    def __init__(self):
        self.x = rnd.randrange(0, SIZE)
        self.y = rnd.randrange(0, SIZE)
        self.eaten = 0
        self.lifespan = 0  # Initialize lifespan counter

    def reproduce(self):
        self.eaten = 0
        self.lifespan = 0  # Reset lifespan counter
        offspring = copy.deepcopy(self)
        # Limit offspring's spawn location within a certain distance from parent's location
        offspring.x = max(0, min(SIZE - 1, self.x + rnd.randint(-10, 10)))
        offspring.y = max(0, min(SIZE - 1, self.y + rnd.randint(-10, 10)))
        return offspring

    def eat(self, amount):
        self.eaten += amount

    def move(self):
        if WRAP:
            self.x = (self.x + rnd.choice([-1, 0, 1])) % SIZE
            self.y = (self.y + rnd.choice([-1, 0, 1])) % SIZE
        else:
            self.x = min(SIZE - 1, max(0, (self.x + rnd.choice([-1, 0, 1]))))
            self.y = min(SIZE - 1, max(0, (self.y + rnd.choice([-1, 0, 1]))))

        self.lifespan += 1  # Increment lifespan counter

class Fox:
    def __init__(self):
        self.x = rnd.randrange(0, SIZE)
        self.y = rnd.randrange(0, SIZE)
        self.eaten = 0
        self.hunger_counter = 0
        self.lifespan = 0  # Initialize lifespan counter

    def reproduce(self):
        self.eaten = 0
        self.hunger_counter = 0
        self.lifespan = 0  # Reset lifespan counter
        offspring = copy.deepcopy(self)
        # Limit offspring's spawn location within a certain distance from parent's location
        offspring.x = max(0, min(SIZE - 1, self.x + rnd.randint(-10, 10)))
        offspring.y = max(0, min(SIZE - 1, self.y + rnd.randint(-10, 10)))
        return offspring

    def eat(self, amount):
        self.eaten += amount
        self.hunger_counter = 0

    def hungry(self):
        if self.hunger_counter >= 10:
            return True
        else:
            return False

    def move(self):
        if WRAP:
            self.x = (self.x + rnd.choice([-2, -1, 0, 1, 2])) % SIZE
            self.y = (self.y + rnd.choice([-2, -1, 0, 1, 2])) % SIZE
        else:
            self.x = min(SIZE - 1, max(0, (self.x + rnd.choice([-2, -1, 0, 1, 2]))))
            self.y = min(SIZE - 1, max(0, (self.y + rnd.choice([-2, -1, 0, 1, 2]))))

        self.hunger_counter += 1
        self.lifespan += 1  # Increment lifespan counter


class Field:
    def __init__(self):
        self.rabbits = []
        self.foxes = []
        self.field = np.ones(shape=(SIZE, SIZE), dtype=int)

    def add_rabbit(self, rabbit):
        self.rabbits.append(rabbit)

    def add_fox(self, fox):
        self.foxes.append(fox)

    def move(self):
        for r in self.rabbits:
            r.move()
        for f in self.foxes:
            f.move()

    def eat(self):
        for r in self.rabbits:
            r.eat(self.field[r.x, r.y])
            self.field[r.x, r.y] = 0
        for f in self.foxes:
            prey = [r for r in self.rabbits if r.x == f.x and r.y == f.y]
            ate = False
            if prey:
                f.eat(1)
                #if not f.eat(0)
                ate = True
                self.rabbits.remove(prey[0])
            if not ate:
                f.eat(0)
                # self.add_fox(f.reproduce())

    def survive(self):
        self.rabbits = [r for r in self.rabbits if (r.eaten > 0 or not r.hungry()) and r.lifespan <= 10]
        self.foxes = [f for f in self.foxes if (f.eaten > 0 or not f.hungry()) and f.lifespan <= 20]

    def reproduce(self):
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
        growloc = (np.random.rand(SIZE, SIZE) < GRASS_RATE) * 1
        self.field = np.maximum(self.field, growloc)

    def generation(self):
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


cmap = ListedColormap(['tan', 'green', 'blue', 'red'])

def animate(i, field, im):
    for _ in range(SPEED):
        field.generation()
    im.set_array(field.field)
    plt.title("Generation: " + str(i * SPEED) + " Rabbits: " + str(len(field.rabbits)) + " Foxes: " +
              str(len(field.foxes)))
    return im,
def main():
    field = Field()

    for _ in range(INIT_RABBITS):
        field.add_rabbit(Rabbit())

    for _ in range(INIT_FOXES):
        field.add_fox(Fox())

    array = np.ones(shape=(SIZE, SIZE), dtype=int)
    fig = plt.figure(figsize=(10, 10))
    im = plt.imshow(array, cmap=cmap, interpolation='nearest', aspect='auto', vmin=0, vmax=3)
    anim = animation.FuncAnimation(fig, animate, fargs=(field, im), frames=10**100, interval=1000, repeat=True)
    plt.show()

if __name__ == '__main__':
    main()


