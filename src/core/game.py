"""
Main game engine and game loop
"""
import pygame
import sys
from src.core.constants import *
from src.core.party import Party, AIParty
from src.systems.events import EventManager
from src.systems.election import Election
from src.ui.screens import MainMenu, GameScreen, ElectionScreen, EventScreen


class Game:
    """Main game class that manages game state and flow"""

    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Political Strategy Game")
        self.clock = pygame.time.Clock()
        self.running = True

        # Game state
        self.current_screen = 'menu'
        self.player_party = None
        self.ai_parties = []
        self.turn = 0
        self.year = 2024
        self.quarter = 1

        # Systems
        self.event_manager = EventManager()
        self.election_system = Election()
        self.current_event = None

        # UI Screens
        self.menu_screen = MainMenu(self)
        self.game_screen = GameScreen(self)
        self.election_screen = ElectionScreen(self)
        self.event_screen = EventScreen(self)

        # Fonts
        self.font_large = pygame.font.Font(None, 48)
        self.font_medium = pygame.font.Font(None, 36)
        self.font_small = pygame.font.Font(None, 24)

    def start_new_game(self, party_name, ideology, difficulty='normal'):
        """Initialize a new game"""
        diff = DIFFICULTY[difficulty]

        # Create player party
        starting_funds = int(STARTING_FUNDS * diff['funds_multiplier'])
        starting_support = STARTING_SUPPORT * diff['support_multiplier']
        self.player_party = Party(party_name, ideology, starting_funds, starting_support)

        # Create AI parties
        self.ai_parties = [
            AIParty("People's Alliance", 'liberal', 90000, 25.0),
            AIParty("National Front", 'conservative', 85000, 22.0),
            AIParty("Progressive Unity", 'progressive', 75000, 18.0),
            AIParty("Centrist Coalition", 'centrist', 80000, 20.0)
        ]

        self.turn = 0
        self.year = 2024
        self.quarter = 1
        self.current_screen = 'game'

    def next_turn(self):
        """Advance to next turn"""
        self.turn += 1
        self.quarter += 1

        if self.quarter > 4:
            self.quarter = 1
            self.year += 1

        # Random event chance (30% each turn)
        import random
        if random.random() < 0.3:
            self.current_event = self.event_manager.get_random_event()
            if self.current_event:
                self.current_screen = 'event'

        # Check for election
        if self.turn % ELECTION_TURN == 0:
            self.hold_election()

        # AI parties take actions
        for ai_party in self.ai_parties:
            ai_party.make_decision({'turn': self.turn})

        # Natural support decay/growth
        self.player_party.adjust_support(random.uniform(-0.5, 0.5))

    def hold_election(self):
        """Trigger an election"""
        results = self.election_system.calculate_results(self.player_party, self.ai_parties)

        # Update party seats
        self.player_party.seats = results['seats'][self.player_party.name]
        for ai_party in self.ai_parties:
            ai_party.seats = results['seats'].get(ai_party.name, 0)

        # Determine winner
        winner = self.election_system.determine_winner(results)
        self.player_party.is_in_power = (winner == self.player_party.name)

        self.current_screen = 'election'

    def handle_event_choice(self, choice_index):
        """Handle player's choice in an event"""
        if self.current_event and 0 <= choice_index < len(self.current_event.choices):
            choice = self.current_event.choices[choice_index]
            self.event_manager.apply_choice_effects(self.player_party, choice)
            self.current_event = None
            self.current_screen = 'game'

    def run(self):
        """Main game loop"""
        while self.running:
            # Handle events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

                # Route events to current screen
                if self.current_screen == 'menu':
                    self.menu_screen.handle_event(event)
                elif self.current_screen == 'game':
                    self.game_screen.handle_event(event)
                elif self.current_screen == 'election':
                    self.election_screen.handle_event(event)
                elif self.current_screen == 'event':
                    self.event_screen.handle_event(event)

            # Render current screen
            self.screen.fill(DARK_GRAY)

            if self.current_screen == 'menu':
                self.menu_screen.render(self.screen)
            elif self.current_screen == 'game':
                self.game_screen.render(self.screen)
            elif self.current_screen == 'election':
                self.election_screen.render(self.screen)
            elif self.current_screen == 'event':
                self.event_screen.render(self.screen)

            pygame.display.flip()
            self.clock.tick(FPS)

        pygame.quit()
        sys.exit()
