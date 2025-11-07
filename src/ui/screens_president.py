"""
Game screens - This Is the President style
Darker UI, presidential theme
"""
import pygame
from src.core.constants import *
from src.ui.components import Button, TextBox, ProgressBar


class MainMenu:
    """Main menu screen - Presidential style"""

    def __init__(self, game):
        self.game = game
        self.buttons = {
            'new_game': Button(450, 350, 300, 60, "Start Presidency", DARK_RED),
            'quit': Button(450, 450, 300, 60, "Quit", DARK_GRAY)
        }

    def handle_event(self, event):
        """Handle input events"""
        if self.buttons['new_game'].handle_event(event):
            self.game.start_new_game()
        elif self.buttons['quit'].handle_event(event):
            self.game.running = False

    def render(self, screen):
        """Draw the menu"""
        # Title
        try:
            title_font = pygame.font.Font(None, 72)
            subtitle_font = pygame.font.Font(None, 36)
        except:
            title_font = pygame.font.SysFont('arial', 72, bold=True)
            subtitle_font = pygame.font.SysFont('arial', 36)

        title = title_font.render("THIS IS THE", True, WHITE)
        title2 = title_font.render("PRESIDENT", True, CRIMSON)
        subtitle = subtitle_font.render("Do whatever it takes to survive", True, LIGHT_GRAY)

        screen.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, 120))
        screen.blit(title2, (SCREEN_WIDTH // 2 - title2.get_width() // 2, 190))
        screen.blit(subtitle, (SCREEN_WIDTH // 2 - subtitle.get_width() // 2, 270))

        for button in self.buttons.values():
            button.render(screen)


class GameScreen:
    """Main game screen - Presidential dashboard"""

    def __init__(self, game):
        self.game = game

        # Action buttons
        self.action_buttons = {
            'bribe': Button(50, 550, 180, 50, "Bribe Congress", CRIMSON),
            'propaganda': Button(250, 550, 180, 50, "Propaganda", DARK_RED),
            'cover_up': Button(450, 550, 180, 50, "Cover-Up", DARK_GRAY),
            'speech': Button(650, 550, 180, 50, "Public Speech", BLUE),
            'exec_order': Button(850, 550, 180, 50, "Exec. Order", PURPLE),
            'next_week': Button(950, 700, 200, 60, "Next Week", DARK_GREEN)
        }

        # Stat bars
        self.approval_bar = ProgressBar(50, 120, 300, 25)
        self.influence_bar = ProgressBar(50, 180, 300, 25)
        self.impeachment_bar = ProgressBar(50, 240, 300, 25)
        self.amendment_bar = ProgressBar(50, 300, 300, 25)

    def handle_event(self, event):
        """Handle input events"""
        if self.action_buttons['bribe'].handle_event(event):
            self.game.perform_action('bribe_congress')
        elif self.action_buttons['propaganda'].handle_event(event):
            self.game.perform_action('propaganda')
        elif self.action_buttons['cover_up'].handle_event(event):
            self.game.perform_action('cover_up')
        elif self.action_buttons['speech'].handle_event(event):
            self.game.perform_action('public_speech')
        elif self.action_buttons['exec_order'].handle_event(event):
            self.game.perform_action('executive_order')
        elif self.action_buttons['next_week'].handle_event(event):
            self.game.next_week()

    def render(self, screen):
        """Draw the game screen"""
        pres = self.game.president

        try:
            title_font = pygame.font.Font(None, 42)
            label_font = pygame.font.Font(None, 24)
            small_font = pygame.font.Font(None, 20)
        except:
            title_font = pygame.font.SysFont('arial', 42, bold=True)
            label_font = pygame.font.SysFont('arial', 24)
            small_font = pygame.font.SysFont('arial', 20)

        # Title
        title = title_font.render(f"{pres.name}", True, WHITE)
        screen.blit(title, (50, 30))

        # Date
        date_text = label_font.render(f"Year {self.game.year}, Week {self.game.week}", True, LIGHT_GRAY)
        screen.blit(date_text, (50, 75))

        weeks_text = small_font.render(f"{pres.weeks_remaining} weeks until end of term", True, YELLOW)
        screen.blit(weeks_text, (250, 80))

        # Stats
        y = 100

        # Approval
        approval_label = label_font.render(f"Approval Rating: {pres.approval_rating:.1f}%", True, WHITE)
        screen.blit(approval_label, (50, y))
        y += 20
        approval_color = GREEN if pres.approval_rating > 50 else YELLOW if pres.approval_rating > 30 else RED
        self.approval_bar.set_value(pres.approval_rating, approval_color)
        self.approval_bar.render(screen)
        y += 40

        # Influence
        influence_label = label_font.render(f"Political Influence: {pres.influence}/100", True, WHITE)
        screen.blit(influence_label, (50, y))
        y += 20
        self.influence_bar.set_value(pres.influence, PURPLE)
        self.influence_bar.render(screen)
        y += 40

        # Impeachment Risk
        impeach_label = label_font.render(f"Impeachment Risk: {pres.impeachment_risk}%", True,
                                          RED if pres.impeachment_risk > 50 else YELLOW if pres.impeachment_risk > 25 else WHITE)
        screen.blit(impeach_label, (50, y))
        y += 20
        impeach_color = RED if pres.impeachment_risk > 50 else ORANGE if pres.impeachment_risk > 25 else YELLOW
        self.impeachment_bar.set_value(pres.impeachment_risk, impeach_color)
        self.impeachment_bar.render(screen)
        y += 40

        # Amendment Progress
        amend_label = label_font.render(f"Amendment Votes: {pres.amendment_votes}/{AMENDMENT_REQUIRED_VOTES}", True, WHITE)
        screen.blit(amend_label, (50, y))
        y += 20
        self.amendment_bar.set_value(pres.amendment_votes, GOLD)
        self.amendment_bar.render(screen)

        # Money
        money_color = GREEN if pres.money > 200000 else YELLOW if pres.money > 50000 else RED
        money_label = label_font.render(f"Slush Fund: ${pres.money:,}", True, money_color)
        screen.blit(money_label, (50, 350))

        # Scandals & Investigations
        scandal_text = label_font.render(f"Active Scandals: {len(pres.active_scandals)}", True, RED if pres.active_scandals else WHITE)
        screen.blit(scandal_text, (50, 390))

        invest_text = label_font.render(f"Investigations: {len(pres.investigations)}", True, CRIMSON if pres.investigations else WHITE)
        screen.blit(invest_text, (50, 420))

        # Factions status
        factions_title = title_font.render("Factions", True, WHITE)
        screen.blit(factions_title, (700, 100))

        fy = 150
        for faction_id, faction in self.game.factions.items():
            faction_info = FACTIONS[faction_id]
            color = faction_info['color']

            faction_text = label_font.render(f"{faction.name}: {faction.loyalty}%", True, color)
            screen.blit(faction_text, (700, fy))

            # Mini loyalty bar
            faction_bar = ProgressBar(700, fy + 25, 200, 15)
            faction_bar.set_value(faction.loyalty, color)
            faction_bar.render(screen)

            fy += 60

        # Action buttons
        for button in self.action_buttons.values():
            button.render(screen)

        # Action costs info
        info_texts = [
            "Bribe Congress: $100K, -10 influence → +votes",
            "Propaganda: $50K, +5 influence → +approval",
            "Cover-Up: $75K, -5 influence → remove scandal",
            "Public Speech: $10K → +2-5% approval",
            "Executive Order: 15 influence → mixed results"
        ]

        iy = 620
        for text in info_texts:
            rendered = small_font.render(text, True, LIGHT_GRAY)
            screen.blit(rendered, (50, iy))
            iy += 20

        # Goal reminder
        goal_font = pygame.font.Font(None, 28)
        goal_text = goal_font.render("GOAL: Pass immunity amendment OR survive 4 years", True, GOLD)
        screen.blit(goal_text, (50, 470))


class EventScreen:
    """Event screen - This Is the President style"""

    def __init__(self, game):
        self.game = game
        self.choice_buttons = []

    def handle_event(self, event):
        """Handle input events"""
        for i, button in enumerate(self.choice_buttons):
            if button.handle_event(event):
                self.game.handle_event_choice(i)

    def render(self, screen):
        """Draw event screen"""
        if not self.game.current_event:
            return

        current_event = self.game.current_event

        try:
            title_font = pygame.font.Font(None, 52)
            desc_font = pygame.font.Font(None, 22)
            small_font = pygame.font.Font(None, 18)
        except:
            title_font = pygame.font.SysFont('arial', 52, bold=True)
            desc_font = pygame.font.SysFont('arial', 22)
            small_font = pygame.font.SysFont('arial', 18)

        # Title with threat indicator
        title_color = RED if current_event.threat_level >= 4 else ORANGE if current_event.threat_level >= 2 else YELLOW
        title = title_font.render(current_event.title, True, title_color)
        screen.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, 80))

        # Threat level
        threat_text = f"Threat Level: {'█' * current_event.threat_level}{'░' * (5 - current_event.threat_level)}"
        threat_surf = small_font.render(threat_text, True, title_color)
        screen.blit(threat_surf, (SCREEN_WIDTH // 2 - threat_surf.get_width() // 2, 140))

        # Description box
        desc_box = TextBox(150, 180, 900, 150, DARK_GRAY)
        desc_box.set_text(current_event.description, WHITE)
        desc_box.render(screen)

        # Choices
        self.choice_buttons = []
        y_offset = 360

        for i, choice in enumerate(current_event.choices):
            button = Button(200, y_offset, 800, 65, choice.text, CRIMSON if i == 0 else DARK_RED)
            self.choice_buttons.append(button)
            button.render(screen)

            # Effects preview
            effects_parts = []
            for effect, value in choice.effects.items():
                color_code = "+" if value > 0 else ""
                effects_parts.append(f"{effect}: {color_code}{value}")

            effects_text = " | ".join(effects_parts)
            effects_surf = small_font.render(effects_text, True, LIGHT_GRAY)
            screen.blit(effects_surf, (220, y_offset + 70))

            y_offset += 110


class EndScreen:
    """Game over / victory screen"""

    def __init__(self, game):
        self.game = game
        self.menu_button = Button(450, 650, 300, 60, "Return to Menu", DARK_GRAY)

    def handle_event(self, event):
        """Handle input events"""
        if self.menu_button.handle_event(event):
            self.game.current_screen = 'menu'
            self.game.game_over = False

    def render(self, screen):
        """Draw end screen"""
        try:
            title_font = pygame.font.Font(None, 72)
            text_font = pygame.font.Font(None, 32)
        except:
            title_font = pygame.font.SysFont('arial', 72, bold=True)
            text_font = pygame.font.SysFont('arial', 32)

        if self.game.victory:
            if self.game.president.amendment_passed:
                title_text = "IMMUNITY SECURED"
                subtitle = "You passed the amendment. You're untouchable now."
                color = GOLD
            else:
                title_text = "TERM COMPLETED"
                subtitle = "You survived 4 years in office. Barely."
                color = GREEN
        else:
            if self.game.president.is_impeached:
                title_text = "IMPEACHED"
                subtitle = "Congress voted you out. Prison awaits."
                color = CRIMSON
            else:
                title_text = "GAME OVER"
                subtitle = "Your presidency has ended in disgrace."
                color = RED

        title = title_font.render(title_text, True, color)
        screen.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, 200))

        subtitle_surf = text_font.render(subtitle, True, WHITE)
        screen.blit(subtitle_surf, (SCREEN_WIDTH // 2 - subtitle_surf.get_width() // 2, 300))

        # Stats summary
        stats = [
            f"Final Approval: {self.game.president.approval_rating:.1f}%",
            f"Money Remaining: ${self.game.president.money:,}",
            f"Amendment Votes: {self.game.president.amendment_votes}/{AMENDMENT_REQUIRED_VOTES}",
            f"Years Served: {self.game.year}",
            f"Scandals: {len(self.game.president.active_scandals)}"
        ]

        y = 400
        for stat in stats:
            stat_surf = text_font.render(stat, True, LIGHT_GRAY)
            screen.blit(stat_surf, (SCREEN_WIDTH // 2 - stat_surf.get_width() // 2, y))
            y += 40

        self.menu_button.render(screen)
