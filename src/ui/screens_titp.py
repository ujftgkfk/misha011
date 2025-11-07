"""
This Is the President - UI Screens (exact copy of original)
"""
import pygame
from src.core.constants import *
from src.ui.components import Button, TextBox, ProgressBar


class MainMenuScreen:
    """Main menu - exact copy"""

    def __init__(self, game):
        self.game = game
        self.buttons = {
            'new_game': Button(450, 380, 300, 60, "NEW GAME", CRIMSON),
            'quit': Button(450, 480, 300, 60, "EXIT", DARK_GRAY)
        }

    def handle_event(self, event):
        if self.buttons['new_game'].handle_event(event):
            self.game.start_new_game()
        elif self.buttons['quit'].handle_event(event):
            self.game.running = False

    def render(self, screen):
        try:
            title_font = pygame.font.Font(None, 70)
            subtitle_font = pygame.font.Font(None, 34)
        except:
            title_font = pygame.font.SysFont('arial', 70, bold=True)
            subtitle_font = pygame.font.SysFont('arial', 34)

        title1 = title_font.render("THIS IS THE", True, WHITE)
        title2 = title_font.render("PRESIDENT", True, CRIMSON)
        subtitle = subtitle_font.render("Pass the 28th Amendment. By any means necessary.", True, LIGHT_GRAY)

        screen.blit(title1, (SCREEN_WIDTH // 2 - title1.get_width() // 2, 120))
        screen.blit(title2, (SCREEN_WIDTH // 2 - title2.get_width() // 2, 190))
        screen.blit(subtitle, (SCREEN_WIDTH // 2 - subtitle.get_width() // 2, 280))

        for btn in self.buttons.values():
            btn.render(screen)


class GameDashboard:
    """Main dashboard - like original game"""

    def __init__(self, game):
        self.game = game
        self.buttons = {
            'advisors': Button(900, 100, 250, 50, "Advisors", BLUE),
            'tasks': Button(900, 170, 250, 50, "Assign Tasks", DARK_GREEN),
            'next_week': Button(900, 680, 250, 60, "NEXT WEEK", CRIMSON)
        }

        # Progress bars
        self.amendment_bar = ProgressBar(50, 120, 400, 30)
        self.threat_bar = ProgressBar(50, 200, 400, 30)
        self.approval_bar = ProgressBar(50, 280, 400, 30)

    def handle_event(self, event):
        if self.buttons['advisors'].handle_event(event):
            self.game.current_screen = 'advisors'
        elif self.buttons['tasks'].handle_event(event):
            self.game.current_screen = 'tasks'
        elif self.buttons['next_week'].handle_event(event):
            self.game.next_week()

    def render(self, screen):
        try:
            title_font = pygame.font.Font(None, 42)
            label_font = pygame.font.Font(None, 26)
            small_font = pygame.font.Font(None, 20)
        except:
            title_font = pygame.font.SysFont('arial', 42, bold=True)
            label_font = pygame.font.SysFont('arial', 26)
            small_font = pygame.font.SysFont('arial', 20)

        # Title
        title = title_font.render("PRESIDENTIAL DASHBOARD", True, GOLD)
        screen.blit(title, (50, 30))

        # Week counter
        week_text = label_font.render(f"Week {self.game.week} / {self.game.week + self.game.weeks_remaining}", True, WHITE)
        screen.blit(week_text, (50, 75))

        weeks_left = small_font.render(f"{self.game.weeks_remaining} weeks until end of term", True, YELLOW)
        screen.blit(weeks_left, (250, 80))

        # Amendment Progress
        y = 100
        amend_label = label_font.render(f"28th Amendment: {self.game.amendment_votes}/67 votes", True, GOLD)
        screen.blit(amend_label, (50, y))
        y += 20
        self.amendment_bar.set_value(self.game.amendment_votes, 67, GOLD)
        self.amendment_bar.render(screen)

        # Overall Threat Level
        y = 180
        threat = self.game.threat_manager.overall_threat
        threat_color = RED if threat > 70 else ORANGE if threat > 40 else YELLOW
        threat_label = label_font.render(f"Threat Level: {threat:.0f}%", True, threat_color)
        screen.blit(threat_label, (50, y))
        y += 20
        self.threat_bar.set_value(threat, 100, threat_color)
        self.threat_bar.render(screen)

        # Approval Rating
        y = 260
        approval = self.game.president.approval_rating
        approval_color = GREEN if approval > 50 else YELLOW if approval > 30 else RED
        approval_label = label_font.render(f"Approval: {approval:.1f}%", True, approval_color)
        screen.blit(approval_label, (50, y))
        y += 20
        self.approval_bar.set_value(approval, 100, approval_color)
        self.approval_bar.render(screen)

        # Money
        money_color = GREEN if self.game.president.money > 200000 else YELLOW if self.game.president.money > 50000 else RED
        money_label = label_font.render(f"Funds: ${self.game.president.money:,}", True, money_color)
        screen.blit(money_label, (50, 340))

        # Active Investigations
        y = 400
        inv_title = title_font.render("ACTIVE INVESTIGATIONS", True, RED)
        screen.blit(inv_title, (50, y))
        y += 50

        active_invs = [inv for inv in self.game.threat_manager.investigations if inv.is_active]
        if active_invs:
            for inv in active_invs[:3]:  # Show top 3
                inv_text = label_font.render(f"{inv.name}: {inv.progress:.0f}%", True, RED)
                screen.blit(inv_text, (70, y))

                danger = small_font.render(f"[{inv.get_danger_level()}]", True,
                    CRIMSON if inv.get_danger_level() == "CRITICAL" else ORANGE)
                screen.blit(danger, (450, y + 5))

                y += 35
        else:
            no_inv = label_font.render("No active investigations", True, GREEN)
            screen.blit(no_inv, (70, y))

        # Team Status
        y = 580
        team_title = title_font.render("TEAM STATUS", True, BLUE)
        screen.blit(team_title, (50, y))
        y += 50

        busy_count = len([adv for adv in self.game.advisors if adv.is_busy])
        team_text = label_font.render(f"{busy_count}/{len(self.game.advisors)} advisors on assignment", True, WHITE)
        screen.blit(team_text, (70, y))

        # Buttons
        for btn in self.buttons.values():
            btn.render(screen)

        # Goal reminder
        goal = small_font.render("GOAL: Secure 67 votes for the 28th Amendment", True, GOLD)
        screen.blit(goal, (50, 760))


class AdvisorScreen:
    """Advisor management screen"""

    def __init__(self, game):
        self.game = game
        self.back_button = Button(50, 720, 200, 50, "Back", DARK_GRAY)

    def handle_event(self, event):
        if self.back_button.handle_event(event):
            self.game.current_screen = 'dashboard'

    def render(self, screen):
        try:
            title_font = pygame.font.Font(None, 42)
            label_font = pygame.font.Font(None, 24)
            small_font = pygame.font.Font(None, 20)
        except:
            title_font = pygame.font.SysFont('arial', 42, bold=True)
            label_font = pygame.font.SysFont('arial', 24)
            small_font = pygame.font.SysFont('arial', 20)

        title = title_font.render("YOUR TEAM", True, GOLD)
        screen.blit(title, (50, 30))

        y = 100
        for advisor in self.game.advisors:
            # Advisor card
            card_color = DARK_GRAY if not advisor.is_busy else VERY_DARK_GRAY
            pygame.draw.rect(screen, card_color, [50, y, 1100, 90])
            pygame.draw.rect(screen, WHITE, [50, y, 1100, 90], 2)

            # Name and role
            name = label_font.render(advisor.name, True, WHITE)
            screen.blit(name, (70, y + 10))

            role = small_font.render(advisor.role, True, LIGHT_GRAY)
            screen.blit(role, (70, y + 35))

            # Status
            if advisor.is_busy:
                status = small_font.render(f"ON MISSION: {advisor.current_task.name}", True, YELLOW)
                weeks = small_font.render(f"Week {advisor.weeks_on_task}/{advisor.current_task.duration_weeks}", True, YELLOW)
                screen.blit(status, (70, y + 60))
                screen.blit(weeks, (400, y + 60))
            else:
                status = small_font.render("AVAILABLE", True, GREEN)
                screen.blit(status, (70, y + 60))

            # Loyalty and stress
            loyalty_text = small_font.render(f"Loyalty: {advisor.loyalty}%", True,
                GREEN if advisor.loyalty > 70 else YELLOW if advisor.loyalty > 40 else RED)
            screen.blit(loyalty_text, (700, y + 20))

            stress_text = small_font.render(f"Stress: {advisor.stress}%", True,
                RED if advisor.stress > 70 else YELLOW if advisor.stress > 40 else GREEN)
            screen.blit(stress_text, (700, y + 50))

            # Skills preview
            skills_text = small_font.render(f"Skills: Legal {advisor.skills.get('legal', 5)}, " +
                f"Illegal {advisor.skills.get('illegal', 5)}, Media {advisor.skills.get('media', 5)}",
                True, LIGHT_GRAY)
            screen.blit(skills_text, (900, y + 35))

            y += 105

        self.back_button.render(screen)


class TaskScreen:
    """Task assignment screen"""

    def __init__(self, game):
        self.game = game
        self.back_button = Button(50, 720, 200, 50, "Back", DARK_GRAY)
        self.selected_advisor = None
        self.selected_task = None

    def handle_event(self, event):
        if self.back_button.handle_event(event):
            self.game.current_screen = 'dashboard'

    def render(self, screen):
        title_font = pygame.font.Font(None, 42)
        label_font = pygame.font.Font(None, 24)

        title = title_font.render("ASSIGN TASKS", True, GOLD)
        screen.blit(title, (50, 30))

        # Placeholder for task assignment interface
        info = label_font.render("Task assignment interface - Coming soon", True, WHITE)
        screen.blit(info, (50, 100))

        self.back_button.render(screen)


class EventScreen:
    """Random event screen"""

    def __init__(self, game):
        self.game = game

    def handle_event(self, event):
        pass

    def render(self, screen):
        pass


class EndGameScreen:
    """End game screen"""

    def __init__(self, game):
        self.game = game
        self.menu_button = Button(450, 650, 300, 60, "Main Menu", DARK_GRAY)

    def handle_event(self, event):
        if self.menu_button.handle_event(event):
            self.game.current_screen = 'menu'

    def render(self, screen):
        try:
            title_font = pygame.font.Font(None, 72)
            text_font = pygame.font.Font(None, 32)
        except:
            title_font = pygame.font.SysFont('arial', 72, bold=True)
            text_font = pygame.font.SysFont('arial', 32)

        # Title
        color = GOLD if self.game.victory else CRIMSON
        title = title_font.render(self.game.end_reason, True, color)
        screen.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, 200))

        # Stats
        stats = [
            f"Weeks Survived: {self.game.week}",
            f"Amendment Votes: {self.game.amendment_votes}/67",
            f"Final Approval: {self.game.president.approval_rating:.1f}%",
            f"Remaining Funds: ${self.game.president.money:,}"
        ]

        y = 350
        for stat in stats:
            text = text_font.render(stat, True, WHITE)
            screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, y))
            y += 50

        self.menu_button.render(screen)
