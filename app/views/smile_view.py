# Makeathon 2024 project
# Utku, Sid, Andrew, Ethan

import pygame
import lib.color as color
import lib.gui as gui


class SmileView(gui.View):
    def __init__(self, radius):
        super().__init__()
        self.radius = radius
        self.offset = 0
        self.direction = 3
        self.big_eye = False

    def set_big_eye(self, big_eye):
        self.big_eye = big_eye

    def render(self, x, y, width, height, screen):
        radius = min(self.radius, min(width / 2, height / 2))

        x += self.offset
        self.offset += self.direction
        min_x = 0
        max_x = width - 2 * radius
        if self.offset > max_x:
            self.offset = max_x
            self.direction *= -1
        elif self.offset < min_x:
            self.offset = min_x
            self.direction *= -1

        center_x = x + radius
        center_y = y + radius

        pygame.draw.circle(screen, color.YELLOW, (center_x, center_y), radius)  # Head

        eye_radius = radius / 10
        if self.big_eye:
            eye_radius *= 1.5
        eye_offset_x = eye_radius * 3
        eye_offset_y = eye_radius * 2
        pygame.draw.circle(
            screen,
            color.BLACK,
            (center_x - eye_offset_x, center_y - eye_offset_y),
            eye_radius,
        )
        pygame.draw.circle(
            screen,
            color.BLACK,
            (center_x + eye_offset_x, center_y - eye_offset_y),
            eye_radius,
        )

        smile_rect = pygame.Rect(
            center_x - radius * 0.5, center_y, radius, radius * 0.4
        )
        pygame.draw.arc(screen, color.BLACK, smile_rect, 0.1, 0, 2)

        return width, 2 * radius
