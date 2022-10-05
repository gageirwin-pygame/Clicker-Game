from turtle import update
import pygame
from datetime import datetime
pygame.font.init()
from enum import Enum, auto


WIDTH = 1920
HEIGHT = 1080
pygame.display.set_caption("Game")
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
TEXT_FONT = pygame.font.SysFont('comicsans', 25)
FPS = 60


MONSTER_LOCATION = (WIDTH//2, HEIGHT//2)
MONSTER_SIZE = (100,100)

HEALTH_BAR_LOCATION = (WIDTH//2-100, HEIGHT//2+200)
HEALTH_BAR_SIZE = (800,70)


# colors
WHITE = (255, 255, 255)
BLACK = (0, 0 , 0)
GREEN = (0, 255, 0)
RED = (255, 0 , 0)
YELLOW = (255, 255, 0)
BLUE = (0, 0, 255)
LIGHT_BLUE = (173, 216, 230)
PURPLE = (255, 0, 255)
GREY_1 = (128, 128, 128)
GREY_2 = (164, 164, 164)
GREY_3 = (192, 192, 192)


class ButtonAction(Enum):
    Clicked = auto()
    NotClicked = auto()


class HealthBar():

    def __init__(self, health, scale=1):
        self.starting = health
        self.current = self.starting
        self.Background = pygame.Rect(HEALTH_BAR_LOCATION[0], HEALTH_BAR_LOCATION[1], HEALTH_BAR_SIZE[0], HEALTH_BAR_SIZE[1])
        self.Bar = pygame.Rect(HEALTH_BAR_LOCATION[0], HEALTH_BAR_LOCATION[1], HEALTH_BAR_SIZE[0], HEALTH_BAR_SIZE[1])

    def Damage(self, amount):
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
        self.damagePerClick = 400
        self.money = 0
        self.level = 0
        self.reward = 1_000

        self.health = 5_000
        self.HealthBar = HealthBar(self.health)
        self.monster = Monster(self.health)


        self.test = Book()


    def NextMonster(self):
        if self.monster.health <= 0:
            self.health = int(self.health * 1.2)
            self.HealthBar = HealthBar(self.health)
            self.monster = Monster(self.health)
            self.money += self.reward
            self.reward = int(self.reward * 1.01)
            self.level += 1           

    def IncreaseDPS(self, amount):
        self.damagePerSecond += amount

    def IncreaseDPC(self, amount):
        self.damagePerClick += amount

    def DamageMonsterPerSecond(self):
        self.monster.Damage(self.damagePerSecond/FPS)
        self.HealthBar.Damage(self.damagePerSecond/FPS)

    def DamageMonsterClick(self):
        self.monster.Damage(self.damagePerClick)
        self.HealthBar.Damage(self.damagePerClick)


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


        self.DamageMonsterPerSecond()

        self.HealthBar.draw()
        self.NextMonster()

        money_spent, dps_increase = self.test.draw(self.money)
        self.money -= money_spent
        self.IncreaseDPS(dps_increase)
            


class Book():

    def __init__(self):
        self.current_page = 0
        self.pages = [
            Page(1, [("Super Clicks", 1_000, 100),("Super Duper Clicks", 10_000, 1_000),("Ultra Clicks", 100_000, 10_000),("God Clicks", 1_000_000, 100_000),("Secret Clicks", 100_000_000, 1_000)])
        ]


    def draw(self, money):
        money_spent, dps_increase = self.pages[self.current_page].draw(money)
        # next and last buttons
        # nextbutton = Button()
        # if self.current_page+1 < len(self.pages):
        #     action = nextbutton.draw()
        #     if action:
        #         self.current_page += 1

        # prevbutton = Button()
        # if self.current_page-1 >= 0:
        #     action = prevbutton.draw()
        #     if action:
        #         self.current_page -= 1
        return(money_spent, dps_increase)

class Page():

    def __init__(self, page_number, spells):
        x, y = 50, 50
        self.page_number = page_number
        self.page_rect = pygame.Rect(x, y, 620, len(spells)*160+110)
        self.spells = [Upgrade(x+10, 10+y+160*index, name, dps, cost) for index, (name, dps, cost) in enumerate(spells)]
            

    def draw(self, money):
        pygame.draw.rect(screen, GREY_3, self.page_rect, border_radius=10)
        text = TEXT_FONT.render(f"PAGE: {self.page_number}", 1, BLACK)
        screen.blit(text, (self.page_rect.x + (self.page_rect.width - text.get_width())//2, self.page_rect.y + self.page_rect.height-text.get_height()-50))

        money_spent = 0
        dps_increase = 0

        for spell in self.spells:
            action = spell.draw(money)
            if action:
                spell.LevelUp()
                money_spent = action
                dps_increase = spell.dps

        return(money_spent, dps_increase)

class Upgrade():

    def __init__(self, x, y, name='', dps=0, cost=0, dps_scale=1.05, cost_scale=1.01):
        block_size = (600, 150)
        upgrade_button_size = (200, 100)
        self.block_rect = pygame.Rect(x, y, block_size[0], block_size[1])
        self.button_rect = pygame.Rect(x + upgrade_button_size[0]//10, y + (block_size[1]-upgrade_button_size[1])//2, upgrade_button_size[0], upgrade_button_size[1])

        self.level = 0
        self.name = name
        self.cost = cost
        self.dps = dps
        self.dps_scale = dps_scale
        self.cost_scale = cost_scale
        
        self.clicked = False
        self.hovered = False

    def LevelUp(self):
        self.level += 1
        self.cost = int(self.cost * self.cost_scale)
        self.dps = int(self.dps * self.dps_scale)

    def draw(self, money):

        pygame.draw.rect(screen, GREY_1, self.block_rect, border_radius=10)

        if self.clicked:
            pygame.draw.rect(screen, YELLOW, self.button_rect, border_radius=10)

        if self.hovered and not self.clicked:
            pygame.draw.rect(screen, LIGHT_BLUE, self.button_rect, border_radius=10)
        else:
            pygame.draw.rect(screen, BLUE, self.button_rect, border_radius=10)

        pygame.draw.rect(screen, BLACK, self.button_rect, 5, border_radius=10)

        text = TEXT_FONT.render(f"LVL: {self.level}", 1, WHITE)
        seper = (self.button_rect.height - 2*text.get_height())//3
        x_pos = self.button_rect.x + (self.button_rect.width - text.get_width())//2
        screen.blit(text, (x_pos, self.button_rect.y + seper))
        text = TEXT_FONT.render(f"GOLD: {self.cost}", 1, WHITE)
        x_pos = self.button_rect.x + (self.button_rect.width - text.get_width())//2
        screen.blit(text, (x_pos, self.button_rect.y + 2*seper + text.get_height()))

        text = TEXT_FONT.render(f"{self.name}", 1, WHITE)
        seper = (self.block_rect.height - 3*text.get_height())//4
        x_pos = self.button_rect.x + self.button_rect.width + self.button_rect.width//10
        screen.blit(text, (x_pos, self.block_rect.y + seper))
        text = TEXT_FONT.render(f"DPS: {self.dps}", 1, WHITE)
        screen.blit(text, (x_pos, self.block_rect.y + 2*seper + text.get_height()))

        action = 0
        if self.button_rect.collidepoint(pygame.mouse.get_pos()):
            self.hovered = True
            if pygame.mouse.get_pressed()[0] and self.clicked == False and money >= self.cost:
                self.clicked = True
                action = self.cost
        else:
            self.hovered = False
        if not pygame.mouse.get_pressed()[0]:
            self.clicked = False
        return action


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