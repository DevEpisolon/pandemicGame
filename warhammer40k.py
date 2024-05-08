import pygame
import random
import math

# Constants
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 800
WHITE = (255, 255, 255)
RED = (255, 0, 0)
NUM_WHITE_CIRCLES = 1000  # Increase the number of white circles
CIRCLE_RADIUS = 10
INFECTED_CIRCLE_RADIUS = 15  # Adjusted radius for infected circles
WHITE_CIRCLE_SPEED = 1
INFECTED_CIRCLE_SPEED = 3.5  # Adjusted for faster spread
MOVEMENT_THRESHOLD = 5

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()

# Function to create a new circle
def create_circle(color, radius):
    return {
        'x': random.randint(radius, SCREEN_WIDTH - radius),
        'y': random.randint(radius, SCREEN_HEIGHT - radius),
        'color': color,
        'radius': radius,
        'angle': random.uniform(0, 2 * math.pi),  # Random initial angle for circular motion
        'speed': WHITE_CIRCLE_SPEED
    }

# Create white circles
white_circles = [create_circle(WHITE, CIRCLE_RADIUS) for _ in range(NUM_WHITE_CIRCLES)]

# Create infected circles (initially infected)
infected_circles = [{
    'x': random.randint(INFECTED_CIRCLE_RADIUS, SCREEN_WIDTH - INFECTED_CIRCLE_RADIUS),
    'y': random.randint(INFECTED_CIRCLE_RADIUS, SCREEN_HEIGHT - INFECTED_CIRCLE_RADIUS),
    'color': RED,
    'radius': INFECTED_CIRCLE_RADIUS,
    'angle': random.uniform(0, 2 * math.pi),  # Random initial angle for movement
    'speed': INFECTED_CIRCLE_SPEED
} for _ in range(500)]  # Adjusted for initial infected count

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
        pygame.draw.circle(screen, circle['color'], (round(circle['x']), round(circle['y'])), circle['radius'])

    # Update infected circles
    for infected_circle in infected_circles:
        # Update random movement
        infected_circle['x'] += infected_circle['speed'] * math.cos(infected_circle['angle'])
        infected_circle['y'] += infected_circle['speed'] * math.sin(infected_circle['angle'])
        # Change direction when hitting edges
        if infected_circle['x'] < 0 or infected_circle['x'] > SCREEN_WIDTH or infected_circle['y'] < 0 or infected_circle['y'] > SCREEN_HEIGHT:
            infected_circle['angle'] = random.uniform(0, 2 * math.pi)
        pygame.draw.circle(screen, infected_circle['color'], (round(infected_circle['x']), round(infected_circle['y'])), infected_circle['radius'])

    # Check collision with infected circles
    for circle in white_circles:
        for infected_circle in infected_circles:
            distance = ((circle['x'] - infected_circle['x']) ** 2 + (circle['y'] - infected_circle['y']) ** 2) ** 0.5
            if distance <= circle['radius'] + infected_circle['radius'] + MOVEMENT_THRESHOLD:
                circle['color'] = RED
                circle['speed'] = INFECTED_CIRCLE_SPEED
                circle['radius'] = INFECTED_CIRCLE_RADIUS

    pygame.display.flip()  # Update the display
    clock.tick(60)  # Limit to 60 frames per second

# Quit Pygame
pygame.quit()
