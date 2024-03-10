# Makeathon 2024 project
# Utku, Sid, Andrew, Ethan

import pygame
import sys

FPS = 60
"""
The frame rate for the app.
"""


def get_font():
    """
    Returns the app's rendering font.
    """
    if get_font.cache == None:
        get_font.cache = pygame.font.SysFont(None, 36)
    return get_font.cache


get_font.cache = None

happiness_levels = 5
"""
The range (`1` to `happiness_levels`) for possible levels of happiness.
"""

happiness_threshold = 3
"""
The threshold greater than or equal to which a happiness level is considered "happy".
"""
