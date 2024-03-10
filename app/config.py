# Makeathon 2024 project - BASSMAXX
# Sidharth Rao, Utku Melemetci, Ethan Uppal, Andrew Louis

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

invert_display_vertically = False
"""
Whether the output should be inverted verbatim in the vertical direction.
"""

on_rpi = True
"""
Whether the app is running on the Raspberry Pi.
"""
if len(sys.argv) >= 2 and sys.argv[1] == "Darwin":
    # since I'm testing it on MacOS
    on_rpi = False
    invert_display_vertically = False
