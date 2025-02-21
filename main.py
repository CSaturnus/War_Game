import pygame
import numpy as np
import math
import random

pygame.init()

HEIGHT, WIDTH = 500, 500

screen = pygame.display.set_mode((HEIGHT, WIDTH))
FPS = 60

Guys_image = pygame.image.load('assets/sprites/Guys.png')
Guys_image = pygame.transform.scale(pygame.image.load('assets/sprites/Guys.png'), (Guys_image.get_width()*2,Guys_image.get_height()*2))

Minion_image = pygame.image.load('assets/sprites/Guys.png')


BLACK = (0,0,0)

def get_sprite(sheet, x, y, width, height):
    sprite = pygame.Surface((width, height), pygame.SRCALPHA)
    sprite.blit(sheet, (0, 0), (x, y, width, height))
    return sprite

class Player:
    def __init__(self, posx, posy, colour = 0, speed = 1):
        self.posx = posx
        self.posy = posy
        self.colour = colour
        self.width = Guys_image.get_width() // 4
        self.height = Guys_image.get_height()
        self.image = get_sprite(Guys_image, self.width * self.colour, 0, self.width, self.height)
        self.image_rotated = get_sprite(Guys_image, self.width * self.colour, 0, self.width, self.height)
        self.angle = 0 
        self.movement = False
        
        self.movement_turn = -1.1

        self.speed_initial = speed
        self.speed = speed
        self.speed_limit = 2.5
        self.speed_increase = 1.005
        self.speed_decrease = 0.990
        self.speed_increase_check = False

        self.trail = []
        self.trail_length_max = 0
        self.counter_trail = 0

    def idle(self):
        self.counter_trail += 1
        if self.counter_trail > 5:
            self.trail.append((self.posx + self.width//2, self.posy))
            self.counter_trail = 0
        if len(self.trail) > self.trail_length_max:
            self.trail.pop(0)

    def trail_maker(self):
        self.counter_trail += 1
        if self.counter_trail > 5:
            self.trail.append((self.posx + self.width//2, self.posy))
            self.counter_trail = 0
        if len(self.trail) > self.trail_length_max:
            self.trail.pop(0)

    def move(self, dx=0, dy=0):
        if dx != 0 or dy != 0:
            magnitude = math.sqrt(dx**2 + dy**2)
            if magnitude != 0:
                dx /= magnitude
                dy /= magnitude

            self.posx += dx * self.speed
            self.posy += dy * self.speed

            self.speed *= self.speed_increase
            if self.speed > self.speed_limit:
                self.speed = self.speed_limit
        else:
            self.speed *= self.speed_decrease
            if self.speed < self.speed_initial:
                self.speed = self.speed_initial

        print(self.speed)

    def display(self):

        if self.angle > 10.1 or self.angle < -10.1:
            self.movement_turn = -self.movement_turn
        if self.movement == True:
            self.angle += self.movement_turn
        elif self.movement == False and abs(self.angle) > 0:
            self.angle -= self.movement_turn
            if self.angle < 0.2:
                self.angle = 0 
        self.image_rotated = pygame.transform.rotate(self.image, self.angle)

        rotated_rect = self.image_rotated.get_rect(midbottom=(self.posx + self.width // 2, self.posy))

        for i, (x, y) in enumerate(self.trail):
            alpha = int((i / self.trail_length_max) * 255)  # Gradual fading
            pygame.draw.circle(screen, (255, 255, 255, alpha), (int(x), int(y)), 3)

        screen.blit(self.image_rotated, rotated_rect)

class Minion:
    def __init__(self, posx, posy, colour = random.randint(0,3), speed = 1):
        self.posx = posx
        self.posy = posy
        self.colour = colour
        self.width = Minion_image.get_width() // 4
        self.height = Minion_image.get_height()
        self.image = get_sprite(Minion_image, self.width * self.colour, 0, self.width, self.height)
        self.image_rotated = get_sprite(Minion_image, self.width * self.colour, 0, self.width, self.height)
        self.angle = 0 
        self.movement = True
        
        self.movement_turn = -1.1

        self.speed_initial = speed
        self.speed = speed
        self.speed_increase = 1.005
        self.speed_decrease = 0.990
        self.speed_increase_check = False
        self.idle_walk_angle = random.random() * 2 * math.pi
        self.idle_walk_radius = random.randint(0,50)

    def move_idle(self, posx_player = 0, posy_player = 0):
        self.posx_reach = posx_player + math.cos(self.idle_walk_angle) * self.idle_walk_radius
        self.posy_reach = posy_player + math.sin(self.idle_walk_angle) * self.idle_walk_radius

        dx = (self.posx_reach - self.posx)
        dy = (self.posy_reach - self.posy)

        if dx**2 + dy**2 < 0.04:
            self.posx = self.posx_reach
            self.posy = self.posy_reach
            self.movement = False
            if random.randint(1, 60) == 1:
                self.idle_walk_angle = random.random() * 2 * math.pi
                self.idle_walk_radius = random.randint(0, 50)
                self.movement = True

        magnitude = math.sqrt(dx**2 + dy**2) * 3

        if magnitude != 0:
            self.posx_dir = dx / magnitude
            self.posy_dir = dy / magnitude
        else:
            self.posx_dir = 0
            self.posy_dir = 0
        
        self.posx += self.posx_dir
        self.posy += self.posy_dir

    def follow_player(self, trail):
        self.movement = True

        dx = (trail[0] - self.width//2 - self.posx)
        dy = (trail[1] - self.posy)

        magnitude = math.sqrt(dx**2 + dy**2)

        if magnitude != 0:
            self.posx_dir = dx / magnitude * 2.5
            self.posy_dir = dy / magnitude * 2.5
        else:
            self.posx_dir = 0
            self.posy_dir = 0
        
        self.posx += self.posx_dir
        self.posy += self.posy_dir        

    def display(self):

        if self.angle > 6 or self.angle < -6:
            self.movement_turn = -self.movement_turn
        if self.movement == True:
            self.angle += self.movement_turn
        elif self.movement == False and abs(self.angle) > 0:
            self.angle -= self.movement_turn
            if self.angle < 0.2:
                self.angle = 0 
        
        self.image_rotated = pygame.transform.rotate(self.image, self.angle)

        rotated_rect = self.image_rotated.get_rect(midbottom=(self.posx + self.width // 2, self.posy))

        screen.blit(self.image_rotated, rotated_rect)

def main():
    running = True
    clock = pygame.time.Clock()

    player = Player(WIDTH//2, HEIGHT//2, 0)
    minion_list = [Minion(WIDTH//2, HEIGHT//2, colour = random.randint(0,3)), Minion(WIDTH//2, HEIGHT//3, colour = random.randint(0,3))]

    for i in range(10):
        minion_list.append(Minion(WIDTH//2, HEIGHT//2, colour = random.randint(0,3)))

    direction = [0,0]

    while running:
        screen.fill(BLACK)

        player.trail_length_max = len(minion_list)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        keys = pygame.key.get_pressed()
        movement_map = {
            pygame.K_w: (0, -1),
            pygame.K_s: (0, 1),
            pygame.K_a: (-1, 0),
            pygame.K_d: (1, 0),
        }

        direction = [0, 0]
        player.movement = False
        for key, (dx, dy) in movement_map.items():
            if keys[key]:
                direction[0] += dx  # Correct way to update x direction
                direction[1] += dy  # Correct way to update y direction
                player.movement = True
        


        player.move(direction[0], direction[1])
        player.trail_maker()

        if player.movement == True:
            for i, postion in enumerate(player.trail):
                minion_list[i].follow_player(postion)
        else:
            for minion in minion_list:
                minion.move_idle(posx_player = player.posx, posy_player = player.posy)

        entities = minion_list + [player]  
        entities.sort(key=lambda entity: entity.posy)
        for entity in entities:
            entity.display()

        pygame.display.update()
        clock.tick(FPS)

if __name__ == '__main__':
    main()
pygame.quit()