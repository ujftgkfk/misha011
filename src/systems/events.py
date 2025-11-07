"""
Event system for random game events and decisions
"""
import random


class Event:
    """Represents a game event with choices"""

    def __init__(self, title, description, choices):
        self.title = title
        self.description = description
        self.choices = choices  # List of Choice objects


class Choice:
    """Represents a choice in an event"""

    def __init__(self, text, effects):
        self.text = text
        self.effects = effects  # Dict of effects: {'support': +5, 'funds': -1000, etc.}


class EventManager:
    """Manages random events in the game"""

    def __init__(self):
        self.events = self._create_events()
        self.current_event = None

    def _create_events(self):
        """Create all possible events"""
        events = []

        # Economic crisis event
        events.append(Event(
            "Economic Crisis",
            "The country is facing an economic downturn. How should your party respond?",
            [
                Choice("Propose tax cuts for businesses",
                       {'support': -2, 'funds': 5000, 'reputation': -5}),
                Choice("Increase social spending",
                       {'support': 3, 'funds': -10000, 'reputation': 5}),
                Choice("Take no action",
                       {'support': -5, 'reputation': -3})
            ]
        ))

        # Scandal event
        events.append(Event(
            "Party Scandal",
            "A member of your party is involved in a corruption scandal!",
            [
                Choice("Defend the member publicly",
                       {'support': -8, 'reputation': -15, 'funds': 5000}),
                Choice("Expel the member from the party",
                       {'support': 2, 'reputation': 5, 'funds': -5000}),
                Choice("Launch internal investigation",
                       {'support': -3, 'reputation': -5, 'funds': -8000})
            ]
        ))

        # Social movement
        events.append(Event(
            "Social Movement",
            "A large social movement is demanding policy changes.",
            [
                Choice("Support the movement",
                       {'support': 5, 'reputation': 8, 'funds': -3000}),
                Choice("Oppose the movement",
                       {'support': -4, 'reputation': -6, 'funds': 2000}),
                Choice("Remain neutral",
                       {'support': -1, 'reputation': -2})
            ]
        ))

        # International crisis
        events.append(Event(
            "International Crisis",
            "A neighboring country is in conflict. Should your party support intervention?",
            [
                Choice("Support military intervention",
                       {'support': -5, 'reputation': -8, 'funds': -15000}),
                Choice("Propose diplomatic solution",
                       {'support': 3, 'reputation': 10, 'funds': -5000}),
                Choice("Isolationist stance",
                       {'support': -2, 'reputation': -3, 'funds': 5000})
            ]
        ))

        # Education reform
        events.append(Event(
            "Education Reform Debate",
            "There's a heated debate about reforming the education system.",
            [
                Choice("Support increased education funding",
                       {'support': 4, 'reputation': 7, 'funds': -12000}),
                Choice("Privatize education",
                       {'support': -6, 'reputation': -5, 'funds': 8000}),
                Choice("Maintain status quo",
                       {'support': -2, 'reputation': -2})
            ]
        ))

        # Healthcare crisis
        events.append(Event(
            "Healthcare Crisis",
            "The healthcare system is overwhelmed. Action is needed!",
            [
                Choice("Expand public healthcare",
                       {'support': 6, 'reputation': 8, 'funds': -20000}),
                Choice("Encourage private healthcare",
                       {'support': -4, 'reputation': -3, 'funds': 10000}),
                Choice("Emergency measures only",
                       {'support': 1, 'reputation': 2, 'funds': -5000})
            ]
        ))

        # Donation opportunity
        events.append(Event(
            "Major Donor Offer",
            "A wealthy donor offers significant funding in exchange for policy influence.",
            [
                Choice("Accept the donation",
                       {'support': -3, 'reputation': -8, 'funds': 25000}),
                Choice("Refuse the donation",
                       {'support': 4, 'reputation': 10, 'funds': 0}),
                Choice("Negotiate conditions",
                       {'support': 0, 'reputation': 2, 'funds': 12000})
            ]
        ))

        # Environmental disaster
        events.append(Event(
            "Environmental Disaster",
            "A major environmental disaster has occurred in the region.",
            [
                Choice("Push for strict environmental laws",
                       {'support': 5, 'reputation': 12, 'funds': -15000}),
                Choice("Balance economy and environment",
                       {'support': 2, 'reputation': 4, 'funds': -8000}),
                Choice("Prioritize economic recovery",
                       {'support': -5, 'reputation': -10, 'funds': 5000})
            ]
        ))

        return events

    def get_random_event(self):
        """Get a random event"""
        if self.events:
            return random.choice(self.events)
        return None

    def apply_choice_effects(self, party, choice):
        """Apply the effects of a choice to the party"""
        for effect, value in choice.effects.items():
            if effect == 'support':
                party.adjust_support(value)
            elif effect == 'funds':
                party.adjust_funds(value)
            elif effect == 'reputation':
                party.adjust_reputation(value)
