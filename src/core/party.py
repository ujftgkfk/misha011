"""
Political Party class and management
"""

class Party:
    """Represents a political party in the game"""

    def __init__(self, name, ideology, funds=100000, support=15.0):
        self.name = name
        self.ideology = ideology
        self.funds = funds
        self.support = support  # Percentage of population support
        self.reputation = 50  # 0-100 scale
        self.policies = []
        self.seats = 0  # Parliament seats
        self.is_in_power = False

    def adjust_support(self, amount):
        """Adjust public support, keeping it between 0 and 100"""
        self.support = max(0, min(100, self.support + amount))

    def adjust_funds(self, amount):
        """Adjust party funds"""
        self.funds += amount

    def adjust_reputation(self, amount):
        """Adjust reputation, keeping it between 0 and 100"""
        self.reputation = max(0, min(100, self.reputation + amount))

    def can_afford(self, cost):
        """Check if party can afford an action"""
        return self.funds >= cost

    def add_policy(self, policy):
        """Add a policy to the party platform"""
        if policy not in self.policies:
            self.policies.append(policy)

    def get_status(self):
        """Get current party status as dict"""
        return {
            'name': self.name,
            'ideology': self.ideology,
            'funds': self.funds,
            'support': self.support,
            'reputation': self.reputation,
            'seats': self.seats,
            'in_power': self.is_in_power
        }


class AIParty(Party):
    """AI-controlled opposition party"""

    def __init__(self, name, ideology, funds=80000, support=20.0):
        super().__init__(name, ideology, funds, support)
        self.aggressiveness = 0.5  # 0-1 scale

    def make_decision(self, game_state):
        """AI decision making for campaigns and actions"""
        # Simple AI: randomly adjust support based on aggressiveness
        import random

        # AI campaigns
        if self.funds > 20000 and random.random() < self.aggressiveness:
            self.funds -= 15000
            self.adjust_support(random.uniform(0.5, 2.0))
