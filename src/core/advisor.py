"""
Advisor/Team member system - exact copy of This Is the President
"""
import random


class Advisor:
    """Team member with skills and loyalty - like in original game"""

    def __init__(self, name, role, skills):
        self.name = name
        self.role = role  # Chief of Staff, AG, Press Secretary, etc.

        # Skills (1-10 scale like in original)
        self.skills = skills  # {'legal': 7, 'illegal': 3, 'media': 8, 'investigation': 5}

        # Status
        self.loyalty = 50  # 0-100
        self.stress = 0  # 0-100, high stress = lower performance
        self.is_busy = False
        self.current_task = None
        self.weeks_on_task = 0

        # Traits
        self.is_corrupted = False
        self.can_be_corrupted = True
        self.will_betray = False

    def assign_task(self, task):
        """Assign advisor to a task"""
        self.is_busy = True
        self.current_task = task
        self.weeks_on_task = 0

    def complete_task(self):
        """Complete current task"""
        self.is_busy = False
        task = self.current_task
        self.current_task = None
        self.weeks_on_task = 0
        return task

    def calculate_success_chance(self, task):
        """Calculate chance of success for a task"""
        base_skill = self.skills.get(task.skill_required, 5)

        # Modifiers
        loyalty_mod = (self.loyalty - 50) / 100  # -0.5 to +0.5
        stress_mod = -self.stress / 200  # 0 to -0.5

        chance = base_skill * 10  # 0-100%
        chance += loyalty_mod * 20
        chance += stress_mod * 20

        if task.is_illegal and not self.is_corrupted:
            chance -= 20  # Less effective if not corrupted

        return max(10, min(95, chance))

    def adjust_loyalty(self, amount):
        """Adjust loyalty"""
        self.loyalty = max(0, min(100, self.loyalty + amount))

        # Check for betrayal
        if self.loyalty < 20 and random.random() < 0.3:
            self.will_betray = True

    def adjust_stress(self, amount):
        """Adjust stress"""
        self.stress = max(0, min(100, self.stress + amount))

        # High stress decreases loyalty
        if self.stress > 80:
            self.adjust_loyalty(-1)

    def corrupt(self):
        """Corrupt this advisor (make them willing to do illegal things)"""
        if self.can_be_corrupted:
            self.is_corrupted = True
            self.adjust_loyalty(-10)  # They know your secrets now
            return True
        return False


class Task:
    """A task/mission that can be assigned to advisors"""

    def __init__(self, name, description, skill_required, duration_weeks,
                 is_illegal=False, effects=None, cost=0):
        self.name = name
        self.description = description
        self.skill_required = skill_required  # 'legal', 'illegal', 'media', etc.
        self.duration_weeks = duration_weeks
        self.is_illegal = is_illegal
        self.effects = effects or {}  # Effects on success
        self.cost = cost  # Money cost
        self.progress = 0  # 0-100


# Predefined advisor templates
ADVISOR_TEMPLATES = {
    'chief_of_staff': {
        'role': 'Chief of Staff',
        'skills': {'legal': 8, 'illegal': 4, 'media': 7, 'investigation': 6}
    },
    'attorney_general': {
        'role': 'Attorney General',
        'skills': {'legal': 9, 'illegal': 3, 'media': 5, 'investigation': 8}
    },
    'press_secretary': {
        'role': 'Press Secretary',
        'skills': {'legal': 5, 'illegal': 2, 'media': 9, 'investigation': 4}
    },
    'security_advisor': {
        'role': 'National Security Advisor',
        'skills': {'legal': 6, 'illegal': 7, 'media': 4, 'investigation': 7}
    },
    'fixer': {
        'role': 'Personal Fixer',
        'skills': {'legal': 3, 'illegal': 9, 'media': 6, 'investigation': 5}
    },
    'lobbyist': {
        'role': 'Chief Lobbyist',
        'skills': {'legal': 7, 'illegal': 5, 'media': 6, 'investigation': 4}
    }
}


# Task templates
TASK_TEMPLATES = {
    # Legal tasks
    'lobby_congress': Task(
        "Lobby Congress Member",
        "Legally lobby a member of Congress for their vote on the amendment",
        'legal',
        2,
        False,
        {'amendment_votes': 1, 'money': -10000},
        10000
    ),

    'media_campaign': Task(
        "Run Media Campaign",
        "Launch a positive media campaign to improve public approval",
        'media',
        1,
        False,
        {'approval': 5, 'money': -25000},
        25000
    ),

    'investigate_threat': Task(
        "Counter-Investigation",
        "Legally investigate those investigating you",
        'investigation',
        3,
        False,
        {'investigation_progress': -10, 'money': -15000},
        15000
    ),

    # Illegal tasks
    'bribe_congressman': Task(
        "Bribe Congressman",
        "Illegally bribe a congressman for their vote (risky)",
        'illegal',
        1,
        True,
        {'amendment_votes': 2, 'money': -50000, 'impeachment_risk': 10},
        50000
    ),

    'blackmail_politician': Task(
        "Blackmail Politician",
        "Use compromising information to secure a vote",
        'illegal',
        2,
        True,
        {'amendment_votes': 1, 'impeachment_risk': 15},
        30000
    ),

    'sabotage_investigation': Task(
        "Sabotage Investigation",
        "Illegally interfere with the investigation against you",
        'illegal',
        2,
        True,
        {'investigation_progress': -25, 'impeachment_risk': 20, 'money': -40000},
        40000
    ),

    'cover_up': Task(
        "Cover Up Evidence",
        "Destroy or hide evidence of your crimes",
        'illegal',
        3,
        True,
        {'investigation_progress': -30, 'impeachment_risk': 25, 'money': -60000},
        60000
    ),

    'threaten_witness': Task(
        "Threaten Witness",
        "Intimidate a witness to prevent them from testifying",
        'illegal',
        1,
        True,
        {'investigation_progress': -15, 'impeachment_risk': 30},
        20000
    ),

    # Media tasks
    'press_conference': Task(
        "Press Conference",
        "Hold a press conference to address concerns",
        'media',
        1,
        False,
        {'approval': 3, 'investigation_progress': -5},
        5000
    ),

    'smear_campaign': Task(
        "Smear Campaign",
        "Launch negative campaign against investigators (illegal)",
        'illegal',
        2,
        True,
        {'investigation_progress': -20, 'approval': -5, 'impeachment_risk': 10},
        35000
    )
}
