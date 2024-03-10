# Makeathon 2024 project - BASSMAXX
# Sidharth Rao, Utku Melemetci, Ethan Uppal, Andrew Louis

import os

os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "hide"
import pygame
import sys
import lib.color as color
import lib.gui as gui
import lib.timer as timer
from views.smile_view import SmileView
import config
import firebase_admin
from firebase_admin import credentials, firestore
from google.cloud.firestore import Increment

if config.on_rpi:
    from servo.serial_connect import signal


class App:
    def __init__(self):
        pygame.init()
        self.screen = None
        if config.on_rpi:
            self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        else:
            self.screen = pygame.display.set_mode((480, 320))
        pygame.display.set_caption("Makeathon 2024")
        self.width = self.screen.get_width()
        self.height = self.screen.get_height()
        self.buffer_surface = pygame.Surface((self.width, self.height))
        self.timing_queue = timer.TimedQueue(2)
        self.clock = pygame.time.Clock()

        cred = credentials.Certificate("secret/serviceAccountKey.json")
        firebase_admin.initialize_app(cred)
        self.db = firestore.client()

    def setup(self):
        self.smiley = SmileView(radius=30)
        self.status_text_area = gui.TextArea("", config.get_font(), color.BLACK)
        self.buttons = list(
            map(
                lambda x: gui.Button(
                    "happiness",
                    x,
                    30,
                    config.get_font(),
                    lambda name, value: self.on_button(name, value),
                ),
                range(1, 6),
            )
        )

        self.main_view = gui.SafeView(
            subview=gui.VStack(
                [
                    gui.TextArea(
                        "On a scale of 1-5, how are you feeling today?",
                        config.get_font(),
                        color.BLACK,
                    ),
                    gui.VSpacer(),
                    gui.HStack(self.buttons).with_dynamic_centering(),
                    gui.VSpacer(),
                    self.status_text_area,
                    self.smiley,
                ]
            )
        )

    def run(self):
        running = True
        try:
            while running:
                # drawing
                self.buffer_surface.fill(color.WHITE)
                self.main_view.render(
                    0, 0, self.width, self.height, self.buffer_surface
                )

                # events
                self.timing_queue.handle_requests()
                for event in pygame.event.get():
                    if event.type == pygame.QUIT or event.type == pygame.KEYDOWN:
                        running = False
                    elif (
                        event.type == pygame.MOUSEBUTTONDOWN
                        or event.type == pygame.MOUSEBUTTONUP
                    ):
                        if config.invert_display_vertically:
                            event.pos = (
                                self.width - event.pos[0],
                                self.height - event.pos[1],
                            )
                        self.main_view.on_event(event)

                # pygame loop
                if config.invert_display_vertically:
                    flipped_buffer = pygame.transform.rotate(self.buffer_surface, 180)
                    self.screen.blit(flipped_buffer, (0, 0))
                else:
                    self.screen.blit(self.buffer_surface, (0, 0))
                pygame.display.flip()
                self.clock.tick(config.FPS)
        except KeyboardInterrupt:
            pygame.quit()
            sys.exit()
    
    def firebase_telemetry(self, happiness):
        s = str(happiness)
        doc_ref = self.db.collection('happiness').document('current')
        doc_ref.update({
            s: Increment(1)
        })

    def on_button(self, name, value):
        if config.on_rpi:
            signal()
        if value >= config.happiness_threshold:
            self.status_text_area.set_text("Glad you're feeling well!")
        else:
            self.status_text_area.set_text("Sorry you're not feeling well.")
        self.status_text_area.set_visible(True)
        self.smiley.set_big_eye(True)
        for button in self.buttons:
            button.set_enabled(False)
    
        self.firebase_telemetry(value)

        def callback(timer):
            self.status_text_area.set_visible(False)
            for button in self.buttons:
                button.set_enabled(True)
            self.smiley.set_big_eye(False)

        self.timing_queue.enqueue(callback)
