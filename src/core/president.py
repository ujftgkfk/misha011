"""
President class and administration management
"""
import random


class President:
    """Represents the player as President"""

    def __init__(self, name="President"):
        self.name = name

        # Resources
        self.money = 500000  # Slush fund
        self.influence = 50  # Political capital
        self.approval_rating = 55.0  # Public approval %

        # Progress
        self.weeks_remaining = 208  # 4 years
        self.amendment_votes = 0  # Votes secured for immunity amendment
        self.impeachment_risk = 0  # 0-100, higher = more danger

        # Status
        self.is_impeached = False
        self.amendment_passed = False
        self.active_scandals = []
        self.investigations = []

        # Cabinet
        self.cabinet = {}
        self.loyalty_cabinet = {}  # Loyalty levels of cabinet members

    def adjust_money(self, amount):
        """Adjust money (can go negative for debt)"""
        self.money += amount

    def adjust_influence(self, amount):
        """Adjust political influence"""
        self.influence = max(0, min(100, self.influence + amount))

    def adjust_approval(self, amount):
        """Adjust approval rating"""
        self.approval_rating = max(0, min(100, self.approval_rating + amount))

    def adjust_impeachment_risk(self, amount):
        """Adjust impeachment risk"""
        self.impeachment_risk = max(0, min(100, self.impeachment_risk + amount))

    def add_scandal(self, scandal_name):
        """Add a scandal"""
        if scandal_name not in self.active_scandals:
            self.active_scandals.append(scandal_name)
            self.adjust_approval(-5)
            self.adjust_impeachment_risk(10)

    def add_investigation(self, investigation_name):
        """Add an investigation"""
        if investigation_name not in self.investigations:
            self.investigations.append(investigation_name)
            self.adjust_impeachment_risk(15)

    def remove_scandal(self, scandal_name):
        """Remove a scandal (cover-up successful)"""
        if scandal_name in self.active_scandals:
            self.active_scandals.remove(scandal_name)
            self.adjust_impeachment_risk(-5)

    def hire_cabinet_member(self, position, name, loyalty=50):
        """Hire a cabinet member"""
        self.cabinet[position] = name
        self.loyalty_cabinet[position] = loyalty

    def get_cabinet_loyalty(self, position):
        """Get loyalty of cabinet member"""
        return self.loyalty_cabinet.get(position, 0)

    def adjust_cabinet_loyalty(self, position, amount):
        """Adjust cabinet member loyalty"""
        if position in self.loyalty_cabinet:
            self.loyalty_cabinet[position] = max(0, min(100,
                self.loyalty_cabinet[position] + amount))

    def can_afford(self, cost_dict):
        """Check if can afford an action"""
        if 'money' in cost_dict and self.money < cost_dict['money']:
            return False
        if 'influence' in cost_dict and cost_dict['influence'] > 0:
            if self.influence < cost_dict['influence']:
                return False
        return True

    def pay_cost(self, cost_dict):
        """Pay the cost of an action"""
        for resource, amount in cost_dict.items():
            if resource == 'money':
                self.adjust_money(-amount)
            elif resource == 'influence':
                self.adjust_influence(-amount)
            elif resource == 'approval':
                self.adjust_approval(-amount)

    def get_status(self):
        """Get current status"""
        return {
            'name': self.name,
            'money': self.money,
            'influence': self.influence,
            'approval': self.approval_rating,
            'weeks_remaining': self.weeks_remaining,
            'amendment_votes': self.amendment_votes,
            'impeachment_risk': self.impeachment_risk,
            'scandals': len(self.active_scandals),
            'investigations': len(self.investigations)
        }


class Faction:
    """Represents a political faction"""

    def __init__(self, name, faction_type):
        self.name = name
        self.type = faction_type
        self.loyalty = 50  # 0-100
        self.influence_level = random.randint(40, 80)

    def adjust_loyalty(self, amount):
        """Adjust faction loyalty"""
        self.loyalty = max(0, min(100, self.loyalty + amount))

    def is_supportive(self):
        """Check if faction is supportive"""
        return self.loyalty > 60

    def will_help_with_amendment(self):
        """Check if faction will help with amendment"""
        return self.loyalty > 70 and random.random() < (self.loyalty / 100)
