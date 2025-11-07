#!/usr/bin/env python3
from PIL import Image, ImageDraw, ImageFont
import os

WIDTH = 1200
HEIGHT = 800

WHITE = (255, 255, 255)
LIGHT_GRAY = (200, 200, 200)
DARK_GRAY = (40, 40, 45)
VERY_DARK_GRAY = (25, 25, 30)
RED = (200, 50, 50)
DARK_RED = (150, 30, 30)
GREEN = (50, 180, 50)
DARK_GREEN = (30, 120, 30)
BLUE = (50, 100, 200)
YELLOW = (220, 200, 50)
GOLD = (255, 215, 0)
CRIMSON = (139, 0, 0)
ORANGE = (255, 140, 0)

def draw_button(draw, x, y, w, h, text, color, tc=WHITE):
    draw.rectangle([x, y, x+w, y+h], fill=color, outline=WHITE, width=2)
    try:
        font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 20)
    except:
        font = ImageFont.load_default()
    bbox = draw.textbbox((0, 0), text, font=font)
    tw = bbox[2] - bbox[0]
    th = bbox[3] - bbox[1]
    draw.text((x+(w-tw)//2, y+(h-th)//2), text, fill=tc, font=font)

def draw_bar(draw, x, y, w, h, val, maxv=100, color=GREEN):
    draw.rectangle([x, y, x+w, y+h], fill=DARK_GRAY, outline=WHITE, width=2)
    fw = int((val/maxv)*w)
    if fw > 0:
        draw.rectangle([x, y, x+fw, y+h], fill=color)

os.makedirs('screenshots_titp', exist_ok=True)

# 1. Dashboard
img = Image.new('RGB', (WIDTH, HEIGHT), VERY_DARK_GRAY)
draw = ImageDraw.Draw(img)
try:
    tf = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 38)
    lf = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 24)
    sf = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 18)
except:
    tf = lf = sf = ImageFont.load_default()

draw.text((50, 30), "PRESIDENTIAL DASHBOARD", fill=GOLD, font=tf)
draw.text((50, 75), "Week 35 / 208", fill=WHITE, font=lf)
draw.text((250, 78), "173 weeks until end of term", fill=YELLOW, font=sf)
draw.text((50, 100), "28th Amendment: 28/67 votes", fill=GOLD, font=lf)
draw_bar(draw, 50, 120, 400, 30, 28, 67, GOLD)
draw.text((50, 180), "Threat Level: 45%", fill=ORANGE, font=lf)
draw_bar(draw, 50, 200, 400, 30, 45, 100, ORANGE)
draw.text((50, 260), "Approval: 52.3%", fill=YELLOW, font=lf)
draw_bar(draw, 50, 280, 400, 30, 52.3, 100, YELLOW)
draw.text((50, 340), "Funds: $287,000", fill=GREEN, font=lf)
draw.text((50, 400), "ACTIVE INVESTIGATIONS", fill=RED, font=tf)
draw.text((70, 450), "Tax Fraud: 32%", fill=RED, font=lf)
draw.text((450, 455), "[MODERATE]", fill=ORANGE, font=sf)
draw.text((70, 485), "Obstruction: 67%", fill=RED, font=lf)
draw.text((450, 490), "[HIGH]", fill=RED, font=sf)
draw.text((50, 580), "TEAM STATUS", fill=BLUE, font=tf)
draw.text((70, 630), "3/6 advisors on assignment", fill=WHITE, font=lf)
draw_button(draw, 900, 100, 250, 50, "Advisors", BLUE)
draw_button(draw, 900, 170, 250, 50, "Assign Tasks", DARK_GREEN)
draw_button(draw, 900, 680, 250, 60, "NEXT WEEK", CRIMSON)
draw.text((50, 760), "GOAL: Secure 67 votes for 28th Amendment", fill=GOLD, font=sf)
img.save('screenshots_titp/1_dashboard.png')
print("✓ Dashboard")

# 2. Advisors
img = Image.new('RGB', (WIDTH, HEIGHT), VERY_DARK_GRAY)
draw = ImageDraw.Draw(img)
draw.text((50, 30), "YOUR TEAM", fill=GOLD, font=tf)
advisors = [
    ("Richard Moss", "Chief of Staff", False, 72, 35),
    ("Sarah Chen", "Attorney General", True, 85, 15),
    ("Marcus Webb", "Press Secretary", False, 68, 42),
    ("General Hayes", "Security Advisor", True, 91, 28),
    ("Tony Romano", "Personal Fixer", True, 58, 65),
    ("Victoria Sterling", "Lobbyist", False, 77, 22)
]
y = 100
for name, role, busy, loy, stress in advisors:
    col = VERY_DARK_GRAY if busy else DARK_GRAY
    draw.rectangle([50, y, 1150, y+90], fill=col, outline=WHITE, width=2)
    draw.text((70, y+10), name, fill=WHITE, font=lf)
    draw.text((70, y+35), role, fill=LIGHT_GRAY, font=sf)
    if busy:
        draw.text((70, y+60), "ON MISSION: Bribe Congressman", fill=YELLOW, font=sf)
    else:
        draw.text((70, y+60), "AVAILABLE", fill=GREEN, font=sf)
    lc = GREEN if loy>70 else YELLOW if loy>40 else RED
    draw.text((700, y+20), f"Loyalty: {loy}%", fill=lc, font=sf)
    sc = RED if stress>70 else YELLOW if stress>40 else GREEN
    draw.text((700, y+50), f"Stress: {stress}%", fill=sc, font=sf)
    draw.text((900, y+35), "Legal:8 Illegal:4 Media:7", fill=LIGHT_GRAY, font=sf)
    y += 105
draw_button(draw, 50, 720, 200, 50, "Back", DARK_GRAY)
img.save('screenshots_titp/2_advisors.png')
print("✓ Advisors")

# 3. Victory
img = Image.new('RGB', (WIDTH, HEIGHT), VERY_DARK_GRAY)
draw = ImageDraw.Draw(img)
try:
    vf = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 64)
except:
    vf = tf
t = "28th AMENDMENT PASSED"
bbox = draw.textbbox((0, 0), t, font=vf)
tw = bbox[2] - bbox[0]
draw.text((WIDTH//2-tw//2, 200), t, fill=GOLD, font=vf)
draw.text((WIDTH//2-200, 300), "Presidential Immunity Secured", fill=WHITE, font=lf)
stats = ["Final Vote: 67-33", "Weeks: 142", "Approval: 48.7%", "Corrupted: 4/6"]
sy = 400
for s in stats:
    bbox = draw.textbbox((0, 0), s, font=lf)
    sw = bbox[2] - bbox[0]
    draw.text((WIDTH//2-sw//2, sy), s, fill=LIGHT_GRAY, font=lf)
    sy += 40
draw_button(draw, 450, 650, 300, 60, "Main Menu", DARK_GRAY)
img.save('screenshots_titp/3_victory.png')
print("✓ Victory")

print("\n✅ Created 3 TITP screenshots!")
