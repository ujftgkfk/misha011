"""
Election system for the game
"""
import random


class Election:
    """Handles election mechanics"""

    def __init__(self):
        self.results = {}

    def calculate_results(self, player_party, ai_parties):
        """Calculate election results based on support levels"""
        total_support = player_party.support
        party_supports = {player_party.name: player_party.support}

        for ai_party in ai_parties:
            total_support += ai_party.support
            party_supports[ai_party.name] = ai_party.support

        # Normalize to 100% and add some randomness
        results = {}
        random_factor = random.uniform(-3, 3)

        for party_name, support in party_supports.items():
            normalized = (support / total_support) * 100 if total_support > 0 else 0
            results[party_name] = max(0, min(100, normalized + random_factor))

        # Calculate seats (assuming 100 seats in parliament)
        total_votes = sum(results.values())
        seats = {}

        for party_name, votes in results.items():
            seats[party_name] = int((votes / total_votes) * 100) if total_votes > 0 else 0

        self.results = {
            'votes': results,
            'seats': seats
        }

        return self.results

    def determine_winner(self, results):
        """Determine which party won the election"""
        seats = results['seats']
        max_seats = max(seats.values()) if seats else 0
        winners = [party for party, count in seats.items() if count == max_seats]

        return winners[0] if winners else None
