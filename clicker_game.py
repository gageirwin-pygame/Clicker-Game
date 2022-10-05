from turtle import update
import pygame
from datetime import datetime
pygame.font.init()
from enum import Enum, auto


WIDTH = 1920
HEIGHT = 1080
pygame.display.set_caption("Game")
screen = pygame.display.set_mode((WIDTH, HEIGHT))
TEXT_FONT = pygame.font.SysFont('comicsans', 25)
FPS = 60


MONSTER_LOCATION = (WIDTH//2, HEIGHT//2)
MONSTER_SIZE = (100,100)

HEALTH_BAR_LOCATION = (WIDTH//2-300, HEIGHT//2+200)
HEALTH_BAR_SIZE = (1000,100)


# colors
WHITE = (255, 255, 255)
BLACK = (0, 0 , 0)
GREEN = (0, 255, 0)
RED = (255, 0 , 0)
YELLOW = (255, 255, 0)
BLUE = (0, 0, 255)
PURPLE = (255, 0, 255)
GREY_1 = (128, 128, 128)
GREY_2 = (164, 164, 164)
GREY_3 = (192, 192, 192)


class ButtonAction(Enum):
    Clicked = auto()
    NotClicked = auto()

class Upgrade():

    def __init__(self, x, y, text='', amount=0, cost=0):
        self.cost = cost
        self.level = 0
        self.rect = pygame.Rect(x,y,100,100)
        self.text = text
        self.amount = amount
        self.clicked = False
        self.hovered = False

    def draw(self, money):
        if self.clicked:
            pygame.draw.rect(screen,YELLOW, self.rect)
        elif money < self.cost:
            pygame.draw.rect(screen,GREY_1, self.rect)
        else:
            pygame.draw.rect(screen,BLACK, self.rect)
        button_text = TEXT_FONT.render(str(self.text), 1, WHITE)
        screen.blit(button_text, (self.rect.x + (self.rect.width - button_text.get_width())//2, self.rect.y + (self.rect.width - button_text.get_height())//2))
        button_text = TEXT_FONT.render(str(self.cost), 1, BLACK)
        screen.blit(button_text, (self.rect.x + 100, self.rect.y))
        if self.hovered and not self.clicked:
            pygame.draw.rect(screen,BLUE, self.rect, 5)
        action = 0
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            self.hovered = True
            if pygame.mouse.get_pressed()[0] and self.clicked == False and money >= self.cost:
                self.clicked = True
                action = self.cost
        else:
            self.hovered = False
        if not pygame.mouse.get_pressed()[0]:
            self.clicked = False
        return action

class HealthBar():

    def __init__(self, health, scale=1):
        self.starting = health
        self.current = self.starting
        self.Background = pygame.Rect(HEALTH_BAR_LOCATION[0], HEALTH_BAR_LOCATION[1], HEALTH_BAR_SIZE[0], HEALTH_BAR_SIZE[1])
        self.Bar = pygame.Rect(HEALTH_BAR_LOCATION[0], HEALTH_BAR_LOCATION[1], HEALTH_BAR_SIZE[0], HEALTH_BAR_SIZE[1])

    def removeHealth(self, amount):
        self.current = int(self.current - amount)
        AdjustedWidth = int(self.current/self.starting * HEALTH_BAR_SIZE[0])
        self.Bar = pygame.Rect(HEALTH_BAR_LOCATION[0], HEALTH_BAR_LOCATION[1], AdjustedWidth, HEALTH_BAR_SIZE[1])

    def draw(self):
        pygame.draw.rect(screen, BLACK, self.Background, 5)
        pygame.draw.rect(screen, RED, self.Bar)
        button_text = TEXT_FONT.render(str(self.current), 1, BLACK)
        screen.blit(button_text, (HEALTH_BAR_LOCATION[0], HEALTH_BAR_LOCATION[1]))

class Monster():

    def __init__(self, health):
        self.rect = pygame.Rect(MONSTER_LOCATION[0], MONSTER_LOCATION[1], MONSTER_SIZE[0], MONSTER_SIZE[1])
        self.health = health
        self.clicked = False

    def Damage(self, amount):
        self.health = int(self.health - amount)

    def draw(self):
        if self.clicked:
            pygame.draw.rect(screen,YELLOW, self.rect)
        else:
            pygame.draw.rect(screen,BLACK, self.rect)

        action = ButtonAction.NotClicked
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            if pygame.mouse.get_pressed()[0] and self.clicked == False:
                self.clicked = True
                action = ButtonAction.Clicked
        if not pygame.mouse.get_pressed()[0]:
            self.clicked = False
        return action  

class Game():

    def __init__(self):
        self.damagePerSecond = 0
        self.damagePerClick = 100
        self.money = 0
        self.level = 0

        self.health = 5_000
        self.HealthBar = HealthBar(self.health)
        self.monster = Monster(self.health)

        self.dps_upgrades = [
            Upgrade(50, 50, '+100 DPS', 100, 100),
            Upgrade(50, 200, '+200 DPS', 200, 200),
            Upgrade(50, 350, '+300 DPS', 300, 300),
            Upgrade(50, 500, '+400 DPS', 400, 400),
            Upgrade(50, 650, '+20k DPS', 10_000, 10_000),
            Upgrade(50, 800, '+20k DPS', 20_000, 20_000),
        ]

        self.dpc_upgrades = [
            Upgrade(250, 50, '+100 DPC', 100, 100),
            Upgrade(250, 200, '+200 DPC', 200, 200),
            Upgrade(250, 350, '+300 DPC', 300, 300),
            Upgrade(250, 500, '+400 DPC', 400, 400),
            Upgrade(250, 650, '+20k DPC', 10_000, 10_000),
            Upgrade(250, 800, '+20k DPC', 20_000, 20_000),
        ]


    def NextMonster(self):
        if self.monster.health <= 0:
            self.health *= 1.2
            self.HealthBar = HealthBar(self.health)
            self.monster = Monster(self.health)
            self.money += 1000
            self.level += 1           

    def IncreaseDPS(self, amount):
        self.damagePerSecond += amount

    def IncreaseDPC(self, amount):
        self.damagePerClick += amount

    def DamageMonsterPerSecond(self):
        self.monster.Damage(self.damagePerSecond/FPS)
        self.HealthBar.removeHealth(self.damagePerSecond/FPS)

    def DamageMonsterClick(self):
        self.monster.Damage(self.damagePerClick)
        self.HealthBar.removeHealth(self.damagePerClick)


    def draw(self):
        screen.fill(WHITE)

        button_text = TEXT_FONT.render("DPS: " + str(self.damagePerSecond), 1, BLACK)
        screen.blit(button_text, (WIDTH//2, (button_text.get_height())))
        button_text = TEXT_FONT.render("DPC: " + str(self.damagePerClick), 1, BLACK)
        screen.blit(button_text, (WIDTH//2, (50 + button_text.get_height())))
        button_text = TEXT_FONT.render("GOLD: " + str(self.money), 1, BLACK)
        screen.blit(button_text, (WIDTH//2, (100 + button_text.get_height())))
        button_text = TEXT_FONT.render("Level: " + str(self.level), 1, BLACK)
        screen.blit(button_text, (WIDTH//2, (150 + button_text.get_height())))
       

        action = self.monster.draw()
        if action == ButtonAction.Clicked:
            self.DamageMonsterClick()       


        for dps_upgrade in self.dps_upgrades:
            action = dps_upgrade.draw(self.money)
            if action:
                self.money -= action
                self.IncreaseDPS(dps_upgrade.amount)

        for dpc_upgrade in self.dpc_upgrades:
            action = dpc_upgrade.draw(self.money)
            if action:
                self.money -= action
                self.IncreaseDPC(dpc_upgrade.amount)


        self.DamageMonsterPerSecond()

        self.HealthBar.draw()
        self.NextMonster()


def main():
    game = Game()
    clock = pygame.time.Clock()
    running = True
    while running:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    game.reset_game()
                # if event.key == pygame.K_h:
                #     game.toggle_ending_screen()
        game.draw()

        pygame.display.update()

if __name__ == '__main__':
    main()