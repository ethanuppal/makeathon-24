import pygame

class AudioPlayer:
    def __init__(self, source):
        self.source = source

    def play(self):
        pygame.mixer.Sound(self.source).play()

    def stop(self):
        pygame.mixer.stop()