"""
This Is the President - Exact game engine copy
Complete recreation of original game mechanics
"""
import pygame
import sys
import random
from src.core.constants import *
from src.core.president import President
from src.core.advisor import Advisor, ADVISOR_TEMPLATES, TASK_TEMPLATES
from src.core.investigation import ThreatManager, INVESTIGATION_TEMPLATES
from src.ui.screens_titp import MainMenuScreen, GameDashboard, AdvisorScreen, TaskScreen, EventScreen, EndGameScreen


class GameTITP:
    """This Is the President - Complete game engine"""

    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("This Is the President")
        self.clock = pygame.time.Clock()
        self.running = True

        # Game state
        self.current_screen = 'menu'
        self.president = None
        self.advisors = []
        self.threat_manager = None

        # Amendment progress
        self.amendment_votes = 0  # Need 67 out of 100
        self.votes_needed = 67

        # Time
        self.week = 1
        self.weeks_remaining = 208  # 4 years

        # Game status
        self.game_over = False
        self.victory = False
        self.end_reason = ""

        # Available tasks
        self.available_tasks = []

        # UI Screens
        self.menu_screen = MainMenuScreen(self)
        self.dashboard = GameDashboard(self)
        self.advisor_screen = AdvisorScreen(self)
        self.task_screen = TaskScreen(self)
        self.event_screen = EventScreen(self)
        self.end_screen = EndGameScreen(self)

        # Fonts
        try:
            self.font_large = pygame.font.Font(None, 48)
            self.font_medium = pygame.font.Font(None, 32)
            self.font_small = pygame.font.Font(None, 24)
        except:
            self.font_large = pygame.font.SysFont('arial', 48, bold=True)
            self.font_medium = pygame.font.SysFont('arial', 32)
            self.font_small = pygame.font.SysFont('arial', 24)

    def start_new_game(self, difficulty='normal'):
        """Start new game - like original"""
        # Create President
        self.president = President("Mr. President")
        self.president.money = 500000
        self.president.approval_rating = 55.0
        self.president.influence = 50

        # Create advisors team (like original game)
        advisor_names = [
            ("Richard Moss", "chief_of_staff"),
            ("Sarah Chen", "attorney_general"),
            ("Marcus Webb", "press_secretary"),
            ("General Hayes", "security_advisor"),
            ("Tony 'The Fixer' Romano", "fixer"),
            ("Victoria Sterling", "lobbyist")
        ]

        self.advisors = []
        for name, template_key in advisor_names:
            template = ADVISOR_TEMPLATES[template_key]
            advisor = Advisor(name, template['role'], template['skills'].copy())
            self.advisors.append(advisor)

        # Initialize threat manager
        self.threat_manager = ThreatManager()

        # Add initial investigation (like in original)
        initial_inv = INVESTIGATION_TEMPLATES['corruption']
        self.threat_manager.add_investigation(initial_inv)

        # Reset progress
        self.amendment_votes = 0
        self.week = 1
        self.weeks_remaining = 208
        self.game_over = False
        self.victory = False

        # Initialize available tasks
        self._refresh_available_tasks()

        self.current_screen = 'dashboard'

    def _refresh_available_tasks(self):
        """Refresh available tasks (like original game task board)"""
        self.available_tasks = list(TASK_TEMPLATES.values())

    def next_week(self):
        """Advance to next week - core game loop"""
        if self.game_over:
            return

        self.week += 1
        self.weeks_remaining -= 1

        # Update all advisors
        for advisor in self.advisors:
            if advisor.is_busy and advisor.current_task:
                advisor.weeks_on_task += 1

                # Task completion
                if advisor.weeks_on_task >= advisor.current_task.duration_weeks:
                    self._complete_task(advisor)

            # Natural stress decay
            advisor.adjust_stress(-2)

        # Investigations progress
        self.threat_manager.weekly_update()

        # Weekly costs
        self.president.adjust_money(-10000)  # Administration costs

        # Natural approval fluctuation
        self.president.adjust_approval(random.uniform(-1, 1))

        # Random events (25% chance)
        if random.random() < 0.25:
            self._trigger_random_event()

        # Check win/lose conditions
        self._check_game_over()

    def assign_task(self, advisor, task):
        """Assign a task to an advisor"""
        if advisor.is_busy:
            return False

        # Check if can afford
        if task.cost > 0 and self.president.money < task.cost:
            return False

        # Pay cost
        self.president.adjust_money(-task.cost)

        # Assign task
        advisor.assign_task(task)

        # Illegal tasks increase stress and lower loyalty
        if task.is_illegal:
            advisor.adjust_stress(15)
            if not advisor.is_corrupted:
                advisor.adjust_loyalty(-5)

        return True

    def _complete_task(self, advisor):
        """Complete an advisor's task"""
        task = advisor.current_task

        # Calculate success
        success_chance = advisor.calculate_success_chance(task)
        success = random.random() * 100 < success_chance

        if success:
            # Apply effects
            for effect, value in task.effects.items():
                if effect == 'amendment_votes':
                    self.amendment_votes = min(100, self.amendment_votes + value)
                elif effect == 'approval':
                    self.president.adjust_approval(value)
                elif effect == 'money':
                    self.president.adjust_money(value)
                elif effect == 'impeachment_risk':
                    self.president.adjust_impeachment_risk(value)
                elif effect == 'investigation_progress':
                    # Reduce most dangerous investigation
                    inv = self.threat_manager.get_most_dangerous_investigation()
                    if inv:
                        inv.setback(abs(value))

            # Reduce stress on success
            advisor.adjust_stress(-5)
            advisor.adjust_loyalty(2)
        else:
            # Failure consequences
            if task.is_illegal:
                # Illegal task failure is BAD
                self.president.adjust_impeachment_risk(10)
                advisor.adjust_stress(10)
                advisor.adjust_loyalty(-5)

                # Might trigger scandal
                if random.random() < 0.3:
                    self.threat_manager.add_scandal(
                        f"{task.name} Exposure",
                        task.severity if hasattr(task, 'severity') else 3
                    )
            else:
                # Legal task failure is just wasted time
                advisor.adjust_stress(5)

        # Complete task
        advisor.complete_task()

    def _trigger_random_event(self):
        """Trigger a random event"""
        # This would show event screen with choices
        # For now, skip to keep it simple
        pass

    def _check_game_over(self):
        """Check for win/lose conditions"""
        # WIN: Amendment passed
        if self.amendment_votes >= self.votes_needed:
            self.victory = True
            self.game_over = True
            self.end_reason = "IMMUNITY SECURED"
            self.current_screen = 'endgame'
            return

        # WIN: Survived full term
        if self.weeks_remaining <= 0:
            if self.president.impeachment_risk < 80:
                self.victory = True
                self.end_reason = "SURVIVED PRESIDENCY"
            else:
                self.victory = False
                self.end_reason = "IMPEACHED AT END OF TERM"
            self.game_over = True
            self.current_screen = 'endgame'
            return

        # LOSE: Impeachment risk too high
        if self.president.impeachment_risk >= 100:
            self.victory = False
            self.game_over = True
            self.end_reason = "IMPEACHED"
            self.current_screen = 'endgame'
            return

        # LOSE: Investigation completed
        for inv in self.threat_manager.investigations:
            if not inv.is_active and inv.progress >= 100:
                self.victory = False
                self.game_over = True
                self.end_reason = f"CONVICTED - {inv.name}"
                self.current_screen = 'endgame'
                return

        # LOSE: Approval too low
        if self.president.approval_rating < 10:
            self.victory = False
            self.game_over = True
            self.end_reason = "FORCED TO RESIGN"
            self.current_screen = 'endgame'
            return

    def get_available_advisors(self):
        """Get advisors who are not busy"""
        return [adv for adv in self.advisors if not adv.is_busy]

    def run(self):
        """Main game loop"""
        while self.running:
            # Handle events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

                # Route to current screen
                if self.current_screen == 'menu':
                    self.menu_screen.handle_event(event)
                elif self.current_screen == 'dashboard':
                    self.dashboard.handle_event(event)
                elif self.current_screen == 'advisors':
                    self.advisor_screen.handle_event(event)
                elif self.current_screen == 'tasks':
                    self.task_screen.handle_event(event)
                elif self.current_screen == 'event':
                    self.event_screen.handle_event(event)
                elif self.current_screen == 'endgame':
                    self.end_screen.handle_event(event)

            # Render
            self.screen.fill(VERY_DARK_GRAY)

            if self.current_screen == 'menu':
                self.menu_screen.render(self.screen)
            elif self.current_screen == 'dashboard':
                self.dashboard.render(self.screen)
            elif self.current_screen == 'advisors':
                self.advisor_screen.render(self.screen)
            elif self.current_screen == 'tasks':
                self.task_screen.render(self.screen)
            elif self.current_screen == 'event':
                self.event_screen.render(self.screen)
            elif self.current_screen == 'endgame':
                self.end_screen.render(self.screen)

            pygame.display.flip()
            self.clock.tick(FPS)

        pygame.quit()
        sys.exit()
