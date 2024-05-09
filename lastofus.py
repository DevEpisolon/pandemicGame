import pygame
import random
import math

# Constants
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 800
WHITE = (255, 255, 255)
RED = (255, 0, 0)
NUM_WHITE_CIRCLES = 700# Increase the number of white circles
CIRCLE_RADIUS = 10
WHITE_CIRCLE_SPEED = .8
INFECTED_CIRCLE_SPEED = .3  # Adjusted for faster spread
MOVEMENT_THRESHOLD = 5

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()

# Function to create a new circle
def create_circle(color):
    return {
        'x': random.randint(CIRCLE_RADIUS, SCREEN_WIDTH - CIRCLE_RADIUS),
        'y': random.randint(CIRCLE_RADIUS, SCREEN_HEIGHT - CIRCLE_RADIUS),
        'color': color,
        'angle': random.uniform(0, 2 * math.pi),  # Random initial angle for circular motion
        'speed': WHITE_CIRCLE_SPEED
    }

# Create white circles
white_circles = [create_circle(WHITE) for _ in range(NUM_WHITE_CIRCLES)]

# Create infected circles (initially infected)
infected_circles = [{
    'x': random.randint(CIRCLE_RADIUS, SCREEN_WIDTH - CIRCLE_RADIUS),
    'y': random.randint(CIRCLE_RADIUS, SCREEN_HEIGHT - CIRCLE_RADIUS),
    'color': RED,
    'angle': random.uniform(0, 2 * math.pi),  # Random initial angle for movement
    'speed': INFECTED_CIRCLE_SPEED
} for _ in range(25)]  # Adjusted for initial infected count

# Main loop
running = True
while running:
    screen.fill((0, 0, 0))  # Clear the screen

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Update white circles
    for circle in white_circles:
        # Update circular motion
        circle['x'] += circle['speed'] * math.cos(circle['angle'])
        circle['y'] += circle['speed'] * math.sin(circle['angle'])
        # Change direction when hitting edges
        if circle['x'] < 0 or circle['x'] > SCREEN_WIDTH or circle['y'] < 0 or circle['y'] > SCREEN_HEIGHT:
            circle['angle'] += math.pi / 2
        pygame.draw.circle(screen, circle['color'], (round(circle['x']), round(circle['y'])), CIRCLE_RADIUS)

    # Update infected circles
    for infected_circle in infected_circles:
        # Update random movement
        infected_circle['x'] += infected_circle['speed'] * math.cos(infected_circle['angle'])
        infected_circle['y'] += infected_circle['speed'] * math.sin(infected_circle['angle'])
        # Change direction when hitting edges
        if infected_circle['x'] < 0 or infected_circle['x'] > SCREEN_WIDTH or infected_circle['y'] < 0 or infected_circle['y'] > SCREEN_HEIGHT:
            infected_circle['angle'] = random.uniform(0, 2 * math.pi)
        pygame.draw.circle(screen, infected_circle['color'], (round(infected_circle['x']), round(infected_circle['y'])), CIRCLE_RADIUS)

    # Check collision with infected circles
    for circle in white_circles:
        for infected_circle in infected_circles:
            distance = ((circle['x'] - infected_circle['x']) ** 2 + (circle['y'] - infected_circle['y']) ** 2) ** 0.5
            if distance < CIRCLE_RADIUS + MOVEMENT_THRESHOLD:
                circle['color'] = RED
                circle['speed'] = INFECTED_CIRCLE_SPEED

    pygame.display.flip()  # Update the display
    clock.tick(30)  # Limit to 60 frames per second

# Quit Pygame
pygame.quit()
