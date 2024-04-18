import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# Set up screen
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pandemic Simulator")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# Constants
NUM_CITIES = 5
INITIAL_INFECTED = 1
POPULATION_SIZE = 100
INFECTION_RATE = 0.1
RECOVERY_RATE = 0.02
DEATH_RATE = 0.01

# Class for cities
class City:
    def __init__(self, x, y):
        self.x = x
        self.y = y

# Create cities
cities = []
for i in range(NUM_CITIES):
    x = random.randint(50, WIDTH - 50)
    y = random.randint(50, HEIGHT - 50)
    cities.append(City(x, y))

# Class for humans
class Human:
    def __init__(self, city):
        self.city = city
        self.x = city.x
        self.y = city.y
        self.infected = False
        self.recovered = False
        self.dead = False

    def update(self):
        if not self.dead:
            if random.random() < INFECTION_RATE and not self.infected:
                self.infected = True
            if self.infected and not self.recovered:
                if random.random() < DEATH_RATE:
                    self.dead = True
                elif random.random() < RECOVERY_RATE:
                    self.recovered = True

    def draw(self):
        if self.infected:
            color = RED
        elif self.recovered:
            color = BLUE
        else:
            color = BLACK
        pygame.draw.circle(screen, color, (int(self.x), int(self.y)), 5)

# Create humans
humans = []
for _ in range(POPULATION_SIZE):
    city = random.choice(cities)
    humans.append(Human(city))

# Infect initial humans
for _ in range(INITIAL_INFECTED):
    humans[random.randint(0, POPULATION_SIZE - 1)].infected = True

# Main loop
def main():
    running = True
    while running:
        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Clear screen
        screen.fill(WHITE)

        # Update and draw humans
        for human in humans:
            human.update()
            human.draw()

        # Update display
        pygame.display.flip()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()

