# Makeathon 2024 project
# Utku, Sid, Andrew, Ethan

import os

os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "hide"
import pygame
import sys
import lib.color as color
import lib.gui as gui
import lib.timer as timer
import config
from servo.serial_connect import signal

pygame.init()

screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
# screen = pygame.display.set_mode((480, 320)) # for local testing
pygame.display.set_caption("Makeathon 2024")
width = screen.get_width()
height = screen.get_height()
buffer_surface = pygame.Surface((width, height))

timing_queue = timer.TimedQueue(2)

clock = pygame.time.Clock()

# need to declare these in advance for `button_callback`
status_text_area = gui.TextArea("", config.get_font(), color.BLACK)
buttons = []


def button_callback(name, value):
    print(f"{name}={value}")
    sys.stdout.flush()
    signal()
    if value >= config.happiness_threshold:
        status_text_area.set_text("Glad you're feeling well!")
    else:
        status_text_area.set_text("Sorry you're not feeling well.")
    status_text_area.set_visible(True)
    for button in buttons:
        button.set_enabled(False)

    def after_timeout(timer):
        status_text_area.set_visible(False)
        for button in buttons:
            button.set_enabled(True)

    timing_queue.enqueue(after_timeout)


buttons = list(
    map(
        lambda x: gui.Button("happiness", x, 30, config.get_font(), button_callback),
        range(1, 6),
    )
)

main_view = gui.SafeView(
    subview=gui.VStack(
        [
            gui.TextArea(
                "On a scale of 1-5, how are you feeling today? Use the buttons to select a value.",
                config.get_font(),
                color.BLACK,
            ),
            gui.VSpacer(),
            gui.HStack(buttons).with_dynamic_centering(),
            gui.VSpacer(),
            status_text_area,
        ]
    )
)

running = True
try:
    while running:
        # drawing
        buffer_surface.fill(color.WHITE)
        main_view.render(0, 0, width, height, buffer_surface)

        # events
        timing_queue.handle_requests()
        for event in pygame.event.get():
            if event.type == pygame.QUIT or event.type == pygame.KEYDOWN:
                running = False
            elif (
                event.type == pygame.MOUSEBUTTONDOWN
                or event.type == pygame.MOUSEBUTTONUP
            ):
                if config.invert_display_vertically:
                    event.pos = (width - event.pos[0], height - event.pos[1])
                main_view.on_event(event)

        # pygame loop
        if config.invert_display_vertically:
            flipped_buffer = pygame.transform.rotate(buffer_surface, 180)
            screen.blit(flipped_buffer, (0, 0))
        else:
            screen.blit(buffer_surface, (0, 0))
        pygame.display.flip()
        clock.tick(config.FPS)
except KeyboardInterrupt:
    pygame.quit()
    sys.exit()
