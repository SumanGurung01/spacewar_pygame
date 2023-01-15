"""
    Date : Sun Jan 15 2023 14:31:31 GMT+0530 (India Standard Time)
    Author : Suman Gurung
    Description : SpaceWar game using pygame
"""
import pygame
import random

pygame.init()

# CONSTANTS
WIN_HEIGHT,WIN_WIDTH = 700,700

SHIP_SPEED = 10
BULLET_SPEED = 20

WIN = pygame.display.set_mode((WIN_WIDTH , WIN_HEIGHT))
pygame.display.set_caption("Space War")

SCORE_FONT = pygame.font.SysFont("comicsans",25)

class Ship:
    def __init__(self , x , y):
        self.x = x
        self.y = y
        self.width = 60
        self.height = 60
        self.image = pygame.image.load("assets/ship.png")
        self.gunline_x = self.x+30
        self.gunline_y = self.y
    
    def move(self, direction):
        if direction == "up":
            self.y-= SHIP_SPEED
        if direction == "down":
            self.y+= SHIP_SPEED
        if direction == "right":
            self.x+= SHIP_SPEED
        if direction == "left":
            self.x-= SHIP_SPEED
        self.gunline_x = self.x+30
        self.gunline_y = self.y

class Bullet:
    def __init__(self , x , y):
        self.x = x
        self.y = y
        self.width = 5
        self.height = 10
        self.image = pygame.image.load("assets/bullet.png")
    
    def move(self):
        self.y -= BULLET_SPEED

class Enemy:
    def __init__(self , x , y):
        self.x = x
        self.y = y
        self.width = 50
        self.height = 30
        self.image = pygame.image.load("assets/enemy.png")
        self.dir = random.choice([1,-1])
    
    def move(self):
        self.x += self.dir * 10 
        self.y += 1
        if self.x <= 0 or self.x+self.width >= 700:
            self.dir*=-1

def gameover(win , enemies , ship ):
    for enemy in enemies:
        if ship.x + ship.width >= enemy.x and ship.x <= enemy.x + enemy.width:
            if ship.y <= enemy.y + enemy.height and ship.y + ship.height >= enemy.y :
                return True

    for enemy in enemies:
        if enemy.y + enemy.height >= WIN_HEIGHT:
                return True
    
    return False


def draw(win , ship , bullets , enemies ):
    win.fill((20,20,20))

    background = pygame.transform.scale( pygame.image.load("assets/bg.png"), (700,700))
    win.blit(background , (0 , 0))
    
    space_ship = pygame.transform.scale( pygame.image.load("assets/ship.png"), (60,60))
    win.blit(space_ship , (ship.x ,ship.y))

    for i,bullet in enumerate(bullets,start=0):
        bullet_sprite = pygame.transform.scale(bullet.image , (5,10))
        win.blit(bullet_sprite , (bullet.x , bullet.y))
        bullet.move()
        if bullet.y <= 0:
            bullets.pop(i)  

    for enemy in enemies:
        enemy_sprite = pygame.transform.scale(enemy.image , (50,30))
        win.blit(enemy_sprite , (enemy.x , enemy.y))
        enemy.move()

    pygame.display.update()

def handle_ship_movement(keys,ship):
    if keys[pygame.K_a] and ship.x - SHIP_SPEED >= 0:
        ship.move(direction = "left")
    if keys[pygame.K_d] and ship.x + ship.width + SHIP_SPEED <= WIN_WIDTH:
        ship.move(direction = "right")
    if keys[pygame.K_w] and ship.y - SHIP_SPEED >= 0:
        ship.move(direction = "up")
    if keys[pygame.K_s] and ship.y + ship.height + SHIP_SPEED <= WIN_HEIGHT:
        ship.move(direction = "down")
   
def handle_bullet_movement(keys , ship , bullets) :
    if keys[pygame.K_SPACE]: 
        if len(bullets) < 5: 
            bullet = Bullet(ship.gunline_x , ship.gunline_y)
            bullets.append(bullet)

def handle_hit(ship , bullets , enemies):
    for i , enemy in enumerate(enemies , start=0):
        for j , bullet in enumerate(bullets , start=0):
            if bullet.x + bullet.width//2 >= enemy.x and bullet.x + bullet.width//2 <= enemy.x + enemy.width:
                if bullet.y <= enemy.y + enemy.height and bullet.y >= enemy.y :
                    bullets.pop(j)
                    enemies.pop(i)

# MAIN
def main():

    run = True 
    
    clock = pygame.time.Clock()

    bullets = []
    enemies = []
    
    ship = Ship(WIN_WIDTH//2-30, WIN_HEIGHT-60)
    
    while run:

        clock.tick(60)

        if len(enemies)<10:
            enemy = Enemy(random.randrange(0,600) , random.randrange(0,300))
            enemies.append(enemy)
        
        draw(WIN , ship , bullets , enemies )
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                 pygame.quit()
   
    
        if gameover(WIN , enemies , ship):
            run=False
    
        keys = pygame.key.get_pressed() 
        handle_ship_movement(keys , ship) 
        handle_bullet_movement(keys , ship , bullets)
        handle_hit(ship , bullets , enemies) 

    run = True

    while run :
        background = pygame.transform.scale( pygame.image.load("assets/bg.png"), (700,700))
        WIN.blit(background , (0 , 0))
        text = SCORE_FONT.render("GAMEOVER",1,(255,255,255))
        WIN.blit(text,(WIN_WIDTH//2-50, WIN_HEIGHT//2))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        pygame.display.update()
    
    pygame.quit()
   
if __name__=="__main__":
    main()
