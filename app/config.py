# Makeathon 2024 project
# Utku, Sid, Andrew, Ethan

import pygame

FPS = 60
"""
The frame rate for the app.
"""

font = pygame.font.SysFont(None, 36)
"""
The app's rendering font.
"""

happiness_levels = 5
"""
The range (`1` to `happiness_levels`) for possible levels of happiness.
"""

happiness_threshold = 3
"""
The threshold greater than or equal to which a happiness level is considered "happy".
"""
