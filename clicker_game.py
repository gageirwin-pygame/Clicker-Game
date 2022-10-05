from turtle import update
import pygame
pygame.font.init()
from enum import Enum, auto


WIDTH = 1920
HEIGHT = 1080
pygame.display.set_caption("Game")
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
TEXT_FONT = pygame.font.SysFont('comicsans', 25)
FPS = 60



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


class Monster():

    x_pos, y_pos = (int(WIDTH*0.75), int(HEIGHT*0.23))
    width, height = int(WIDTH*0.26), int(HEIGHT*0.46)

    def __init__(self, name, health):
        self.name = name
        self.hitbox_rect = pygame.Rect(Monster.x_pos-Monster.width//2, Monster.y_pos, Monster.width, Monster.height)
        self.health = health
        self.clicked = False
        self.healthbar = HealthBar(self.health)

    def Damage(self, amount):
        self.health = int(self.health - amount)
        self.healthbar.CurrentHealth(self.health)

    def draw(self):
        self.healthbar.draw()
        name_text = TEXT_FONT.render(f"{self.name}", 1, BLACK)
        screen.blit(name_text, (Monster.x_pos-name_text.get_width()//2, Monster.y_pos-name_text.get_height()))

        if self.clicked:
            pygame.draw.rect(screen,YELLOW, self.hitbox_rect, 8, border_radius=10)
        else:
            pygame.draw.rect(screen,BLACK, self.hitbox_rect, 8, border_radius=10)

        action = ButtonAction.NotClicked
        if self.hitbox_rect.collidepoint(pygame.mouse.get_pos()):
            if pygame.mouse.get_pressed()[0] and self.clicked == False:
                self.clicked = True
                action = ButtonAction.Clicked
        if not pygame.mouse.get_pressed()[0]:
            self.clicked = False
        return action  

class HealthBar():

    x_pos, y_pos = (int(WIDTH*0.75), int(HEIGHT*0.23) + Monster.height)
    width, height = int(WIDTH*0.26), int(HEIGHT*0.11)

    def __init__(self, health):
        self.starting = health
        self.current = self.starting
        self.Background = pygame.Rect(HealthBar.x_pos-HealthBar.width//2, HealthBar.y_pos, HealthBar.width, HealthBar.height)
        self.Bar = pygame.Rect(HealthBar.x_pos-HealthBar.width//2, HealthBar.y_pos, HealthBar.width, HealthBar.height)

    def CurrentHealth(self, health):
        self.current = health
        AdjustedWidth = int(self.current/self.starting * HealthBar.width)
        self.Bar = pygame.Rect(HealthBar.x_pos-HealthBar.width//2, HealthBar.y_pos, AdjustedWidth, HealthBar.height)

    def draw(self):
        pygame.draw.rect(screen, RED, self.Bar, border_radius=10)
        pygame.draw.rect(screen, BLACK, self.Background, 8, border_radius=10)
        # button_text = TEXT_FONT.render(str(self.current), 1, BLACK)
        # screen.blit(button_text, (HEALTH_BAR_LOCATION[0], HEALTH_BAR_LOCATION[1]))
            
class Button():

    def __init__(self, x, y) -> None:
        self.button_rect = pygame.Rect(x, y, 50, 50)
        self.clicked = False

    def draw(self):
        pygame.draw.rect(screen, BLACK, self.button_rect, border_radius=10)
        action = 0
        if self.button_rect.collidepoint(pygame.mouse.get_pos()):
            self.hovered = True
            if pygame.mouse.get_pressed()[0] and self.clicked == False:
                self.clicked = True
                action = 1
        else:
            self.hovered = False
        if not pygame.mouse.get_pressed()[0]:
            self.clicked = False
        return action

class Book():

    x_pos, y_pos = int(WIDTH*0.025), int(HEIGHT*0.05)
    width, height = int(WIDTH*0.34), int(HEIGHT*0.74)

    def __init__(self):
        self.current_page = 0
        self.nextbutton = Button(Book.x_pos + int(Book.width*0.9), Book.y_pos + int(Book.height*0.9))
        self.prevbutton = Button(Book.x_pos + int(Book.width*0.1), Book.y_pos + int(Book.height*0.9))
        self.pages = [
            Page([("Water Ball", 1_000, 10),("Ice Ball", 10_000, 15),("Fire Ball", 100_000, 20),("Thunder Bolt", 1_000_000, 30)]),
            Page([("Rock Throw", 1_000, 100),("Heaven's Light", 10_000, 1_000),("Shadow Ball", 100_000, 10_000),("Water Spear", 1_000_000, 100_000)]),
            Page([("Ice Spear", 100_000_000, 1_000),("Wind Blast", 100_000_000, 40)])
        ]

    def draw(self, money):
        money_spent, dps_increase = self.pages[self.current_page].draw(money, self.current_page+1)
        
        if self.current_page+1 < len(self.pages):
            action = self.nextbutton.draw()
            if action:
                self.current_page += 1


        if self.current_page-1 >= 0:
            action = self.prevbutton.draw()
            if action:
                self.current_page -= 1

        return(money_spent, dps_increase)

class Page():

    x_pos, y_pos = int(WIDTH*0.025), int(HEIGHT*0.05)
    width, height = int(WIDTH*0.34), int(HEIGHT*0.74)
    max_spells = 4

    def __init__(self, spells):
        self.page_rect = pygame.Rect(Page.x_pos, Page.y_pos, Page.width, Page.height)
        x_padding = int(Page.width*0.05)
        y_padding = int(Page.height*0.1)
        spell_padding = int(Page.height*0.01)
        self.spells = [Spell(Page.x_pos+x_padding, y_padding+Page.y_pos+(Spell.height+spell_padding)*index, name, dps, cost) for index, (name, dps, cost) in enumerate(spells)]

    def draw(self, money, page):
        pygame.draw.rect(screen, GREY_3, self.page_rect, border_radius=10)
        text = TEXT_FONT.render(f"PAGE: {page}", 1, BLACK)
        screen.blit(text, (self.page_rect.x + (self.page_rect.width - text.get_width())//2, self.page_rect.y + text.get_height()))

        money_spent = 0
        dps_increase = 0

        for spell in self.spells:
            action = spell.draw(money)
            if action:
                spell.LevelUp()
                money_spent = action
                dps_increase = spell.dps

        return(money_spent, dps_increase)

class Spell():

    width, height = int(Page.width*0.9), int(Page.height*0.18)
    button_width, button_height = int(width*.35), int(height*.7)

    def __init__(self, x, y, name='', dps=0, cost=0, dps_scale=1.05, cost_scale=1.01):
        self.block_rect = pygame.Rect(x, y, Spell.width, Spell.height)
        self.button_rect = pygame.Rect(x + Spell.button_width//10, y + (Spell.height-Spell.button_height)//2, Spell.button_width, Spell.button_height)

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

class Game():

    def __init__(self):
        self.damagePerSecond = 0
        self.damagePerClick = 400
        self.money = 0.0
        self.level = 0
        self.reward = 1_000

        self.health = 5_000
        self.monster = Monster('Bob',self.health)


        self.test = Book()


    def NextMonster(self):
        if self.monster.health <= 0:
            self.health = int(self.health * 1.2)
            self.monster = Monster('Bob',self.health)
            self.money += self.reward
            self.reward = int(self.reward * 1.01)
            self.level += 1           

    def IncreaseDPS(self, amount):
        self.damagePerSecond += amount

    def IncreaseDPC(self, amount):
        self.damagePerClick += amount

    def DamageMonsterPerSecond(self):
        self.monster.Damage(self.damagePerSecond/FPS)

    def DamageMonsterClick(self):
        self.monster.Damage(self.damagePerClick)


    def draw(self):
        screen.fill(WHITE)

        dps_text = TEXT_FONT.render(f"DPS: {self.damagePerSecond:.0f}", 1, BLACK)
        dpc_text = TEXT_FONT.render(f"DPC: {self.damagePerClick:.0f}", 1, BLACK)
        gold_text = TEXT_FONT.render(f"GOLD: {self.money:.0f}", 1, BLACK)
        
        screen.blit(dps_text, (Book.x_pos, Book.y_pos + Book.height + dps_text.get_height()))
        screen.blit(dpc_text, (Book.x_pos, Book.y_pos + Book.height + dps_text.get_height() + dpc_text.get_height()))
        screen.blit(gold_text, (Book.x_pos, Book.y_pos + Book.height + dps_text.get_height() + dpc_text.get_height() + gold_text.get_height()))

        level_text = TEXT_FONT.render(f"Level: {self.level}", 1, BLACK)
        screen.blit(level_text, (int(WIDTH*0.75) - level_text.get_width()//2, 2*level_text.get_height()))
       

        action = self.monster.draw()
        if action == ButtonAction.Clicked:
            self.DamageMonsterClick()       


        self.DamageMonsterPerSecond()

        self.NextMonster()

        money_spent, dps_increase = self.test.draw(self.money)
        self.money -= money_spent
        self.IncreaseDPS(dps_increase)

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