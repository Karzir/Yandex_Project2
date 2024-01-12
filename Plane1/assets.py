import os
import pygame

sprites = {}
audios = {}


def load_sprites():  # Загрузка спрайтов
    path = os.path.join("assets", "sprites")
    for file in os.listdir(path):
        sprites[file.split('.')[0]] = pygame.image.load(os.path.join(path, file))


def get_sprite(name):  # Метод для обращения к спрайту
    return sprites[name]


def load_audios():
    path = os.path.join("assets", "audios")
    for file in os.listdir(path):
        audios[''.join(file[::-1].split('.', 1)[::-1][:-1])[::-1]] = pygame.mixer.Sound(os.path.join(path, file))


def play_audio(name, count=0, volume=1):
    audios[name].set_volume(volume)
    audios[name].play(count)
