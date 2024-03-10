# Copyright (C) 2024 Ethan Uppal. All rights reserved.
# GUI library in pygame for Makeathon 2024.

import pygame
import sys
import lib.color as color

PADDING = 8


class View:
    def __init__(self):
        self.subviews = []

    def render(self, x, y, width, height, screen):
        """Renders the view in screen with the given bounds and returns the actual `width, height` of the view as a tuple.
        The `x` and `y` parameters must be adhered to, but `width`, and `height` are subject to the view.
        """
        for subview in self.subviews:
            subview.render(x, y, width, height, screen)
        return width, height

    def on_event(self, event):
        """Dispatches an event to subviews. Should only be overriden on root views."""
        for subview in self.subviews:
            subview.on_event(event)


class Spacer(View):
    def __init__(self, width=0, height=0):
        super().__init__()
        self.width = width
        self.height = height

    def render(self, x, y, width, height, screen):
        return self.width, self.height


def VSpacer():
    return Spacer(height=PADDING)


def HSpacer():
    return Spacer(width=PADDING)


class SafeView(View):
    def __init__(
        self, subview, top=PADDING, left=PADDING, right=PADDING, bottom=PADDING
    ):
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
            screen,
        )
        return swidth + self.left + self.right, sheight + self.top + self.bottom


class VStack(View):
    def __init__(self, subviews):
        super().__init__()
        for i in range(0, len(subviews)):
            self.subviews.append(
                SafeView(
                    subviews[i],
                    left=0,
                    right=0,
                    top=(PADDING if i > 0 else 0),
                    bottom=(PADDING if i < len(subviews) - 1 else 0),
                )
            )

    def render(self, x, y, width, height, screen):
        total_width = 0
        total_height = 0
        for subview in self.subviews:
            swidth, sheight = subview.render(x, y + total_height, width, height, screen)
            total_width = max(total_width, swidth)
            total_height += sheight
        return total_width, total_height


class HStack(View):
    def __init__(self, subviews):
        super().__init__()
        self.dynamic_centering = False
        self.last_width = 0
        for i in range(0, len(subviews)):
            self.subviews.append(
                SafeView(
                    subviews[i],
                    top=0,
                    bottom=0,
                    left=(PADDING if i > 0 else 0),
                    right=(PADDING if i < len(subviews) - 1 else 0),
                )
            )

    def with_dynamic_centering(self):
        self.dynamic_centering = True
        return self

    def render(self, x, y, width, height, screen):
        if self.dynamic_centering:
            x += (width - self.last_width) / 2
        total_width = 0
        total_height = 0
        for subview in self.subviews:
            swidth, sheight = subview.render(x + total_width, y, width, height, screen)
            total_width += swidth
            total_height = max(total_height, sheight)
        self.last_width = total_width
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
        words = self.text.split(" ")
        wrapped_lines = []
        line = ""
        for word in words:
            test_line = line + word + " "
            if self.font.size(test_line)[0] <= width:
                line = test_line
            else:
                wrapped_lines.append(line)
                line = word + " "
        wrapped_lines.append(line)
        old_y = y
        max_width = 0
        for wrapped_line in wrapped_lines:
            rendered_line = self.font.render(wrapped_line, True, self.color)
            max_width = max(max_width, rendered_line.get_width())
            screen.blit(rendered_line, (x, y))
            y += self.font.size(wrapped_line)[1]
        return max_width, y - old_y


class Button(View):
    def __init__(self, name, value, radius, font, callback):
        super().__init__()
        self.name = name
        self.value = value
        self.font = font
        self.callback = callback
        self.clicked = False
        self.enabled = True
        self.radius = 30
        self.last_x = 0
        self.last_y = 0

    def set_enabled(self, enabled):
        self.enabled = enabled

    def render(self, x, y, width, height, screen):
        self.last_x = x
        self.last_y = y
        if self.enabled:
            pygame.draw.circle(
                screen,
                color.GREEN if self.clicked else color.BLACK,
                (x + self.radius, y + self.radius),
                self.radius,
            )
        else:
            pygame.draw.circle(
                screen, color.GRAY, (x + self.radius, y + self.radius), self.radius
            )
        text = self.font.render(str(self.value), True, color.WHITE)
        text_rect = text.get_rect(center=(x + self.radius, y + self.radius))
        screen.blit(text, text_rect)
        return 2 * self.radius, 2 * self.radius

    def on_event(self, event):
        if not self.enabled:
            return
        mouse_pos = event.pos
        distance = (mouse_pos[0] - (self.last_x + self.radius)) ** 2 + (
            mouse_pos[1] - (self.last_y + self.radius)
        ) ** 2
        if distance > self.radius**2:
            return
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.clicked = True
        elif event.type == pygame.MOUSEBUTTONUP:
            if self.clicked:
                self.callback(self.name, self.value)
                self.clicked = False
