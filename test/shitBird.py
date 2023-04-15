import pygame
from pygame.locals import *
import random
import sys
import time
pygame.init()
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Square Game")
player = pygame.image.load("assets/youtube-comment.png").convert_alpha()
player = pygame.transform.scale(player, (40, 40))
player_rect = player.get_rect()
player_rect.x = 100
player_rect.y = screen_height // 2
gravity = 5
jump_height = 15
player_speed = 0
last_update = 0
obstacle_speed = 2
obstacles = []
score = 0
bullets = []
bullet_speed = 2
running = True
while running:
    screen.fill((255, 255, 255))
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
        if event.type == KEYDOWN:
            if event.key == K_SPACE:
                bullet_vector = [player_rect.x, player_rect.y]
                bullets.append({"rect": pygame.Rect(player_rect.x, player_rect.y, 5, 5), "vector": bullet_vector})
        if event.type == MOUSEBUTTONDOWN:
            player_speed = -jump_height
    if pygame.time.get_ticks() - last_update > 100:
        player_speed += gravity
        last_update = pygame.time.get_ticks()
    player_rect.y += player_speed
    if player_rect.y <= 0:
        player_rect.y = 0
    if player_rect.y >= screen_height - player_rect.height:
        pygame.quit()
        sys.exit()
    if random.randint(0, 500) < 5:
        new_obstacle = pygame.Rect(screen_width, random.randint(0, screen_height-40), 40, 40)
        obstacles.append(new_obstacle)
    for i, obstacle in enumerate(obstacles):
        obstacle.x -= obstacle_speed
        if obstacle.colliderect(player_rect):
            pygame.quit()
            sys.exit()
        if obstacle.x + obstacle.width < 0:
            obstacles.pop(i)
            score += 1
        pygame.draw.rect(screen, (0, 0, 255), obstacle)
    for bullet in bullets:
        bullet["rect"].x += bullet_speed
        for obstacle in obstacles:
            if bullet["rect"].colliderect(obstacle):
                obstacles.remove(obstacle)
                bullets.remove(bullet)
                break
        pygame.draw.rect(screen, (255, 0, 0), bullet["rect"])
    screen.blit(player, player_rect)
    pygame.display.update()
    time.sleep(0.01)
pygame.quit()