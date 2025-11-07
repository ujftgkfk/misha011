"""
Save and load game functionality
"""
import json
import os
from datetime import datetime


class SaveSystem:
    """Handles saving and loading game state"""

    def __init__(self):
        self.save_dir = "saves"
        if not os.path.exists(self.save_dir):
            os.makedirs(self.save_dir)

    def save_game(self, game, save_name=None):
        """Save current game state"""
        if save_name is None:
            save_name = f"save_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"

        save_data = {
            'turn': game.turn,
            'year': game.year,
            'quarter': game.quarter,
            'player_party': {
                'name': game.player_party.name,
                'ideology': game.player_party.ideology,
                'funds': game.player_party.funds,
                'support': game.player_party.support,
                'reputation': game.player_party.reputation,
                'seats': game.player_party.seats,
                'is_in_power': game.player_party.is_in_power,
                'policies': game.player_party.policies
            },
            'ai_parties': [
                {
                    'name': ai.name,
                    'ideology': ai.ideology,
                    'funds': ai.funds,
                    'support': ai.support,
                    'reputation': ai.reputation,
                    'seats': ai.seats,
                    'is_in_power': ai.is_in_power,
                    'aggressiveness': ai.aggressiveness
                }
                for ai in game.ai_parties
            ]
        }

        save_path = os.path.join(self.save_dir, save_name)

        try:
            with open(save_path, 'w') as f:
                json.dump(save_data, f, indent=2)
            return True, save_path
        except Exception as e:
            return False, str(e)

    def load_game(self, save_name):
        """Load game state from file"""
        save_path = os.path.join(self.save_dir, save_name)

        try:
            with open(save_path, 'r') as f:
                save_data = json.load(f)
            return True, save_data
        except Exception as e:
            return False, str(e)

    def list_saves(self):
        """List all available save files"""
        if not os.path.exists(self.save_dir):
            return []

        saves = []
        for filename in os.listdir(self.save_dir):
            if filename.endswith('.json'):
                filepath = os.path.join(self.save_dir, filename)
                mtime = os.path.getmtime(filepath)
                saves.append({
                    'filename': filename,
                    'modified': datetime.fromtimestamp(mtime).strftime('%Y-%m-%d %H:%M:%S')
                })

        return sorted(saves, key=lambda x: x['modified'], reverse=True)

    def apply_save_data(self, game, save_data):
        """Apply loaded save data to game"""
        from src.core.party import Party, AIParty

        game.turn = save_data['turn']
        game.year = save_data['year']
        game.quarter = save_data['quarter']

        # Restore player party
        pp = save_data['player_party']
        game.player_party = Party(pp['name'], pp['ideology'], pp['funds'], pp['support'])
        game.player_party.reputation = pp['reputation']
        game.player_party.seats = pp['seats']
        game.player_party.is_in_power = pp['is_in_power']
        game.player_party.policies = pp['policies']

        # Restore AI parties
        game.ai_parties = []
        for ai_data in save_data['ai_parties']:
            ai = AIParty(ai_data['name'], ai_data['ideology'], ai_data['funds'], ai_data['support'])
            ai.reputation = ai_data['reputation']
            ai.seats = ai_data['seats']
            ai.is_in_power = ai_data['is_in_power']
            ai.aggressiveness = ai_data['aggressiveness']
            game.ai_parties.append(ai)
