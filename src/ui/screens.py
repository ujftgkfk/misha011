"""
Game screens (Menu, Game, Election, Event screens)
"""
import pygame
from src.core.constants import *
from src.ui.components import Button, TextBox, ProgressBar


class MainMenu:
    """Main menu screen"""

    def __init__(self, game):
        self.game = game
        self.buttons = {
            'new_game': Button(450, 300, 300, 60, "New Game", GREEN),
            'quit': Button(450, 400, 300, 60, "Quit", RED)
        }
        self.show_setup = False
        self.selected_ideology = 'liberal'
        self.party_name = "My Party"

        # Setup buttons
        self.ideology_buttons = {}
        x_offset = 200
        for i, (key, value) in enumerate(IDEOLOGIES.items()):
            y = 250 + (i * 70)
            self.ideology_buttons[key] = Button(x_offset, y, 300, 50, value['name'], value['color'])

        self.start_button = Button(450, 600, 300, 60, "Start Game", GREEN)
        self.back_button = Button(450, 680, 300, 60, "Back", GRAY)

    def handle_event(self, event):
        """Handle input events"""
        if not self.show_setup:
            if self.buttons['new_game'].handle_event(event):
                self.show_setup = True
            elif self.buttons['quit'].handle_event(event):
                self.game.running = False
        else:
            # In setup screen
            for ideology, button in self.ideology_buttons.items():
                if button.handle_event(event):
                    self.selected_ideology = ideology

            if self.start_button.handle_event(event):
                self.game.start_new_game(self.party_name, self.selected_ideology)
                self.show_setup = False

            if self.back_button.handle_event(event):
                self.show_setup = False

    def render(self, screen):
        """Draw the menu"""
        if not self.show_setup:
            # Main menu
            title_font = pygame.font.Font(None, 72)
            title = title_font.render("Political Strategy", True, WHITE)
            screen.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, 150))

            for button in self.buttons.values():
                button.render(screen)
        else:
            # Setup screen
            title_font = pygame.font.Font(None, 48)
            title = title_font.render("Create Your Party", True, WHITE)
            screen.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, 100))

            label_font = pygame.font.Font(None, 32)
            label = label_font.render("Choose Ideology:", True, WHITE)
            screen.blit(label, (200, 200))

            for button in self.ideology_buttons.values():
                button.render(screen)

            # Highlight selected
            if self.selected_ideology in self.ideology_buttons:
                selected_rect = self.ideology_buttons[self.selected_ideology].rect
                pygame.draw.rect(screen, YELLOW, selected_rect, 4)

            self.start_button.render(screen)
            self.back_button.render(screen)


class GameScreen:
    """Main game screen"""

    def __init__(self, game):
        self.game = game
        self.buttons = {
            'campaign': Button(50, 600, 200, 50, "Campaign", BLUE),
            'policy': Button(270, 600, 200, 50, "Policy", GREEN),
            'fundraise': Button(490, 600, 200, 50, "Fundraise", YELLOW),
            'end_turn': Button(950, 600, 200, 50, "End Turn", PURPLE)
        }

        # Stats bars
        self.support_bar = ProgressBar(50, 150, 300, 30)
        self.reputation_bar = ProgressBar(50, 220, 300, 30)

    def handle_event(self, event):
        """Handle input events"""
        if self.buttons['campaign'].handle_event(event):
            self.run_campaign()
        elif self.buttons['policy'].handle_event(event):
            self.propose_policy()
        elif self.buttons['fundraise'].handle_event(event):
            self.fundraise()
        elif self.buttons['end_turn'].handle_event(event):
            self.game.next_turn()

    def run_campaign(self):
        """Run a campaign (costs money, increases support)"""
        cost = 15000
        if self.game.player_party.can_afford(cost):
            self.game.player_party.adjust_funds(-cost)
            import random
            support_gain = random.uniform(1.5, 4.0)
            self.game.player_party.adjust_support(support_gain)

    def propose_policy(self):
        """Propose a new policy"""
        cost = 5000
        if self.game.player_party.can_afford(cost):
            self.game.player_party.adjust_funds(-cost)
            import random
            self.game.player_party.adjust_support(random.uniform(0.5, 2.0))
            self.game.player_party.adjust_reputation(random.uniform(1, 3))

    def fundraise(self):
        """Hold fundraising event"""
        import random
        funds_raised = random.randint(5000, 20000)
        self.game.player_party.adjust_funds(funds_raised)
        self.game.player_party.adjust_reputation(random.uniform(-1, 1))

    def render(self, screen):
        """Draw the game screen"""
        party = self.game.player_party

        # Title
        font = pygame.font.Font(None, 48)
        title = font.render(f"{party.name} - {IDEOLOGIES[party.ideology]['name']}", True, WHITE)
        screen.blit(title, (50, 50))

        # Date
        date_font = pygame.font.Font(None, 32)
        date_text = date_font.render(f"Q{self.game.quarter} {self.game.year} - Turn {self.game.turn}", True, WHITE)
        screen.blit(date_text, (50, 100))

        # Stats
        stats_font = pygame.font.Font(None, 28)

        # Support
        support_label = stats_font.render(f"Public Support: {party.support:.1f}%", True, WHITE)
        screen.blit(support_label, (50, 120))
        self.support_bar.set_value(party.support, GREEN if party.support > 25 else YELLOW if party.support > 15 else RED)
        self.support_bar.render(screen)

        # Reputation
        rep_label = stats_font.render(f"Reputation: {party.reputation:.0f}/100", True, WHITE)
        screen.blit(rep_label, (50, 190))
        self.reputation_bar.set_value(party.reputation, GREEN if party.reputation > 60 else YELLOW if party.reputation > 40 else RED)
        self.reputation_bar.render(screen)

        # Funds
        funds_label = stats_font.render(f"Funds: ${party.funds:,}", True, GREEN if party.funds > 50000 else RED)
        screen.blit(funds_label, (50, 260))

        # Seats
        seats_label = stats_font.render(f"Parliament Seats: {party.seats}/100", True, WHITE)
        screen.blit(seats_label, (50, 290))

        # Power status
        if party.is_in_power:
            power_label = stats_font.render("IN POWER", True, GREEN)
            screen.blit(power_label, (50, 320))

        # AI Parties status
        y_offset = 400
        ai_font = pygame.font.Font(None, 24)
        ai_title = pygame.font.Font(None, 32).render("Other Parties:", True, WHITE)
        screen.blit(ai_title, (700, 350))

        for ai_party in self.game.ai_parties:
            ai_text = ai_font.render(
                f"{ai_party.name}: {ai_party.support:.1f}% ({ai_party.seats} seats)",
                True,
                IDEOLOGIES[ai_party.ideology]['color']
            )
            screen.blit(ai_text, (700, y_offset))
            y_offset += 30

        # Action buttons
        for button in self.buttons.values():
            button.render(screen)

        # Info text
        info_font = pygame.font.Font(None, 20)
        info_texts = [
            "Campaign: Spend $15,000 to gain support",
            "Policy: Spend $5,000 to propose policy",
            "Fundraise: Raise money for your party",
            f"Next Election: Turn {((self.game.turn // ELECTION_TURN) + 1) * ELECTION_TURN}"
        ]

        y = 680
        for text in info_texts:
            rendered = info_font.render(text, True, LIGHT_GRAY)
            screen.blit(rendered, (50, y))
            y += 25


class ElectionScreen:
    """Election results screen"""

    def __init__(self, game):
        self.game = game
        self.continue_button = Button(450, 650, 300, 60, "Continue", GREEN)

    def handle_event(self, event):
        """Handle input events"""
        if self.continue_button.handle_event(event):
            self.game.current_screen = 'game'

    def render(self, screen):
        """Draw election results"""
        title_font = pygame.font.Font(None, 64)
        title = title_font.render("ELECTION RESULTS", True, WHITE)
        screen.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, 50))

        results = self.game.election_system.results
        y_offset = 200

        result_font = pygame.font.Font(None, 32)

        # Player result
        player_name = self.game.player_party.name
        player_votes = results['votes'].get(player_name, 0)
        player_seats = results['seats'].get(player_name, 0)

        player_text = result_font.render(
            f"{player_name}: {player_votes:.1f}% - {player_seats} seats",
            True,
            GREEN if self.game.player_party.is_in_power else WHITE
        )
        screen.blit(player_text, (300, y_offset))
        y_offset += 60

        # AI results
        for ai_party in self.game.ai_parties:
            votes = results['votes'].get(ai_party.name, 0)
            seats = results['seats'].get(ai_party.name, 0)

            ai_text = result_font.render(
                f"{ai_party.name}: {votes:.1f}% - {seats} seats",
                True,
                IDEOLOGIES[ai_party.ideology]['color']
            )
            screen.blit(ai_text, (300, y_offset))
            y_offset += 50

        # Winner announcement
        winner_font = pygame.font.Font(None, 48)
        if self.game.player_party.is_in_power:
            winner_text = winner_font.render("YOU WON THE ELECTION!", True, GREEN)
        else:
            winner = self.game.election_system.determine_winner(results)
            winner_text = winner_font.render(f"{winner} won the election", True, RED)

        screen.blit(winner_text, (SCREEN_WIDTH // 2 - winner_text.get_width() // 2, 500))

        self.continue_button.render(screen)


class EventScreen:
    """Random event screen"""

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

        # Title
        title_font = pygame.font.Font(None, 56)
        title = title_font.render(current_event.title, True, YELLOW)
        screen.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, 100))

        # Description
        desc_box = TextBox(200, 200, 800, 150)
        desc_box.set_text(current_event.description, WHITE)
        desc_box.render(screen)

        # Choices
        self.choice_buttons = []
        y_offset = 400

        for i, choice in enumerate(current_event.choices):
            button = Button(300, y_offset, 600, 60, choice.text, BLUE)
            self.choice_buttons.append(button)
            button.render(screen)

            # Show effects preview
            effects_font = pygame.font.Font(None, 20)
            effects_text = ", ".join([f"{k}: {v:+}" for k, v in choice.effects.items()])
            effects_surf = effects_font.render(effects_text, True, LIGHT_GRAY)
            screen.blit(effects_surf, (320, y_offset + 65))

            y_offset += 100
