"""
Event system for Presidential decisions - This Is the President style
Darker, more cynical events with moral dilemmas
"""
import random


class Event:
    """Represents a game event with choices"""

    def __init__(self, title, description, choices, threat_level=0):
        self.title = title
        self.description = description
        self.choices = choices  # List of Choice objects
        self.threat_level = threat_level  # How dangerous this event is


class Choice:
    """Represents a choice in an event"""

    def __init__(self, text, effects, consequence_text=""):
        self.text = text
        self.effects = effects  # Dict: {'money': -50000, 'approval': +5, 'impeachment_risk': +10}
        self.consequence_text = consequence_text


class EventManager:
    """Manages darker, more cynical presidential events"""

    def __init__(self):
        self.events = self._create_events()
        self.current_event = None

    def _create_events(self):
        """Create all possible events - This Is the President style"""
        events = []

        # FBI Investigation
        events.append(Event(
            "FBI Investigation",
            "The FBI has opened an investigation into your pre-election business dealings. "
            "Your Attorney General can shut it down, but it will look suspicious.",
            [
                Choice("Order Attorney General to close the investigation",
                       {'impeachment_risk': -15, 'approval': -8, 'influence': -10},
                       "Investigation closed. Media outcry follows."),
                Choice("Let the investigation continue",
                       {'impeachment_risk': 25, 'approval': 5, 'money': -50000},
                       "Investigation proceeds. You'll need good lawyers."),
                Choice("Bribe the FBI Director",
                       {'money': -150000, 'impeachment_risk': -20, 'influence': 5},
                       "Director becomes 'cooperative'. Very risky.")
            ],
            threat_level=3
        ))

        # Whistleblower
        events.append(Event(
            "Whistleblower Threat",
            "A former aide threatens to go public with evidence of your corruption. "
            "They want money to stay quiet.",
            [
                Choice("Pay them off ($200,000)",
                       {'money': -200000, 'impeachment_risk': -10},
                       "Problem solved... for now."),
                Choice("Threaten them into silence",
                       {'impeachment_risk': 15, 'influence': -15, 'approval': -5},
                       "They back down, but might talk later."),
                Choice("Have them 'discredited' by your media allies",
                       {'money': -80000, 'influence': -10, 'approval': -3},
                       "Character assassination successful.")
            ],
            threat_level=4
        ))

        # Mass Protest
        events.append(Event(
            "Mass Protests",
            "Tens of thousands are protesting your policies outside the White House. "
            "The situation is escalating.",
            [
                Choice("Order police to disperse them with force",
                       {'approval': -15, 'influence': 10, 'impeachment_risk': 10},
                       "Protests crushed. International condemnation."),
                Choice("Negotiate with protest leaders",
                       {'approval': 5, 'influence': -5, 'money': -30000},
                       "Protests end peacefully. You look weak."),
                Choice("Ignore them completely",
                       {'approval': -8, 'impeachment_risk': 5},
                       "Protests continue for weeks.")
            ],
            threat_level=2
        ))

        # Corporate Bribe Offer
        events.append(Event(
            "Corporate Favor",
            "A major corporation offers $500,000 for your campaign fund in exchange for "
            "blocking new environmental regulations.",
            [
                Choice("Accept the money",
                       {'money': 500000, 'approval': -10, 'impeachment_risk': 15},
                       "Money received. Environmental groups furious."),
                Choice("Refuse and implement the regulations",
                       {'approval': 8, 'influence': -10, 'money': -50000},
                       "Corporations become hostile."),
                Choice("Take the money and implement watered-down regulations",
                       {'money': 300000, 'approval': -5, 'influence': 5},
                       "Everyone somewhat unhappy.")
            ],
            threat_level=2
        ))

        # Scandal Cover-Up
        events.append(Event(
            "Affair Scandal",
            "Photos of you with your mistress are about to be published by a tabloid. "
            "Your Press Secretary has options.",
            [
                Choice("Buy the photos and bury the story",
                       {'money': -250000, 'impeachment_risk': -5},
                       "Story killed. Publisher 'convinced'."),
                Choice("Admit everything and apologize publicly",
                       {'approval': -20, 'influence': -15, 'impeachment_risk': 5},
                       "Honesty... admirable but costly."),
                Choice("Deny everything and attack the tabloid",
                       {'approval': -12, 'influence': -8, 'impeachment_risk': 10},
                       "Media war begins. Truth unclear.")
            ],
            threat_level=3
        ))

        # Military Coup Hint
        events.append(Event(
            "Military Concerns",
            "Your Security Advisor reports that some generals are 'concerned' about "
            "your fitness for office. This could be serious.",
            [
                Choice("Fire the disloyal generals immediately",
                       {'influence': -20, 'approval': -10, 'impeachment_risk': 15},
                       "Loyalty restored, but military angry."),
                Choice("Meet with them privately and make concessions",
                       {'money': -100000, 'influence': 10, 'approval': -5},
                       "Peace maintained. You owe them now."),
                Choice("Increase military budget significantly",
                       {'money': -200000, 'influence': 15, 'approval': -8},
                       "Generals happy. Treasury empty.")
            ],
            threat_level=5
        ))

        # Foreign Dirt
        events.append(Event(
            "Foreign Intelligence Offer",
            "A foreign intelligence service offers compromising information about your "
            "political rivals. They want favors in return.",
            [
                Choice("Accept the information",
                       {'impeachment_risk': 20, 'influence': 15, 'approval': -5},
                       "Powerful leverage gained. Very illegal."),
                Choice("Report this to the FBI",
                       {'approval': 10, 'influence': -10, 'impeachment_risk': -5},
                       "You do the right thing. Rivals survive."),
                Choice("Decline but stay in contact",
                       {'influence': 5, 'impeachment_risk': 5},
                       "Door left open for future 'cooperation'.")
            ],
            threat_level=4
        ))

        # Supreme Court Justice
        events.append(Event(
            "Supreme Court Vacancy",
            "A Supreme Court Justice died. You can nominate a loyalist who might "
            "protect you from prosecution, or a qualified moderate.",
            [
                Choice("Nominate your personal lawyer",
                       {'influence': 20, 'approval': -15, 'impeachment_risk': -20},
                       "Insurance policy installed."),
                Choice("Nominate a moderate",
                       {'approval': 8, 'influence': -5},
                       "Bipartisan approval. No special protection."),
                Choice("Nominate an extremist to energize your base",
                       {'approval': -10, 'influence': 10, 'impeachment_risk': 10},
                       "Base loves it. Everyone else horrified.")
            ],
            threat_level=1
        ))

        # Tax Returns Leak
        events.append(Event(
            "Tax Return Leak",
            "Someone leaked your tax returns showing massive tax avoidance schemes. "
            "The media is having a field day.",
            [
                Choice("Claim it's all legal (it probably is)",
                       {'approval': -12, 'impeachment_risk': 8},
                       "Legal, but looks terrible."),
                Choice("Attack the leaker, ignore the content",
                       {'approval': -15, 'influence': -10},
                       "Distraction successful. Anger remains."),
                Choice("Promise tax reform that benefits everyone",
                       {'approval': -5, 'money': -100000, 'influence': 5},
                       "Empty promise buys time.")
            ],
            threat_level=2
        ))

        # Pardon Request
        events.append(Event(
            "Pardon Request",
            "Your former campaign manager, now in prison for fraud, wants a pardon. "
            "He knows where all the bodies are buried.",
            [
                Choice("Grant the pardon immediately",
                       {'impeachment_risk': 15, 'influence': 10, 'approval': -12},
                       "He's free and grateful. Obstruction of justice?"),
                Choice("Refuse the pardon",
                       {'impeachment_risk': 25, 'influence': -15},
                       "He might start talking to prosecutors."),
                Choice("Delay and string him along",
                       {'impeachment_risk': 10, 'influence': 5},
                       "Buy time. He's still hopeful.")
            ],
            threat_level=4
        ))

        # Election Interference
        events.append(Event(
            "Election Integrity",
            "Your party has an opportunity to manipulate voting districts for the "
            "upcoming midterms. It's technically legal but deeply unethical.",
            [
                Choice("Gerrymander aggressively",
                       {'influence': 20, 'approval': -15, 'impeachment_risk': 5},
                       "Your party secure for a decade."),
                Choice("Gerrymander moderately",
                       {'influence': 10, 'approval': -8},
                       "Some advantage gained."),
                Choice("Refuse to manipulate districts",
                       {'approval': 5, 'influence': -15},
                       "Fair elections. You might lose control.")
            ],
            threat_level=2
        ))

        # Cabinet Loyalty Test
        events.append(Event(
            "Cabinet Loyalty Crisis",
            "Your Chief of Staff is allegedly writing a tell-all book about your "
            "administration's dysfunction. Fire them or tolerate it?",
            [
                Choice("Fire them immediately",
                       {'influence': -10, 'approval': -8, 'impeachment_risk': 10},
                       "They'll go on a media tour."),
                Choice("Threaten legal action",
                       {'money': -50000, 'influence': -5, 'approval': -5},
                       "Tied up in court for months."),
                Choice("Offer them money to cancel the book",
                       {'money': -150000, 'impeachment_risk': -5},
                       "Book cancelled. Other staffers watching.")
            ],
            threat_level=3
        ))

        return events

    def get_random_event(self):
        """Get a random event"""
        if self.events:
            return random.choice(self.events)
        return None

    def apply_choice_effects(self, president, choice):
        """Apply the effects of a choice to the president"""
        for effect, value in choice.effects.items():
            if effect == 'money':
                president.adjust_money(value)
            elif effect == 'approval':
                president.adjust_approval(value)
            elif effect == 'influence':
                president.adjust_influence(value)
            elif effect == 'impeachment_risk':
                president.adjust_impeachment_risk(value)
            elif effect == 'amendment_votes':
                president.amendment_votes = max(0, min(100, president.amendment_votes + value))
