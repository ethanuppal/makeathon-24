# Makeathon 2024 project
# Utku, Sid, Andrew, Ethan

import pygame
import sys

pygame.init()

#screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
screen = pygame.display.set_mode((480, 320))
pygame.display.set_caption("Makeathon 2024")
width = screen.get_width()
height = screen.get_height()

# make sure the GUI looks good
padding = 8
safe_width = width - 2 * padding
safe_height = height - 2 * padding

FPS = 60

class View:
    def __init__(self):
        self.subviews = []
    """
    Renders the view in screen with the given bounds and returns the actual 
    (width, height) of the view.
    """
    def render(self, x, y, width, height, screen):
        for subview in self.subviews:
            subview.render(x, y, width, height, screen)
        return width, height
    def on_event(self, event):
        for subview in self.subviews:
            subview.on_event(event)

class Fill(View):
    def __init__(self, width=0, height=0):
        super().__init__()
        self.width = width
        self.height = height
    def render(self, x, y, width, height, screen):
        return self.width, self.height

class SafeView(View):
    def __init__(self, subview, top=padding, left=padding, right=padding, bottom=padding):
        super().__init__()
        self.subviews = [subview]
        self.top = top
        self.left = left
        self.right = right
        self.bottom = bottom
    def render(self, x, y, width, height, screen):
        swidth, sheight = self.subviews[0].render(
            x + self.left, 
            y + self.top, 
            width - self.left - self.right, 
            height - self.top - self.bottom, 
            screen
        )
        return swidth + self.left + self.right, sheight + self.top + self.bottom

class VStack(View):
    def __init__(self, subviews):
        super().__init__()
        for i in range(0, len(subviews)):
            self.subviews.append(SafeView(subviews[i], left=0, right=0, top=(padding if i > 0 else 0), bottom=(padding if i < len(subviews) - 1 else 0)))
    def render(self, x, y, width, height, screen):
        total_width = 0
        total_height = 0
        for subview in self.subviews:
            swidth, sheight = subview.render(x, y + total_height, width, height, screen)
            total_width += swidth
            total_height += sheight
        return total_width, total_height

class HStack(View):
    def __init__(self, subviews):
        super().__init__()
        for i in range(0, len(subviews)):
            self.subviews.append(SafeView(subviews[i], top=0, bottom=0, left=(padding if i > 0 else 0), right=(padding if i < len(subviews) - 1 else 0)))
    def render(self, x, y, width, height, screen):
        total_width = 0
        total_height = 0
        for subview in self.subviews:
            swidth, sheight = subview.render(x + total_width, y, width, height, screen)
            total_width += swidth
            total_height += sheight
        return total_width, total_height

class TextArea(View):
    def __init__(self, text, font, color):
        super().__init__()
        self.text = text 
        self.font = font
        self.color = color
        self.visible = True
    def set_text(self, text):
        self.text = text
    def set_visible(self, visible):
        self.visible = visible
    def render(self, x, y, width, height, screen):
        if not self.visible:
            return 0, 0
        words = self.text.split(' ')
        wrapped_lines = []
        line = ''
        for word in words:
            test_line = line + word + ' '
            if self.font.size(test_line)[0] <= width:
                line = test_line
            else:
                wrapped_lines.append(line)
                line = word + ' '
        wrapped_lines.append(line)
        old_y = y
        max_width = 0
        for wrapped_line in wrapped_lines:
            rendered_line = self.font.render(wrapped_line, True, self.color)
            max_width = max(max_width, rendered_line.get_width())
            screen.blit(rendered_line, (x, y))
            y += font.size(wrapped_line)[1]
        return max_width, y - old_y

class Button(View):
    def __init__(self, name, value, callback):
        super().__init__()
        self.name = name
        self.value = value
        self.callback = callback
        self.clicked = False
    def on_event(event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.clicked = True
        elif event.type == pygame.MOUSEBUTTONUP:
            if self.clicked:
                callback(name, value)
                self.clicked = False

text_area_top = (padding, padding, safe_width, safe_height * 0.3)
text_area_bottom = (padding, padding + safe_height * 0.7, safe_width, safe_height * 0.3)

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
GRAY = (192, 192, 192)

font = pygame.font.SysFont(None, 36)

buttons = [1, 2, 3, 4, 5]
clicked = [False for button in buttons]
button_radius = 30
button_spacing = 20
button_y = padding + safe_height * 0.5

time_status = 2
happiness_threshold = 3

selected_answer = None
status_message_timer = 0

clock = pygame.time.Clock()

status_text_area = TextArea("", font, BLACK)

main_view = SafeView(subview=VStack([
    TextArea("On a scale of 1-5, how are you feeling today? Use the buttons to select a value.", font, BLACK),
    Fill(height=button_radius * 4),
    status_text_area
]))

def draw_buttons(buttons):
    button_positions = []
    total_button_width = len(buttons) * (button_radius * 2 + button_spacing) - button_spacing
    x_start = (width - total_button_width) / 2 + button_radius
    for i, button in enumerate(buttons):
        x = x_start + (button_radius * 2 + button_spacing) * i
        if selected_answer is None:
            pygame.draw.circle(screen, GREEN if clicked[i] else BLACK, (x, button_y), button_radius)
        else:
            pygame.draw.circle(screen, GRAY, (x, button_y), button_radius)
        text = font.render(str(button), True, WHITE)
        text_rect = text.get_rect(center=(x, button_y))
        screen.blit(text, text_rect)
        button_positions.append((x, button_y))
    return button_positions

def check_click_button(button_positions, mouse_pos, mouse_down):
    global selected_answer
    if selected_answer is None:
        for i, pos in enumerate(button_positions):
            x, y = pos
            distance = ((mouse_pos[0] - x) ** 2 + (mouse_pos[1] - y) ** 2) ** 0.5
            if distance <= button_radius:
                if mouse_down:
                    clicked[i] = True
                else:
                    if clicked[i] is True:
                        selected_answer = buttons[i]
                    clicked[i] = False

def handle_status_message():
    global status_message_timer, selected_answer
    status_message_timer += 1
    if status_message_timer >= time_status * FPS:
        selected_answer = None
        status_message_timer = 0
        status_text_area.set_visible(False)
        for i in range(len(clicked)):
            clicked[i] = False

running = True
while running:
    screen.fill(WHITE)
    button_positions = draw_buttons(buttons)

    if selected_answer is not None:
        if selected_answer >= happiness_threshold:
            status_text_area.set_text("Glad you're feeling well!")
        else:
            status_text_area.set_text("Sorry you're not feeling well.")
        status_text_area.set_visible(True)
        handle_status_message()

    main_view.render(0, 0, width, height, screen)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT or event.type == pygame.KEYDOWN:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            check_click_button(button_positions, mouse_pos, True)
        elif event.type == pygame.MOUSEBUTTONUP:
            mouse_pos = pygame.mouse.get_pos()
            check_click_button(button_positions, mouse_pos, False)
        main_view.on_event(event)

    pygame.display.flip()
    
    clock.tick(FPS)

pygame.quit()
sys.exit()
