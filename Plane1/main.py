import pygame
import assets
import conf
import sqlite3

from objects.Pause import Pause
from objects.background import Background
from objects.column import Column
from objects.plane import Plane
from objects.game_start import GameStart
from objects.game_over import GameOver
from objects.score import Score

import sys

pygame.init()
con = sqlite3.connect("score.sqlite")
cur = con.cursor()

pygame.display.set_caption('SwitchPlane')
screen = pygame.display.set_mode((conf.SCREEN_WIDTH, conf.SCREEN_HEIGHT))
clock = pygame.time.Clock()
column_create_event = pygame.USEREVENT
running = True
gameover = False
gamestarted = False
start = True
bom = True


def terminate():
    pygame.quit()
    sys.exit()


assets.load_sprites()
assets.load_audios()
boom = assets.get_sprite("bum")
boom = pygame.transform.scale(boom, (150, 70))
gg = assets.get_sprite('rest')
gg = pygame.transform.scale(gg, (200, 20))
sprites = pygame.sprite.LayeredUpdates()
assets.play_audio('Смешарики - От винта!', volume=0.1)
pause_menu = assets.get_sprite('pause_menu')
pause_menu_ch = False


def create_sprites():
    Background(0, sprites)
    Background(1, sprites)

    return Plane(sprites), GameStart(sprites), Score(sprites)


def paused():
    global gameover, gamestarted, start, pause_menu_ch
    gamestarted = False
    gameover = True
    pygame.time.set_timer(column_create_event, 0)
    start = True
    pause_menu_ch = True


plane, game_start, score = create_sprites()
Pause(sprites)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == column_create_event:
            Column(sprites)
            Pause(sprites)

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and not gamestarted and not gameover:
                if start:
                    pygame.time.set_timer(column_create_event, 1000)
                gamestarted = True
                pause_menu_ch = False
                start = False
                game_start.kill()

            if event.key == pygame.K_r and gameover and not pause_menu_ch:
                cur.execute(f"""INSERT INTO Score VALUES({end_points})""").fetchall()
                bom = True
                gameover = False
                gamestarted = False
                pygame.time.set_timer(column_create_event, 0)
                start = True
                sprites.empty()
                plane, game_start, score = create_sprites()
                Pause(sprites)

            if event.key == pygame.K_ESCAPE and not start and gamestarted:
                paused()

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                x, y = event.pos
                if 745 <= x <= 795 and 8 <= y <= 55 and gamestarted:
                    paused()
                if start:
                    pygame.time.set_timer(column_create_event, 1000)
                if pause_menu_ch:
                    if 250 <= x <= 505 and 210 <= y <= 265:
                        if start:
                            pygame.time.set_timer(column_create_event, 1000)
                        gamestarted = True
                        gameover = False
                        pause_menu_ch = False
                        start = False
                        game_start.kill()
                    if 250 <= x <= 505 and 355 <= y <= 410:
                        print('Начальника,не злися,я патом даделать')
                else:
                    start = False
                    pause_menu_ch = False
                    gamestarted = True
                    game_start.kill()
        if not gameover:
            plane.handle_event(event)

    screen.fill(0)

    sprites.draw(screen)
    if pause_menu_ch:
        im, rct = Pause().check()
        screen.blit(im, rct)
    if gamestarted and not gameover:
        sprites.update()

    if plane.check_collision(sprites):
        gameover = True
        end_points = score.value
        gamestarted = False

        GameOver(sprites)
        x, y = plane.get_coord()
        screen.blit(boom, (x - 20, y - 10))
        screen.blit(gg, (300, 320))
        if bom:
            assets.play_audio('Звук взрыва', volume=0.2)
            bom = False

    for sprite in sprites:
        if type(sprite) is Column and sprite.is_passed():
            score.value += 1
    pygame.display.flip()
    clock.tick(conf.FPS)


con.commit()
con.close()
terminate()

