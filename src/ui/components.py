"""
UI Components (buttons, text, etc.)
"""
import pygame
from src.core.constants import *


class Button:
    """Clickable button UI component"""

    def __init__(self, x, y, width, height, text, color=BLUE, hover_color=None):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.hover_color = hover_color or self._lighten_color(color)
        self.font = pygame.font.Font(None, 32)
        self.is_hovered = False

    def _lighten_color(self, color):
        """Create a lighter version of a color"""
        return tuple(min(255, c + 40) for c in color)

    def handle_event(self, event):
        """Handle mouse events"""
        if event.type == pygame.MOUSEMOTION:
            self.is_hovered = self.rect.collidepoint(event.pos)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1 and self.is_hovered:
                return True
        return False

    def render(self, screen):
        """Draw the button"""
        color = self.hover_color if self.is_hovered else self.color
        pygame.draw.rect(screen, color, self.rect)
        pygame.draw.rect(screen, WHITE, self.rect, 2)

        text_surf = self.font.render(self.text, True, WHITE)
        text_rect = text_surf.get_rect(center=self.rect.center)
        screen.blit(text_surf, text_rect)


class TextBox:
    """Text display component"""

    def __init__(self, x, y, width, height, bg_color=LIGHT_GRAY):
        self.rect = pygame.Rect(x, y, width, height)
        self.bg_color = bg_color
        self.lines = []
        self.font = pygame.font.Font(None, 24)

    def set_text(self, text, color=BLACK):
        """Set text with word wrapping"""
        self.lines = []
        words = text.split(' ')
        current_line = []

        for word in words:
            test_line = ' '.join(current_line + [word])
            text_surf = self.font.render(test_line, True, color)

            if text_surf.get_width() <= self.rect.width - 20:
                current_line.append(word)
            else:
                if current_line:
                    self.lines.append((' '.join(current_line), color))
                    current_line = [word]
                else:
                    self.lines.append((word, color))

        if current_line:
            self.lines.append((' '.join(current_line), color))

    def render(self, screen):
        """Draw the text box"""
        pygame.draw.rect(screen, self.bg_color, self.rect)
        pygame.draw.rect(screen, BLACK, self.rect, 2)

        y_offset = 10
        for line_text, color in self.lines:
            text_surf = self.font.render(line_text, True, color)
            screen.blit(text_surf, (self.rect.x + 10, self.rect.y + y_offset))
            y_offset += 30

            if y_offset > self.rect.height - 30:
                break


class ProgressBar:
    """Progress/stat bar component"""

    def __init__(self, x, y, width, height, max_value=100):
        self.rect = pygame.Rect(x, y, width, height)
        self.max_value = max_value
        self.value = 0
        self.color = GREEN

    def set_value(self, value, color=None):
        """Set the current value"""
        self.value = max(0, min(self.max_value, value))
        if color:
            self.color = color

    def render(self, screen):
        """Draw the progress bar"""
        # Background
        pygame.draw.rect(screen, DARK_GRAY, self.rect)

        # Fill
        fill_width = int((self.value / self.max_value) * self.rect.width)
        fill_rect = pygame.Rect(self.rect.x, self.rect.y, fill_width, self.rect.height)
        pygame.draw.rect(screen, self.color, fill_rect)

        # Border
        pygame.draw.rect(screen, WHITE, self.rect, 2)
