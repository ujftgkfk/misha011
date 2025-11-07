"""
Game constants and configuration - This Is the President style
"""

# Screen settings
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 800
FPS = 60

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (128, 128, 128)
LIGHT_GRAY = (200, 200, 200)
DARK_GRAY = (40, 40, 45)
VERY_DARK_GRAY = (25, 25, 30)
RED = (200, 50, 50)
DARK_RED = (150, 30, 30)
GREEN = (50, 180, 50)
DARK_GREEN = (30, 120, 30)
BLUE = (50, 100, 200)
YELLOW = (220, 200, 50)
PURPLE = (150, 50, 150)
ORANGE = (255, 140, 0)
GOLD = (255, 215, 0)
CRIMSON = (139, 0, 0)

# Game settings
STARTING_MONEY = 500000  # Slush fund
STARTING_INFLUENCE = 50
STARTING_APPROVAL = 55.0
TOTAL_WEEKS = 208  # 4 years = 208 weeks
AMENDMENT_REQUIRED_VOTES = 67  # 67% of Congress

# Resources
RESOURCE_MONEY = "money"
RESOURCE_INFLUENCE = "influence"
RESOURCE_APPROVAL = "approval"

# Factions
FACTIONS = {
    'military': {
        'name': 'Military',
        'color': DARK_GREEN,
        'description': 'Armed Forces and Defense Department'
    },
    'oligarchs': {
        'name': 'Oligarchs',
        'color': GOLD,
        'description': 'Wealthy business magnates'
    },
    'media': {
        'name': 'Media',
        'color': BLUE,
        'description': 'Press and broadcasting networks'
    },
    'congress': {
        'name': 'Congress',
        'color': PURPLE,
        'description': 'Senate and House members'
    },
    'intelligence': {
        'name': 'Intelligence',
        'color': DARK_GRAY,
        'description': 'CIA, FBI, NSA agencies'
    }
}

# Cabinet positions
CABINET_POSITIONS = [
    'Chief of Staff',
    'Attorney General',
    'Press Secretary',
    'Security Advisor',
    'Treasury Secretary'
]

# Threat levels
THREAT_IMPEACHMENT = 'impeachment'
THREAT_INVESTIGATION = 'investigation'
THREAT_SCANDAL = 'scandal'
THREAT_PROTEST = 'protest'

# Game objectives
OBJECTIVE_AMENDMENT = 'amendment'  # Pass constitutional amendment for immunity
OBJECTIVE_SURVIVAL = 'survival'    # Survive 4 years without impeachment

# Difficulty
DIFFICULTY = {
    'easy': {
        'money_mult': 1.5,
        'approval_mult': 1.2,
        'threat_mult': 0.8
    },
    'normal': {
        'money_mult': 1.0,
        'approval_mult': 1.0,
        'threat_mult': 1.0
    },
    'hard': {
        'money_mult': 0.7,
        'approval_mult': 0.8,
        'threat_mult': 1.3
    }
}

# Action costs
ACTION_COSTS = {
    'bribe_congress': {'money': 100000, 'influence': -10},
    'propaganda': {'money': 50000, 'influence': 5},
    'cover_up': {'money': 75000, 'influence': -5},
    'executive_order': {'influence': 15, 'approval': -3},
    'public_speech': {'money': 10000, 'approval': 2},
    'backroom_deal': {'money': 80000, 'influence': 10},
    'dismiss_official': {'influence': 20, 'approval': -5}
}
