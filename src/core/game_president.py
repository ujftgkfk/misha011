"""
Main game engine - This Is the President style
"""
import pygame
import sys
import random
from src.core.constants import *
from src.core.president import President, Faction
from src.systems.events_president import EventManager
from src.ui.screens_president import MainMenu, GameScreen, EventScreen, EndScreen


class Game:
    """Main game class - Presidential power management"""

    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("This Is the President")
        self.clock = pygame.time.Clock()
        self.running = True

        # Game state
        self.current_screen = 'menu'
        self.president = None
        self.factions = {}
        self.week = 0
        self.year = 1
        self.game_over = False
        self.victory = False

        # Systems
        self.event_manager = EventManager()
        self.current_event = None

        # UI Screens
        self.menu_screen = MainMenu(self)
        self.game_screen = GameScreen(self)
        self.event_screen = EventScreen(self)
        self.end_screen = EndScreen(self)

        # Fonts
        try:
            self.font_large = pygame.font.Font(None, 48)
            self.font_medium = pygame.font.Font(None, 36)
            self.font_small = pygame.font.Font(None, 24)
        except:
            self.font_large = pygame.font.SysFont('arial', 48)
            self.font_medium = pygame.font.SysFont('arial', 36)
            self.font_small = pygame.font.SysFont('arial', 24)

    def start_new_game(self, name="Mr. President", difficulty='normal'):
        """Initialize a new game"""
        diff = DIFFICULTY[difficulty]

        # Create president
        self.president = President(name)
        self.president.money = int(STARTING_MONEY * diff['money_mult'])
        self.president.approval_rating = STARTING_APPROVAL * diff['approval_mult']

        # Create factions
        for faction_id, faction_info in FACTIONS.items():
            self.factions[faction_id] = Faction(faction_info['name'], faction_id)

        # Initialize cabinet with temp members
        for position in CABINET_POSITIONS:
            self.president.hire_cabinet_member(position, "Acting " + position, loyalty=40)

        self.week = 0
        self.year = 1
        self.game_over = False
        self.victory = False
        self.current_screen = 'game'

    def next_week(self):
        """Advance to next week"""
        self.week += 1
        self.president.weeks_remaining -= 1

        if self.week > 52:
            self.week = 1
            self.year += 1

        # Random event chance (25% each week)
        if random.random() < 0.25:
            self.current_event = self.event_manager.get_random_event()
            if self.current_event:
                self.current_screen = 'event'

        # Natural decay/changes
        self.president.adjust_approval(random.uniform(-1.5, 1.5))

        # Weekly costs
        self.president.adjust_money(-5000)  # Administration costs

        # Impeachment risk decay
        if self.president.impeachment_risk > 0:
            self.president.adjust_impeachment_risk(-1)

        # Check for game over conditions
        self.check_game_over()

    def check_game_over(self):
        """Check if game should end"""
        # Win condition: Amendment passed
        if self.president.amendment_votes >= AMENDMENT_REQUIRED_VOTES:
            self.president.amendment_passed = True
            self.victory = True
            self.game_over = True
            self.current_screen = 'end'

        # Win condition: Survived 4 years
        if self.president.weeks_remaining <= 0 and not self.president.is_impeached:
            self.victory = True
            self.game_over = True
            self.current_screen = 'end'

        # Lose condition: Impeached
        if self.president.impeachment_risk >= 100:
            self.president.is_impeached = True
            self.victory = False
            self.game_over = True
            self.current_screen = 'end'

        # Lose condition: Approval too low for too long
        if self.president.approval_rating < 15:
            self.president.impeachment_risk += 5

    def handle_event_choice(self, choice_index):
        """Handle player's choice in an event"""
        if self.current_event and 0 <= choice_index < len(self.current_event.choices):
            choice = self.current_event.choices[choice_index]
            self.event_manager.apply_choice_effects(self.president, choice)
            self.current_event = None
            self.current_screen = 'game'

    def perform_action(self, action_name):
        """Perform a presidential action"""
        if action_name not in ACTION_COSTS:
            return False

        cost = ACTION_COSTS[action_name]

        if not self.president.can_afford(cost):
            return False

        self.president.pay_cost(cost)

        # Apply action effects
        if action_name == 'bribe_congress':
            votes_gained = random.randint(3, 8)
            self.president.amendment_votes += votes_gained

        elif action_name == 'propaganda':
            self.president.adjust_approval(random.uniform(3, 7))

        elif action_name == 'cover_up':
            if self.president.active_scandals:
                scandal = random.choice(self.president.active_scandals)
                self.president.remove_scandal(scandal)

        elif action_name == 'executive_order':
            self.president.adjust_approval(random.uniform(-2, 5))

        elif action_name == 'public_speech':
            self.president.adjust_approval(random.uniform(2, 5))
            self.president.adjust_influence(random.randint(-2, 3))

        elif action_name == 'backroom_deal':
            faction = random.choice(list(self.factions.values()))
            faction.adjust_loyalty(random.randint(5, 15))

        elif action_name == 'dismiss_official':
            self.president.adjust_impeachment_risk(random.randint(-5, 10))

        return True

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
                elif self.current_screen == 'event':
                    self.event_screen.handle_event(event)
                elif self.current_screen == 'end':
                    self.end_screen.handle_event(event)

            # Render current screen
            self.screen.fill(VERY_DARK_GRAY)

            if self.current_screen == 'menu':
                self.menu_screen.render(self.screen)
            elif self.current_screen == 'game':
                self.game_screen.render(self.screen)
            elif self.current_screen == 'event':
                self.event_screen.render(self.screen)
            elif self.current_screen == 'end':
                self.end_screen.render(self.screen)

            pygame.display.flip()
            self.clock.tick(FPS)

        pygame.quit()
        sys.exit()
