import sys

import pygame
import random
import math

# CONSTANTS
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 800
MENU_WIDTH = SCREEN_WIDTH/5

# Variables
menu_open = False
speed = 1
speed_button = pygame.Rect(25, 50, 150, 50)
virus_button = pygame.Rect(25, 110, 150, 50)
rcell_button = pygame.Rect(25, 170, 150, 50)
wcell_button = pygame.Rect(25, 230, 150, 50)

pathogens = []
rcells = []
wcells = []
infected = []

# Initialize Pygame Engine
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()

# Set Up
pygame.display.set_caption("ANTIGEN")

def create_virus(deadInfo):
    info = {
        'x': random.randint(4, SCREEN_WIDTH - 4),
        'y': random.randint(4, SCREEN_HEIGHT - 4),
        'radius': 4,
        'angle': random.uniform(0, 360),
    }

    if deadInfo is not None:
        info = {
            'x': deadInfo['x'],
            'y': deadInfo['y'],
            'radius': 4,
            'angle': random.uniform(0, 360)
        }

    pathogens.append(info)

def create_rcell():
    info = {
        'x': random.randint(40, SCREEN_WIDTH - 40),
        'y': random.randint(40, SCREEN_HEIGHT - 40),
        'radius': 20,
        'angle': random.uniform(0, 360),
    }

    rcells.append(info)

def create_wcell():
    info = {
        'x': random.randint(40, SCREEN_WIDTH - 40),
        'y': random.randint(40, SCREEN_HEIGHT - 40),
        'radius': 20,
        'angle': random.uniform(0, 360),
    }

    wcells.append(info)

def infect_cell(cell):
    info = {
        'x': cell['x'],
        'y': cell['y'],
        'radius': 20,
        'angle': random.uniform(0, 360),
    }

    infected.append(info)

def draw_menu():
    pygame.draw.rect(screen, (255,255,255), (0, 0, MENU_WIDTH, SCREEN_HEIGHT))
    arial = pygame.font.SysFont('arial', 20)

    pygame.draw.rect(screen, (44, 95, 80), speed_button)
    speed_button_text = arial.render("Increase Speed: " + str(speed), True, (255,255,255))
    screen.blit(speed_button_text, (30, 60))

    pygame.draw.rect(screen, (44, 95, 80), virus_button)
    spawn_button_text = arial.render("Create Virus", True, (255,255,255))
    screen.blit(spawn_button_text, (30, 120))

    pygame.draw.rect(screen, (44, 95, 80), rcell_button)
    spawn_button_text = arial.render("Create Red Cell", True, (255,255,255))
    screen.blit(spawn_button_text, (30, 180))

    pygame.draw.rect(screen, (44, 95, 80), wcell_button)
    spawn_button_text = arial.render("Create White Cell", True, (255,255,255))
    screen.blit(spawn_button_text, (30, 240))

def interaction():
    global menu_open, speed

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_m:
                menu_open = not menu_open
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if menu_open:
                if speed_button.collidepoint(event.pos):
                    speed += 1
                elif virus_button.collidepoint(event.pos):
                    create_virus(None)
                elif rcell_button.collidepoint(event.pos):
                    create_rcell()
                elif wcell_button.collidepoint(event.pos):
                    create_wcell()

def physics_step():

    # Update circles
    for circle in wcells:
        # Update circular motion
        circle['x'] += speed * math.cos(circle['angle'])
        circle['y'] += speed * math.sin(circle['angle'])
        # Change direction when hitting edges
        if circle['x'] < 0 or circle['x'] > SCREEN_WIDTH or circle['y'] < 0 or circle['y'] > SCREEN_HEIGHT:
            circle['angle'] += math.pi / 2
        pygame.draw.circle(screen, (255, 255, 255), (round(circle['x']), round(circle['y'])), circle['radius'])
        pygame.draw.circle(screen, (215, 215, 215), (round(circle['x']), round(circle['y'])), circle['radius']-1)

    for circle in rcells:
        # Update circular motion
        circle['x'] += speed * math.cos(circle['angle'])
        circle['y'] += speed * math.sin(circle['angle'])
        # Change direction when hitting edges
        if circle['x'] < 0 or circle['x'] > SCREEN_WIDTH or circle['y'] < 0 or circle['y'] > SCREEN_HEIGHT:
            circle['angle'] += math.pi / 2
        pygame.draw.circle(screen, (255, 0, 0), (round(circle['x']), round(circle['y'])), circle['radius'])
        pygame.draw.circle(screen, (215, 0, 0), (round(circle['x']), round(circle['y'])), circle['radius']-1)

    # Update infected circles
    for circle in pathogens:
        # Update circular motion
        circle['x'] += speed * math.cos(circle['angle'])
        circle['y'] += speed * math.sin(circle['angle'])
        # Change direction when hitting edges
        if circle['x'] < 0 or circle['x'] > SCREEN_WIDTH or circle['y'] < 0 or circle['y'] > SCREEN_HEIGHT:
            circle['angle'] += math.pi / 2
        pygame.draw.circle(screen, (252,87,153), (round(circle['x']), round(circle['y'])), circle['radius'])
        pygame.draw.circle(screen, (212,87,113), (round(circle['x']), round(circle['y'])), circle['radius']-1)

    for i, circle in enumerate(infected):
        circle['radius'] += .1

        pygame.draw.circle(screen, (217,152,70), (round(circle['x']), round(circle['y'])), circle['radius'])
        pygame.draw.circle(screen, (177,112,70), (round(circle['x']), round(circle['y'])), circle['radius'] - 1)

        if circle['radius'] > 50:
            for j in range(1, 10):
                create_virus(circle)

            if infected[i]:
                del infected[i]

    # Check collision with infected circles
    for i, cell in enumerate(rcells):
        for j, virus in enumerate(pathogens):
            distance = ((cell['x'] - virus['x']) ** 2 + (cell['y'] - virus['y']) ** 2) ** 0.5
            if distance <= cell['radius'] + virus['radius'] + 5:
                infect_cell(cell)

                if rcells[i]:
                    del rcells[i]
                if pathogens[j]:
                    del pathogens[j]

    for cell in wcells:
        for j, virus in enumerate(pathogens):
            distance = ((cell['x'] - virus['x']) ** 2 + (cell['y'] - virus['y']) ** 2) ** 0.5
            if distance <= cell['radius'] + virus['radius'] + 5:
                if pathogens[j]:
                    del pathogens[j]

while True:
    screen.fill((26,95,76))

    physics_step()
    interaction()

    if menu_open:
        draw_menu()

    pygame.display.flip()  # Update the display
    clock.tick(60)  # Limit to 60 frames per second