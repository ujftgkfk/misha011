#!/usr/bin/env python3
"""
Create visual mockups of the game screens
"""
from PIL import Image, ImageDraw, ImageFont
import os

# Screen dimensions
WIDTH = 1200
HEIGHT = 800

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

def draw_button(draw, x, y, width, height, text, color, text_color=WHITE):
    """Draw a button"""
    draw.rectangle([x, y, x + width, y + height], fill=color, outline=WHITE, width=2)
    try:
        font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 24)
    except:
        font = ImageFont.load_default()

    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    text_x = x + (width - text_width) // 2
    text_y = y + (height - text_height) // 2
    draw.text((text_x, text_y), text, fill=text_color, font=font)

def draw_progress_bar(draw, x, y, width, height, value, max_value=100, color=GREEN):
    """Draw a progress bar"""
    # Background
    draw.rectangle([x, y, x + width, y + height], fill=DARK_GRAY, outline=WHITE, width=2)
    # Fill
    fill_width = int((value / max_value) * width)
    draw.rectangle([x, y, x + fill_width, y + height], fill=color)

def create_main_menu():
    """Create main menu mockup"""
    img = Image.new('RGB', (WIDTH, HEIGHT), DARK_GRAY)
    draw = ImageDraw.Draw(img)

    # Title
    try:
        title_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 60)
    except:
        title_font = ImageFont.load_default()

    title_text = "Political Strategy"
    bbox = draw.textbbox((0, 0), title_text, font=title_font)
    title_width = bbox[2] - bbox[0]
    draw.text((WIDTH // 2 - title_width // 2, 150), title_text, fill=WHITE, font=title_font)

    # Buttons
    draw_button(draw, 450, 300, 300, 60, "New Game", GREEN)
    draw_button(draw, 450, 400, 300, 60, "Quit", RED)

    img.save('screenshots/1_main_menu.png')
    print("✓ Created main menu screenshot")

def create_party_selection():
    """Create party selection mockup"""
    img = Image.new('RGB', (WIDTH, HEIGHT), DARK_GRAY)
    draw = ImageDraw.Draw(img)

    try:
        title_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 40)
        label_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 28)
    except:
        title_font = ImageFont.load_default()
        label_font = ImageFont.load_default()

    # Title
    title_text = "Create Your Party"
    bbox = draw.textbbox((0, 0), title_text, font=title_font)
    title_width = bbox[2] - bbox[0]
    draw.text((WIDTH // 2 - title_width // 2, 100), title_text, fill=WHITE, font=title_font)

    # Label
    draw.text((200, 200), "Choose Ideology:", fill=WHITE, font=label_font)

    # Ideology buttons
    ideologies = [
        ("Liberal", BLUE),
        ("Conservative", RED),
        ("Progressive", GREEN),
        ("Centrist", PURPLE),
        ("Nationalist", ORANGE)
    ]

    y = 250
    for name, color in ideologies:
        draw_button(draw, 200, y, 300, 50, name, color)
        y += 70

    # Highlight selected (Liberal)
    draw.rectangle([200, 250, 500, 300], outline=YELLOW, width=4)

    # Start and Back buttons
    draw_button(draw, 450, 600, 300, 60, "Start Game", GREEN)
    draw_button(draw, 450, 680, 300, 60, "Back", GRAY)

    img.save('screenshots/2_party_selection.png')
    print("✓ Created party selection screenshot")

def create_game_screen():
    """Create main game screen mockup"""
    img = Image.new('RGB', (WIDTH, HEIGHT), DARK_GRAY)
    draw = ImageDraw.Draw(img)

    try:
        title_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 40)
        normal_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 24)
        small_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 18)
    except:
        title_font = ImageFont.load_default()
        normal_font = ImageFont.load_default()
        small_font = ImageFont.load_default()

    # Party name and ideology
    draw.text((50, 50), "Freedom Party - Liberal", fill=WHITE, font=title_font)

    # Date
    draw.text((50, 100), "Q2 2024 - Turn 6", fill=WHITE, font=normal_font)

    # Stats
    draw.text((50, 140), "Public Support: 32.5%", fill=WHITE, font=normal_font)
    draw_progress_bar(draw, 50, 170, 300, 30, 32.5, color=GREEN)

    draw.text((50, 220), "Reputation: 65/100", fill=WHITE, font=normal_font)
    draw_progress_bar(draw, 50, 250, 300, 30, 65, color=GREEN)

    draw.text((50, 300), "Funds: $87,500", fill=GREEN, font=normal_font)
    draw.text((50, 340), "Parliament Seats: 28/100", fill=WHITE, font=normal_font)
    draw.text((50, 380), "IN POWER", fill=GREEN, font=normal_font)

    # AI Parties
    draw.text((700, 150), "Other Parties:", fill=WHITE, font=title_font)

    ai_parties = [
        ("People's Alliance: 25.3% (22 seats)", BLUE),
        ("National Front: 21.8% (19 seats)", RED),
        ("Progressive Unity: 18.2% (15 seats)", GREEN),
        ("Centrist Coalition: 19.5% (16 seats)", PURPLE)
    ]

    y = 220
    for text, color in ai_parties:
        draw.text((700, y), text, fill=color, font=normal_font)
        y += 40

    # Action buttons
    draw_button(draw, 50, 600, 200, 50, "Campaign", BLUE)
    draw_button(draw, 270, 600, 200, 50, "Policy", GREEN)
    draw_button(draw, 490, 600, 200, 50, "Fundraise", YELLOW, BLACK)
    draw_button(draw, 950, 600, 200, 50, "End Turn", PURPLE)

    # Info text
    info = [
        "Campaign: Spend $15,000 to gain support",
        "Policy: Spend $5,000 to propose policy",
        "Fundraise: Raise money for your party",
        "Next Election: Turn 16"
    ]

    y = 680
    for text in info:
        draw.text((50, y), text, fill=LIGHT_GRAY, font=small_font)
        y += 25

    img.save('screenshots/3_game_screen.png')
    print("✓ Created game screen screenshot")

def create_event_screen():
    """Create event screen mockup"""
    img = Image.new('RGB', (WIDTH, HEIGHT), DARK_GRAY)
    draw = ImageDraw.Draw(img)

    try:
        title_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 48)
        normal_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 20)
        small_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 16)
    except:
        title_font = ImageFont.load_default()
        normal_font = ImageFont.load_default()
        small_font = ImageFont.load_default()

    # Title
    title_text = "Economic Crisis"
    bbox = draw.textbbox((0, 0), title_text, font=title_font)
    title_width = bbox[2] - bbox[0]
    draw.text((WIDTH // 2 - title_width // 2, 100), title_text, fill=YELLOW, font=title_font)

    # Description box
    draw.rectangle([200, 200, 1000, 350], fill=LIGHT_GRAY, outline=BLACK, width=2)
    desc_text = "The country is facing an economic downturn.\nHow should your party respond?"
    draw.text((220, 220), desc_text, fill=BLACK, font=normal_font)

    # Choices
    choices = [
        ("Propose tax cuts for businesses", "support: -2, funds: +5000, reputation: -5"),
        ("Increase social spending", "support: +3, funds: -10000, reputation: +5"),
        ("Take no action", "support: -5, reputation: -3")
    ]

    y = 400
    for choice_text, effects in choices:
        draw_button(draw, 300, y, 600, 60, choice_text, BLUE)
        draw.text((320, y + 65), effects, fill=LIGHT_GRAY, font=small_font)
        y += 100

    img.save('screenshots/4_event_screen.png')
    print("✓ Created event screen screenshot")

def create_election_screen():
    """Create election results mockup"""
    img = Image.new('RGB', (WIDTH, HEIGHT), DARK_GRAY)
    draw = ImageDraw.Draw(img)

    try:
        title_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 56)
        result_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 28)
        winner_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 40)
    except:
        title_font = ImageFont.load_default()
        result_font = ImageFont.load_default()
        winner_font = ImageFont.load_default()

    # Title
    title_text = "ELECTION RESULTS"
    bbox = draw.textbbox((0, 0), title_text, font=title_font)
    title_width = bbox[2] - bbox[0]
    draw.text((WIDTH // 2 - title_width // 2, 50), title_text, fill=WHITE, font=title_font)

    # Results
    results = [
        ("Freedom Party: 34.2% - 38 seats", GREEN, True),
        ("People's Alliance: 23.8% - 26 seats", BLUE, False),
        ("National Front: 19.5% - 21 seats", RED, False),
        ("Progressive Unity: 12.3% - 13 seats", GREEN, False),
        ("Centrist Coalition: 10.2% - 2 seats", PURPLE, False)
    ]

    y = 200
    for text, color, is_winner in results:
        draw.text((300, y), text, fill=color if is_winner else WHITE, font=result_font)
        if is_winner:
            # Draw star or highlight
            draw.text((250, y), "★", fill=YELLOW, font=result_font)
        y += 60

    # Winner announcement
    winner_text = "YOU WON THE ELECTION!"
    bbox = draw.textbbox((0, 0), winner_text, font=winner_font)
    winner_width = bbox[2] - bbox[0]
    draw.text((WIDTH // 2 - winner_width // 2, 500), winner_text, fill=GREEN, font=winner_font)

    # Continue button
    draw_button(draw, 450, 650, 300, 60, "Continue", GREEN)

    img.save('screenshots/5_election_results.png')
    print("✓ Created election results screenshot")

# Create screenshots directory
os.makedirs('screenshots', exist_ok=True)

# Create all mockups
print("Creating game screenshots...")
create_main_menu()
create_party_selection()
create_game_screen()
create_event_screen()
create_election_screen()

print("\n✅ All screenshots created in 'screenshots/' directory!")
