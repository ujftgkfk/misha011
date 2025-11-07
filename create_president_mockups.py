#!/usr/bin/env python3
"""
Create visual mockups for This Is the President style game
"""
from PIL import Image, ImageDraw, ImageFont
import os

# Screen dimensions
WIDTH = 1200
HEIGHT = 800

# Colors - Presidential style
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
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
GOLD = (255, 215, 0)
CRIMSON = (139, 0, 0)
ORANGE = (255, 140, 0)

def draw_button(draw, x, y, width, height, text, color, text_color=WHITE):
    """Draw a button"""
    draw.rectangle([x, y, x + width, y + height], fill=color, outline=WHITE, width=2)
    try:
        font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 22)
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
    if fill_width > 0:
        draw.rectangle([x, y, x + fill_width, y + height], fill=color)

def create_main_menu():
    """Create presidential main menu"""
    img = Image.new('RGB', (WIDTH, HEIGHT), VERY_DARK_GRAY)
    draw = ImageDraw.Draw(img)

    try:
        title_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 68)
        subtitle_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 32)
    except:
        title_font = ImageFont.load_default()
        subtitle_font = ImageFont.load_default()

    # Title
    title_text = "THIS IS THE"
    bbox = draw.textbbox((0, 0), title_text, font=title_font)
    title_width = bbox[2] - bbox[0]
    draw.text((WIDTH // 2 - title_width // 2, 120), title_text, fill=WHITE, font=title_font)

    title2_text = "PRESIDENT"
    bbox2 = draw.textbbox((0, 0), title2_text, font=title_font)
    title2_width = bbox2[2] - bbox2[0]
    draw.text((WIDTH // 2 - title2_width // 2, 190), title2_text, fill=CRIMSON, font=title_font)

    # Subtitle
    subtitle = "Do whatever it takes to survive"
    bbox3 = draw.textbbox((0, 0), subtitle, font=subtitle_font)
    subtitle_width = bbox3[2] - bbox3[0]
    draw.text((WIDTH // 2 - subtitle_width // 2, 280), subtitle, fill=LIGHT_GRAY, font=subtitle_font)

    # Buttons
    draw_button(draw, 450, 370, 300, 60, "Start Presidency", DARK_RED)
    draw_button(draw, 450, 470, 300, 60, "Quit", DARK_GRAY)

    img.save('screenshots_president/1_menu_president.png')
    print("✓ Created presidential main menu")

def create_game_screen():
    """Create main game screen - Presidential dashboard"""
    img = Image.new('RGB', (WIDTH, HEIGHT), VERY_DARK_GRAY)
    draw = ImageDraw.Draw(img)

    try:
        title_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 38)
        label_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 22)
        small_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 18)
    except:
        title_font = ImageFont.load_default()
        label_font = ImageFont.load_default()
        small_font = ImageFont.load_default()

    # Title
    draw.text((50, 30), "Mr. President", fill=WHITE, font=title_font)

    # Date
    draw.text((50, 75), "Year 2, Week 15", fill=LIGHT_GRAY, font=label_font)
    draw.text((250, 78), "193 weeks until end of term", fill=YELLOW, font=small_font)

    # Stats
    y = 105
    draw.text((50, y), "Approval Rating: 48.3%", fill=WHITE, font=label_font)
    y += 20
    draw_progress_bar(draw, 50, y, 300, 25, 48.3, color=YELLOW)
    y += 45

    draw.text((50, y), "Political Influence: 65/100", fill=WHITE, font=label_font)
    y += 20
    draw_progress_bar(draw, 50, y, 300, 25, 65, color=PURPLE)
    y += 45

    draw.text((50, y), "Impeachment Risk: 32%", fill=YELLOW, font=label_font)
    y += 20
    draw_progress_bar(draw, 50, y, 300, 25, 32, color=ORANGE)
    y += 45

    draw.text((50, y), "Amendment Votes: 28/67", fill=WHITE, font=label_font)
    y += 20
    draw_progress_bar(draw, 50, y, 300, 25, 28, 67, color=GOLD)

    # Money
    draw.text((50, 350), "Slush Fund: $345,000", fill=GREEN, font=label_font)

    # Scandals
    draw.text((50, 390), "Active Scandals: 2", fill=RED, font=label_font)
    draw.text((50, 420), "Investigations: 1", fill=CRIMSON, font=label_font)

    # Goal
    try:
        goal_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 24)
    except:
        goal_font = ImageFont.load_default()
    draw.text((50, 470), "GOAL: Pass immunity amendment OR survive 4 years", fill=GOLD, font=goal_font)

    # Factions
    draw.text((700, 100), "Factions", fill=WHITE, font=title_font)

    factions = [
        ("Military: 72%", DARK_GREEN, 72),
        ("Oligarchs: 85%", GOLD, 85),
        ("Media: 45%", BLUE, 45),
        ("Congress: 58%", PURPLE, 58),
        ("Intelligence: 38%", DARK_GRAY, 38)
    ]

    fy = 150
    for fname, color, value in factions:
        draw.text((700, fy), fname, fill=color, font=label_font)
        draw_progress_bar(draw, 700, fy + 25, 200, 15, value, color=color)
        fy += 60

    # Action buttons
    draw_button(draw, 50, 550, 180, 50, "Bribe Congress", CRIMSON)
    draw_button(draw, 250, 550, 180, 50, "Propaganda", DARK_RED)
    draw_button(draw, 450, 550, 180, 50, "Cover-Up", DARK_GRAY)
    draw_button(draw, 650, 550, 180, 50, "Public Speech", BLUE)
    draw_button(draw, 850, 550, 180, 50, "Exec. Order", PURPLE)

    draw_button(draw, 950, 700, 200, 60, "Next Week", DARK_GREEN)

    # Info text
    info = [
        "Bribe Congress: $100K, -10 influence → +votes",
        "Propaganda: $50K, +5 influence → +approval",
        "Cover-Up: $75K, -5 influence → remove scandal",
        "Public Speech: $10K → +2-5% approval",
        "Executive Order: 15 influence → mixed results"
    ]

    iy = 620
    for text in info:
        draw.text((50, iy), text, fill=LIGHT_GRAY, font=small_font)
        iy += 20

    img.save('screenshots_president/2_game_screen.png')
    print("✓ Created game screen")

def create_event_screen():
    """Create event screen - dark and cynical"""
    img = Image.new('RGB', (WIDTH, HEIGHT), VERY_DARK_GRAY)
    draw = ImageDraw.Draw(img)

    try:
        title_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 48)
        desc_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 20)
        small_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 16)
    except:
        title_font = ImageFont.load_default()
        desc_font = ImageFont.load_default()
        small_font = ImageFont.load_default()

    # Title
    title_text = "FBI Investigation"
    bbox = draw.textbbox((0, 0), title_text, font=title_font)
    title_width = bbox[2] - bbox[0]
    draw.text((WIDTH // 2 - title_width // 2, 80), title_text, fill=RED, font=title_font)

    # Threat level
    threat_text = "Threat Level: ███░░"
    bbox2 = draw.textbbox((0, 0), threat_text, font=small_font)
    threat_width = bbox2[2] - bbox2[0]
    draw.text((WIDTH // 2 - threat_width // 2, 145), threat_text, fill=RED, font=small_font)

    # Description box
    draw.rectangle([150, 180, 1050, 330], fill=DARK_GRAY, outline=BLACK, width=2)
    desc_lines = [
        "The FBI has opened an investigation into your pre-election",
        "business dealings. Your Attorney General can shut it down,",
        "but it will look suspicious."
    ]
    dy = 200
    for line in desc_lines:
        draw.text((170, dy), line, fill=WHITE, font=desc_font)
        dy += 35

    # Choices
    choices = [
        ("Order Attorney General to close the investigation", "impeachment_risk: -15, approval: -8, influence: -10"),
        ("Let the investigation continue", "impeachment_risk: +25, approval: +5, money: -50000"),
        ("Bribe the FBI Director", "money: -150000, impeachment_risk: -20, influence: +5")
    ]

    y = 360
    for i, (choice_text, effects) in enumerate(choices):
        color = CRIMSON if i == 0 else DARK_RED
        draw_button(draw, 200, y, 800, 65, choice_text, color)
        draw.text((220, y + 70), effects, fill=LIGHT_GRAY, font=small_font)
        y += 110

    img.save('screenshots_president/3_event_fbi.png')
    print("✓ Created FBI investigation event")

def create_scandal_event():
    """Create scandal event"""
    img = Image.new('RGB', (WIDTH, HEIGHT), VERY_DARK_GRAY)
    draw = ImageDraw.Draw(img)

    try:
        title_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 48)
        desc_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 20)
        small_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 16)
    except:
        title_font = ImageFont.load_default()
        desc_font = ImageFont.load_default()
        small_font = ImageFont.load_default()

    # Title
    title_text = "Whistleblower Threat"
    bbox = draw.textbbox((0, 0), title_text, font=title_font)
    title_width = bbox[2] - bbox[0]
    draw.text((WIDTH // 2 - title_width // 2, 80), title_text, fill=ORANGE, font=title_font)

    # Threat level
    threat_text = "Threat Level: ████░"
    bbox2 = draw.textbbox((0, 0), threat_text, font=small_font)
    threat_width = bbox2[2] - bbox2[0]
    draw.text((WIDTH // 2 - threat_width // 2, 145), threat_text, fill=ORANGE, font=small_font)

    # Description box
    draw.rectangle([150, 180, 1050, 330], fill=DARK_GRAY, outline=BLACK, width=2)
    desc_lines = [
        "A former aide threatens to go public with evidence of your",
        "corruption. They want money to stay quiet."
    ]
    dy = 220
    for line in desc_lines:
        draw.text((170, dy), line, fill=WHITE, font=desc_font)
        dy += 35

    # Choices
    choices = [
        ("Pay them off ($200,000)", "money: -200000, impeachment_risk: -10"),
        ("Threaten them into silence", "impeachment_risk: +15, influence: -15, approval: -5"),
        ("Have them 'discredited' by media", "money: -80000, influence: -10, approval: -3")
    ]

    y = 360
    for i, (choice_text, effects) in enumerate(choices):
        color = CRIMSON if i == 0 else DARK_RED
        draw_button(draw, 200, y, 800, 65, choice_text, color)
        draw.text((220, y + 70), effects, fill=LIGHT_GRAY, font=small_font)
        y += 110

    img.save('screenshots_president/4_event_whistleblower.png')
    print("✓ Created whistleblower event")

def create_victory_screen():
    """Create victory screen"""
    img = Image.new('RGB', (WIDTH, HEIGHT), VERY_DARK_GRAY)
    draw = ImageDraw.Draw(img)

    try:
        title_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 68)
        text_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 28)
    except:
        title_font = ImageFont.load_default()
        text_font = ImageFont.load_default()

    # Title
    title_text = "IMMUNITY SECURED"
    bbox = draw.textbbox((0, 0), title_text, font=title_font)
    title_width = bbox[2] - bbox[0]
    draw.text((WIDTH // 2 - title_width // 2, 180), title_text, fill=GOLD, font=title_font)

    # Subtitle
    subtitle = "You passed the amendment. You're untouchable now."
    bbox2 = draw.textbbox((0, 0), subtitle, font=text_font)
    subtitle_width = bbox2[2] - bbox2[0]
    draw.text((WIDTH // 2 - subtitle_width // 2, 280), subtitle, fill=WHITE, font=text_font)

    # Stats
    stats = [
        "Final Approval: 52.3%",
        "Money Remaining: $125,000",
        "Amendment Votes: 67/67",
        "Years Served: 4",
        "Scandals: 3"
    ]

    y = 380
    for stat in stats:
        bbox3 = draw.textbbox((0, 0), stat, font=text_font)
        stat_width = bbox3[2] - bbox3[0]
        draw.text((WIDTH // 2 - stat_width // 2, y), stat, fill=LIGHT_GRAY, font=text_font)
        y += 45

    # Button
    draw_button(draw, 450, 650, 300, 60, "Return to Menu", DARK_GRAY)

    img.save('screenshots_president/5_victory.png')
    print("✓ Created victory screen")

def create_impeached_screen():
    """Create defeat screen"""
    img = Image.new('RGB', (WIDTH, HEIGHT), VERY_DARK_GRAY)
    draw = ImageDraw.Draw(img)

    try:
        title_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 68)
        text_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 28)
    except:
        title_font = ImageFont.load_default()
        text_font = ImageFont.load_default()

    # Title
    title_text = "IMPEACHED"
    bbox = draw.textbbox((0, 0), title_text, font=title_font)
    title_width = bbox[2] - bbox[0]
    draw.text((WIDTH // 2 - title_width // 2, 180), title_text, fill=CRIMSON, font=title_font)

    # Subtitle
    subtitle = "Congress voted you out. Prison awaits."
    bbox2 = draw.textbbox((0, 0), subtitle, font=text_font)
    subtitle_width = bbox2[2] - bbox2[0]
    draw.text((WIDTH // 2 - subtitle_width // 2, 280), subtitle, fill=WHITE, font=text_font)

    # Stats
    stats = [
        "Final Approval: 18.5%",
        "Money Remaining: $-45,000",
        "Amendment Votes: 31/67",
        "Years Served: 2",
        "Scandals: 8"
    ]

    y = 380
    for stat in stats:
        bbox3 = draw.textbbox((0, 0), stat, font=text_font)
        stat_width = bbox3[2] - bbox3[0]
        draw.text((WIDTH // 2 - stat_width // 2, y), stat, fill=LIGHT_GRAY, font=text_font)
        y += 45

    # Button
    draw_button(draw, 450, 650, 300, 60, "Return to Menu", DARK_GRAY)

    img.save('screenshots_president/6_impeached.png')
    print("✓ Created impeachment screen")

# Create screenshots directory
os.makedirs('screenshots_president', exist_ok=True)

# Create all mockups
print("Creating THIS IS THE PRESIDENT screenshots...")
print()
create_main_menu()
create_game_screen()
create_event_screen()
create_scandal_event()
create_victory_screen()
create_impeached_screen()

print()
print("✅ All presidential screenshots created in 'screenshots_president/' directory!")
print()
print("Presidential game features:")
print("  • Dark, cynical tone")
print("  • Moral dilemmas")
print("  • Corruption mechanics")
print("  • Impeachment risk")
print("  • Faction management")
print("  • Amendment system")
