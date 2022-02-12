import pygame
from config import *
import random

pygame.init()
size = width, height = 1066, 600
screen = pygame.display.set_mode(size)
BORDER = 10


class Player:
    def __init__(self, name, score=0, hod=False):
        self.score = score
        self.name = name
        self.hod = hod
    
    def set_hod(self, glist):
        for i in glist:
            i.hod = False
        self.hod = True
    
    def render(self):
        surf = pygame.Surface((200, 200))
        if self.hod:
            surf.fill(pygame.Color("green"))
        else:
            surf.fill(pygame.Color("grey"))
        
        font = pygame.font.Font(None, 50)
        name = font.render(self.name, True, pygame.Color("White"))
        surf.blit(name, (BORDER, BORDER))
        
        font = pygame.font.Font(None, 100)
        score = font.render(str(self.score), True, pygame.Color("White"))
        surf.blit(score, (BORDER, BORDER + 50))
        
        return surf


class Baraban:
    def __init__(self):
        self.segments = [25, "+", 20, 15, "Б", 10, 5, 45, 40, 35, "А", 30]
        self.in_process_count = 0
        self.ind_seg = 0
        self.score = 25
        self.sound_baraban = pygame.mixer.Sound("data/baraban.mp3")
        self.sector_flag = False
        self.sector = self.segments[self.ind_seg]
        self.sectors_sounds = {"+": pygame.mixer.Sound("data/sector_plyus.mp3"),
                                "Б": pygame.mixer.Sound("data/sector_bankrot.mp3"),
                                "А": pygame.mixer.Sound("data/sector_priz.mp3")}
    
    def start(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    running = False
                if event.type == pygame.QUIT:
                    exit()
        self.in_process_count = random.randint(32, 128)
        self.sound_baraban.play()
    
    def update(self):
        if self.in_process_count:
            self.ind_seg = (self.ind_seg - 1) % len(self.segments)
            if type(self.segments[self.ind_seg]) is int:
                self.score = self.segments[self.ind_seg]
            else:
                self.score = 25
            self.in_process_count -= 1
            self.sector_flag = True
        else:
            if self.sector_flag:
                self.sector = self.segments[self.ind_seg]
                self.sound_baraban.stop()
                if type(self.sector) is str:
                    self.sectors_sounds[self.sector].play()
                self.sector_flag = False
            
    
    def render(self, screen):
        self.update()
    
        x = width // 2 - 75
        y = height // 2 - 75
        
        
        for i in range(-3, 4):
            pygame.draw.rect(screen, pygame.Color("grey"), (x + i * (150 + BORDER), y, 150, 150))
        
        pygame.draw.rect(screen, (255, 255, 255), (x, y, 150, 150))
        
        for i in range(-3, 4):
            font = pygame.font.Font(None, 150)
            text = font.render(str(self.segments[(self.ind_seg + i) % len(self.segments)]), True, (0, 0, 0))
            screen.blit(text, (x + i * (150 + BORDER), y + BORDER))


def start_screen(screen):
    running = True
    
    opend_sound = pygame.mixer.Sound("data/opening.mp3")
    opend_sound.play()
    
    size_klet = 100
    kletochka = pygame.Surface((((width - size_klet) // size_klet) * size_klet,
                                ((height - size_klet) // size_klet) * size_klet))

    font = pygame.font.Font(None, 150)
    text = font.render("ПОЛЕ ЧУДЕС", True, (70, 70, 250))
    font1 = pygame.font.Font(None, 100)
    text1 = font1.render("КАПИТАЛ ШОУ", True, (100, 200, 100))
    font2 = pygame.font.Font(None, 75)
    text2 = font2.render("МАКСИК ПОПОВ ПРЕДСТАВЛЯЕТ", True, (200, 100, 100))
    clock = pygame.time.Clock()
    v = 80
    delta = 0
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            elif event.type == pygame.KEYDOWN:
                running = False
                opend_sound.stop()
        
        kletochka.fill((125, 125, 125))
        for x in range((width - size_klet) // size_klet):
            for y in range((height - size_klet) // size_klet):
                pygame.draw.rect(kletochka, (25, 25, 25), (x * size_klet, y * size_klet, size_klet, size_klet), size_klet // 10)
         
        if delta < 1000:
            delta += v * clock.tick() / 1000
        else:
            kletochka.blit(text1, ((kletochka.get_width() - text1.get_width()) // 2, -100 + (kletochka.get_height() - text1.get_height()) // 2))
        
        
        screen.fill(pygame.Color("Black"))
        w_c = (kletochka.get_width() - text.get_width()) // 2
        h_c = (kletochka.get_height() - text.get_height()) // 2
        kletochka.blit(text, (w_c, int(delta) + 10 + h_c - 1000))
        kletochka.blit(text, (w_c, -int(delta) + 10 + h_c + 1000))
        kletochka.blit(text2, (int(delta) + w_c, 50 + h_c))
        kletochka.blit(text2, (-int(delta) + w_c, 10 + h_c))
        screen.blit(kletochka, ((width - kletochka.get_width()) // 2, (height - kletochka.get_height()) // 2))
        pygame.display.flip()
    text = font2.render("Крутите барабан", True, (200, 100, 100))
    screen.blit(text, ((width - text.get_width()) // 2, 100 + (height - text.get_height()) // 2))
    pygame.display.flip()


def blit_text(surface, text, pos, font, color=pygame.Color('black')):
    words = [word.split(' ') for word in text.splitlines()]  # 2D array where each row is a list of words.
    space = font.size(' ')[0]  # The width of a space.
    max_width, max_height = surface.get_size()
    x, y = pos
    for line in words:
        for word in line:
            word_surface = font.render(word, True, color)
            word_width, word_height = word_surface.get_size()
            if x + word_width >= max_width:
                x = pos[0]  # Reset the x.
                y += word_height  # Start on new row.
            surface.blit(word_surface, (x, y))
            x += word_width + space
        x = pos[0]  # Reset the x.
        y += word_height  # Start on new row.


def sector_anek(screen):
    font = pygame.font.Font(None, 50)
    text = font.render("Вы точно хотите приз?", True, pygame.Color("Blue"), pygame.Color("Black"))
    screen.blit(text, ((width - text.get_width()) // 2, (height - text.get_height()) // 2))
    font = pygame.font.Font(None, 35)
    text = font.render("ENTER - да, ПРОБЕЛ - нет", True, pygame.Color("Blue"), pygame.Color("Black"))
    screen.blit(text, ((width - text.get_width()) // 2, (height - text.get_height()) // 2 + 40))
    pygame.display.flip()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    running = False
                elif event.key == pygame.K_SPACE:
                    return False
    with open("data/aneks.txt") as file:
        aneks = file.read().split("\n\n")
        file.close()
    anek = random.choice(aneks)
    screen.fill(pygame.Color("Black"))
    font = pygame.font.Font(None, 30)
    blit_text(screen, anek, (10, 10), font, pygame.Color("White"))
    pygame.display.flip()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            elif event.type == pygame.KEYDOWN:
                return True


def draw_word(word):
    tile_size = min((width - 2 * BORDER) // len(word), (width - 2 * BORDER) // 6)
    font = pygame.font.Font(None, (tile_size * 3) // 2)
    surf_word = pygame.Surface((len(word) * tile_size, tile_size))
    surf_word.fill((255, 255, 255))
    
    for k, i in enumerate(word):
        pygame.draw.rect(surf_word, (0, 0, 0), (k * tile_size, 0, (k + 1) * tile_size, tile_size), BORDER)
        if i != "*":
            text = font.render(i, True, (0, 0, 0))
            surf_word.blit(text, (tile_size * k + tile_size // 6, BORDER))
        
    return surf_word, tile_size


def draw_choose(choose_word, tile_size, opend_words):
    tile_size = tile_size // 4
    font = pygame.font.Font(None, (tile_size * 3) // 2)
    if choose_word not in opend_words:
        color = (255, 255, 255)
    else:
        color = (255, 100, 100)
    text = font.render(choose_word, True, (0, 0, 0), color)
    
    return text


def closed_word(word, opend_words):
    show_word = ""
    for i in word:
        if i in opend_words:
            show_word += i
        else:
            show_word += "*"
    return show_word


ok_sound = pygame.mixer.Sound("data/letter_correct.mp3")
no_sound = pygame.mixer.Sound("data/letter_wrong.mp3")
winner_sound = pygame.mixer.Sound("data/win.mp3")

word = word.upper().replace("Ё", "Е").replace("Ъ", "Ь")
opend_words = set()
choose_word = ""

start_screen(screen)

player_ind = 0
players = list()
for i in range(players_count):
    players.append(Player(str(i + 1)))
players[player_ind].set_hod(players)

baraban = Baraban()
running = True
clock = pygame.time.Clock()
baraban_flag = True
while running:
    if baraban_flag:
        baraban.start()
        baraban_flag = False
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key != pygame.K_RETURN:
                choose_word = event.unicode.upper()
            else:
                if baraban.sector == "Б":
                    players[player_ind].score = 0
                    player_ind = (player_ind + 1) % len(players)
                    players[player_ind].set_hod(players)
                    baraban_flag = True
                elif baraban.sector == "А":
                    answer = sector_anek(screen)
                    if answer:
                        player_ind = (player_ind + 1) % len(players)
                        players[player_ind].set_hod(players)
                        baraban_flag = True
                elif choose_word.isdigit() and baraban.sector == "+":
                    choose_word = word[int(choose_word) - 1]
                    ok_sound.play()
                    baraban_flag = True
                elif choose_word in word and choose_word not in show_word:
                    if closed_word(word, [*opend_words, choose_word]) == word:
                        winner_sound.play()
                    else:
                        ok_sound.play()
                        players[player_ind].score += baraban.score * word.count(choose_word)
                        baraban_flag = True
                elif choose_word not in word:
                    no_sound.play()
                    player_ind = (player_ind + 1) % len(players)
                    players[player_ind].set_hod(players)
                    baraban_flag = True
                
                opend_words.add(choose_word)
    
    show_word = closed_word(word, opend_words)
    
    surf_word, tile_size = draw_word(show_word)
    surf_choose = draw_choose(choose_word, tile_size, opend_words)
    
    screen.fill((0, 0, 0))
    screen.blit(surf_word, (BORDER, BORDER))
    baraban.render(screen)
    screen.blit(surf_choose, (BORDER, 2 * BORDER + tile_size))
    for k, i in enumerate(players):
        screen.blit(i.render(), (200 * k + BORDER * (k + 1), height - 200 - BORDER))
    
    pygame.display.flip()

