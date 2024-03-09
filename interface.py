# Makeathon 2024 project
# Utku, Sid, Andrew, Ethan

import pygame
import sys

pygame.init()

width, height = 460, 320
padding = 18
safe_width = width - 2 * padding
safe_height = height - 2 * padding
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Makeathon 2024")

text_area = (padding, padding, safe_width, safe_height * 0.5)

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

font = pygame.font.SysFont(None, 36)

buttons = [1,2,3,4,5]
clicked = [False for button in buttons]
button_radius = 30
button_spacing = 20
button_y = padding + safe_height * 0.5

def render_text_with_wrap(text, font, color, rect, surface):
    words = text.split(' ')
    wrapped_lines = []
    line = ''
    for word in words:
        test_line = line + word + ' '
        if font.size(test_line)[0] <= rect.width:
            line = test_line
        else:
            wrapped_lines.append(line)
            line = word + ' '
    wrapped_lines.append(line)

    y = rect.top
    for wrapped_line in wrapped_lines:
        rendered_line = font.render(wrapped_line, True, color)
        surface.blit(rendered_line, (rect.left, y))
        y += font.size(wrapped_line)[1]

def draw_buttons(buttons):
    button_positions = []
    total_button_width = len(buttons) * (button_radius * 2 + button_spacing) - button_spacing
    x_start = (width - total_button_width) / 2 + button_radius
    for i, button in enumerate(buttons):
        x = x_start + (button_radius * 2 + button_spacing) * i
        pygame.draw.circle(screen, GREEN if clicked[i] else BLACK, (x, button_y), button_radius)
        text = font.render(str(button), True, WHITE)
        text_rect = text.get_rect(center=(x, button_y))
        screen.blit(text, text_rect)
        button_positions.append((x, button_y))
    return button_positions

def check_click_button(button_positions, mouse_pos, mouse_down):
    for i, pos in enumerate(button_positions):
        x, y = pos
        distance = ((mouse_pos[0] - x)**2 + (mouse_pos[1] - y)**2) ** 0.5
        if distance <= button_radius:
            if mouse_down:
                clicked[i] = True
            else:
                clicked[i] = False

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            check_click_button(button_positions, mouse_pos, True)
        elif event.type == pygame.MOUSEBUTTONUP:
            mouse_pos = pygame.mouse.get_pos()
            check_click_button(button_positions, mouse_pos, False)

    screen.fill(WHITE)

    text = "On a scale of 1-5, how are you feeling today? Use the buttons to select a value."
    render_text_with_wrap(text, font, BLACK, pygame.Rect(text_area), screen)

    button_positions = draw_buttons(buttons)

    pygame.display.flip()

pygame.quit()
sys.exit()
