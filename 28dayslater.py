import pygame
import random
import math

# Constants
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 800
WHITE = (255, 255, 255)
RED = (255, 0, 0)
NUM_WHITE_CIRCLES = 800  # Adjust the number of white circles
CIRCLE_RADIUS = 10
MOVEMENT_THRESHOLD = 5

# Adjustable parameters for virus spread and threat potential
WHITE_CIRCLE_SPEED = 2  # Rate of spread for the virus
RED_CIRCLE_SPEED = .5  # Threat potential of the virus

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

# Create red circles
red_circles = [{
    'x': random.randint(CIRCLE_RADIUS, SCREEN_WIDTH - CIRCLE_RADIUS),
    'y': random.randint(CIRCLE_RADIUS, SCREEN_HEIGHT - CIRCLE_RADIUS),
    'color': RED,
    'angle': random.uniform(0, 2 * math.pi),  # Random initial angle for movement
    'speed': RED_CIRCLE_SPEED
} for _ in range(10)]

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

    # Update red circles
    for red_circle in red_circles:
        # Update random movement
        red_circle['x'] += red_circle['speed'] * math.cos(red_circle['angle'])
        red_circle['y'] += red_circle['speed'] * math.sin(red_circle['angle'])
        # Change direction when hitting edges
        if red_circle['x'] < 0 or red_circle['x'] > SCREEN_WIDTH or red_circle['y'] < 0 or red_circle['y'] > SCREEN_HEIGHT:
            red_circle['angle'] = random.uniform(0, 2 * math.pi)
        pygame.draw.circle(screen, red_circle['color'], (round(red_circle['x']), round(red_circle['y'])), CIRCLE_RADIUS)

    # Check collision with red circles
    for circle in white_circles:
        for red_circle in red_circles:
            distance = ((circle['x'] - red_circle['x']) ** 2 + (circle['y'] - red_circle['y']) ** 2) ** 0.5
            if distance < CIRCLE_RADIUS + MOVEMENT_THRESHOLD:
                circle['color'] = RED
                circle['speed'] = RED_CIRCLE_SPEED

    pygame.display.flip()  # Update the display
    clock.tick(60)  # Limit to 60 frames per second

# Quit Pygame
pygame.quit()

