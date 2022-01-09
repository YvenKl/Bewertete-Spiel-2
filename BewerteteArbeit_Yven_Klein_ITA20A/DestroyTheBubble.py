import pygame
from pygame.version import PygameVersion
import os
from random import randint
from pygame.constants import (QUIT, K_ESCAPE, KEYDOWN, KEYUP, MOUSEBUTTONDOWN)
import sys
from time import sleep

class Settings:
    window_width = 700
    window_height = 700
    path_file = os.path.dirname(os.path.abspath(__file__))
    path_image = os.path.join(path_file, "images")
    sound_path = os.path.join(path_file, "sounds")
    fps = 60
    delay_indicator = 60
    delay = 0
    caption = "DestroyTheBubblesUltimateEdition"
    level_indicator = 0
    point = 0
    path = {}
    lvl = 0
    growth = randint(1, 4)
    mouse_indicator = 0
    mouse_image = "Needle1.png"
    mouse_image_target = "Needle2.png"
    nof_bubbles = 10
    alive = True
    mouse_pos = "x,y"

class Background(object):
    def __init__(self, filename="background.jpg") -> None:
        super().__init__()
        self.image = pygame.image.load(os.path.join(Settings.path_image, filename)).convert()
        self.image = pygame.transform.scale(self.image, (Settings.window_width, Settings.window_height))

    def draw(self, screen):
        screen.blit(self.image, (0, 0))
        main_font = pygame.font.SysFont("comicsans", 50)  # Schriftart von der Font
        point_label = main_font.render(f"Points: {Settings.point}", 1, (255, 0, 0)) #Farben der Fonts
        level_label = main_font.render(f"Difficulty: {Settings.lvl}", 1, (255, 0, 0))
        screen.blit(level_label, (10, Settings.window_height - point_label.get_height() - 10))  # Koordinaten der Fonts
        screen.blit(point_label, (Settings.window_width - point_label.get_width() - 10, 10))

class Bubble(pygame.sprite.Sprite):
    def __init__(self) -> None:
        super().__init__()
        fullfilename = os.path.join(Settings.path_image, "Bubble.png")
        self.image_orig = pygame.image.load(fullfilename).convert_alpha()
        self.image = pygame.transform.scale(self.image_orig, (10, 10))
        self.rect = self.image.get_rect()
        self.scale = {'width': self.rect.width, 'height': self.rect.height}
        self.rect.left = randint(10, Settings.window_width-20)
        self.rect.top = randint(10, Settings.window_height-20)
        self.worth = 1


    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def update(self):
        c = self.rect.center                                                            #Der alte Zentralpunkt einer Blase wird hiermit abgespeichert und dann wieder genutzt um die Blase wachsen/platzieren zu lassen
        self.image = pygame.transform.scale(self.image_orig, (self.get_scale()))
        self.rect = self.image.get_rect()
        self.rect.center = c
        self.growth()
        if self.rect.bottom > Settings.window_height:
            self.kill()
            pygame.mixer.music.load(os.path.join(Settings.sound_path, "die.mp3"))         #Wenn die Blasen den Rand des Screens berühren platzen sie
            pygame.mixer.music.play(1)

        elif self.rect.right > Settings.window_width:
            self.kill()
            pygame.mixer.music.load(os.path.join(Settings.sound_path, "die.mp3"))
            pygame.mixer.music.play(1)

        elif self.rect.left < 0:
            self.kill()
            pygame.mixer.music.load(os.path.join(Settings.sound_path, "die.mp3"))
            pygame.mixer.music.play(1)

        elif self.rect.top < 0:
            self.kill()
            pygame.mixer.music.load(os.path.join(Settings.sound_path, "die.mp3"))
            pygame.mixer.music.play(1)


    def scale_up(self):                             #Hiermit wächst die Blase(1-4 pro Sekunde/Zeiteinheit(Das Worth funktionier nicht, das war ein versuch um den Wert einer Blase zu erhöhen).
        self.scale['width'] += Settings.growth
        self.scale['height'] += Settings.growth
        self.worth += 1

    def get_scale(self):
        return (self.scale['width'], self.scale['height'])

    def set_center(self, center):
        self.rect.centerx, self.rect.centery = center

    def growth(self):
        if Settings.delay == 0:
            self.scale_up()

class Needle(pygame.sprite.Sprite):
    def __init__(self, filename=Settings.mouse_image) -> None:
        super().__init__()
        self.image_original = pygame.image.load(os.path.join(Settings.path_image, filename)).convert_alpha()
        self.image = pygame.transform.scale(self.image_original, (40, 40))
        self.rect = self.image.get_rect()
        self.rect.topleft = pygame.mouse.get_pos()

    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def update(self):
        self.rect.center = pygame.mouse.get_pos()

class Needle_target(pygame.sprite.Sprite):                  #Die Nadel(Maussprite) wird zweimal erstellt um damit eine Kleine Veränderung/Animation hinzuzufügen
    def __init__(self, filename=Settings.mouse_image_target) -> None:
        super().__init__()
        self.image_original = pygame.image.load(os.path.join(Settings.path_image, filename)).convert_alpha()
        self.image = pygame.transform.scale(self.image_original, (40, 40))
        self.rect = self.image.get_rect()
        self.rect.topleft = pygame.mouse.get_pos()

    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def update(self):
        self.rect.center = pygame.mouse.get_pos()

class Game(object):
    def __init__(self) -> None:
        super().__init__()
        # Position Fenster
        os.environ['SDL_VIDEO_WINDOW_POS'] = "50,30"

        # PyGame-Vorbereitungen
        pygame.init()
        pygame.display.set_caption(Settings.caption)
        self.screen = pygame.display.set_mode((Settings.window_width, Settings.window_height))
        self.clock = pygame.time.Clock()
        self.bubble = pygame.sprite.Group()
        self.needle = pygame.sprite.Group()
        self.needle_target = pygame.sprite.Group()
        self.Bubble = Bubble()
        self.Needle = Needle()
        self.Needle_target = Needle_target()
        self.pause_screen_main = pygame.image.load(os.path.join(Settings.path_image, "greyscreen.png")).convert_alpha()
        self.pause_screen = pygame.transform.scale(self.pause_screen_main,(Settings.window_width, Settings.window_height))
        self.gameover_screen_main = pygame.image.load(os.path.join(Settings.path_image, "greyscreen.png")).convert_alpha()
        self.gameover_screen = pygame.transform.scale(self.pause_screen_main,(Settings.window_width, Settings.window_height))
        self.running = False

    def run(self):
        self.start()
        # Hauptprogrammschleife
        self.running = True
        while self.running:
            self.clock.tick(Settings.fps)
            self.watch_for_events()
            self.update()
            self.draw()

        pygame.quit()

    def draw(self):
        self.background.draw(self.screen)
        self.bubble.draw(self.screen)
        self.needle.draw(self.screen)
        self.needle_target.draw(self.screen)
        pygame.display.flip()

    def get_pos(self):
        Settings.mouse_pos = pygame.mouse.get_pos

    def time_difficulty(self):                                  #Hier wird die Schwierigkeit angehoben indem die Zeiteinheit verkleinert wird und die Wachstumsgeschwindigkeit anzuheben
        if Settings.point == 10 and Settings.lvl == 0:
            Settings.delay_indicator = 50
            Settings.lvl += 1
        elif Settings.point == 20 and Settings.lvl == 1:
            Settings.delay_indicator = 40
            Settings.lvl += 1
        elif Settings.point == 30 and Settings.lvl == 2:
            Settings.delay_indicator = 30
            Settings.growth = randint(1, 6)
            Settings.lvl += 1

    def spawning_of_bubbles(self):
        if len(self.bubble.sprites()) < Settings.nof_bubbles and Settings.delay == 0:           #Blasen werden mit einem Sound random gespawnt (max.10 Blasen)
            self.bubble.add(Bubble())
            pygame.mixer.music.load(os.path.join(Settings.sound_path, "Spawn.wav"))
            pygame.mixer.music.play(1)

    def time(self):                                           #Hier ist die Zeit angeben hiermit läuft alles ab.
        if Settings.delay == 0:
            Settings.delay = Settings.delay_indicator

        else:
            Settings.delay -= 1

    def pop_bubble(self):
        if pygame.sprite.groupcollide(self.needle or self.needle_target, self.bubble, False, True):             #Blasen werden geplatzt und ein Punkt wird hinzugefügt
            Settings.point += self.Bubble.worth
            pygame.mixer.music.load(os.path.join(Settings.sound_path, "Pop.wav"))
            pygame.mixer.music.play(1)

    def pause_game(self):                                   #Mit Spacebar pausiert man das Game und entpausiert es wieder
        paused = True
        while paused:
            print("Paused")
            self.draw_pause_screen()
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        print("Unpaused")
                        paused = False

    def draw_pause_screen(self):
        self.screen.blit(self.pause_screen, (0, 0))
        pygame.display.flip()

    def difficulty_reset(self):                                #Wenn man stirbt wird hiermit die Schwierigkeit zurrückgesetzt
        Settings.delay_indicator = 60
        Settings.lvl = 0

    def gameover(self):                                         #Hiermit stribt man
        if Settings.alive == False:
            for Bubble in self.bubble.sprites():
                Bubble.remove(self.bubble)
            Settings.point = 0
            self.difficulty_reset()
            Settings.alive = True
            self.gameover_execute()

    def gameover_execute(self):
        pausedg = True
        while pausedg:
            self.draw_gameover_screen()
            print("Dead")
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        pausedg = False
                        print("Alive")

    def draw_gameover_screen(self):
        self.screen.blit(self.gameover_screen, (0, 0))
        pygame.display.flip()

    def bubble_collide(self):                       #Mithilfe von enumerate werden Blasen verschieden gekennzeichnet und wenn 2 verschiedene Blasen kollidieren hat man verloren
        bubbles = self.bubble.sprites()
        for i, bubble1 in enumerate(bubbles):
            for bubble2 in bubbles[i + 1:]:
                if pygame.sprite.collide_rect(bubble1, bubble2):
                    pygame.mixer.music.load(os.path.join(Settings.sound_path, "die.mp3"))
                    pygame.mixer.music.play(1)
                    Settings.alive = False

    def mouse_target_change(self):                      #Hiermit wird die veränderung der Maus und animation angefügt
        if pygame.sprite.groupcollide(self.needle, self.bubble, False, False):
            for Needle in self.needle.sprites():
                Needle.remove(self.needle)
                self.needle_target.add(self.Needle_target)

        else:
            for Needle_target in self.needle_target.sprites():
                Needle_target.remove(self.needle_target)
            self.needle.add(self.Needle)

    def update(self):
        self.bubble.update()
        self.spawning_of_bubbles()
        self.needle.update()
        self.needle_target.update()
        self.time_difficulty()
        self.time()
        self.gameover()
        self.mouse_target_change()
        self.bubble_collide()
        self.get_pos()

    def watch_for_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                elif event.key == pygame.K_SPACE:
                    self.pause_game()
            elif event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    self.pop_bubble()

    def start(self):
        pygame.mixer.music.set_volume(0.2)
        pygame.mouse.set_visible(False)
        self.needle.add(Needle())
        self.background = Background()

if __name__ == "__main__":
    game = Game()
    game.run()

