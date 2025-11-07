"""
Game constants and configuration
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
DARK_GRAY = (64, 64, 64)
RED = (220, 50, 50)
GREEN = (50, 220, 50)
BLUE = (50, 50, 220)
YELLOW = (220, 220, 50)
PURPLE = (180, 50, 180)
ORANGE = (255, 140, 0)

# Game settings
STARTING_FUNDS = 100000
STARTING_SUPPORT = 15.0
TURNS_PER_YEAR = 4
ELECTION_TURN = 16  # Election every 4 years

# Political ideologies
IDEOLOGIES = {
    'liberal': {'name': 'Liberal', 'color': BLUE},
    'conservative': {'name': 'Conservative', 'color': RED},
    'progressive': {'name': 'Progressive', 'color': GREEN},
    'centrist': {'name': 'Centrist', 'color': PURPLE},
    'nationalist': {'name': 'Nationalist', 'color': ORANGE}
}

# Game difficulty
DIFFICULTY = {
    'easy': {'funds_multiplier': 1.5, 'support_multiplier': 1.3},
    'normal': {'funds_multiplier': 1.0, 'support_multiplier': 1.0},
    'hard': {'funds_multiplier': 0.7, 'support_multiplier': 0.8}
}
