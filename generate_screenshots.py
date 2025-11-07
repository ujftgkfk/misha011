#!/usr/bin/env python3
"""
Генератор скриншотов для игры Succession
Создает изображения, показывающие как выглядит игра
"""

from PIL import Image, ImageDraw, ImageFont
import os

# Размеры окна
WIDTH = 1000
HEIGHT = 700

# Цвета из игры
BG_COLOR = "#16213e"
GOLD = "#d4af37"
WHITE = "#ffffff"
BUTTON_COLOR = "#0f3460"
STAT_BG = "#1a1a2e"

def create_character_selection_screen():
    """Создает скриншот экрана выбора персонажа"""
    img = Image.new('RGB', (WIDTH, HEIGHT), BG_COLOR)
    draw = ImageDraw.Draw(img)

    # Заголовок
    try:
        title_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 48)
        text_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 20)
        small_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 14)
    except:
        title_font = ImageFont.load_default()
        text_font = ImageFont.load_default()
        small_font = ImageFont.load_default()

    # Заголовок
    title = "SUCCESSION GAME"
    title_bbox = draw.textbbox((0, 0), title, font=title_font)
    title_width = title_bbox[2] - title_bbox[0]
    draw.text((WIDTH//2 - title_width//2, 30), title, fill=GOLD, font=title_font)

    subtitle = "Выберите персонажа"
    subtitle_bbox = draw.textbbox((0, 0), subtitle, font=text_font)
    subtitle_width = subtitle_bbox[2] - subtitle_bbox[0]
    draw.text((WIDTH//2 - subtitle_width//2, 100), subtitle, fill=WHITE, font=text_font)

    # Карточки персонажей (2x2)
    card_width = 400
    card_height = 200
    padding = 30
    start_x = (WIDTH - (card_width * 2 + padding)) // 2
    start_y = 180

    characters = [
        {"name": "Kendall Roy", "desc": "Амбициозный наследник", "bonus": "+10 к власти"},
        {"name": "Shiv Roy", "desc": "Стратег и манипулятор", "bonus": "+10 к репутации"},
        {"name": "Roman Roy", "desc": "Непредсказуемый игрок", "bonus": "+10 к богатству"},
        {"name": "Connor Roy", "desc": "Независимый аутсайдер", "bonus": "+10 к лояльности"}
    ]

    for i, char in enumerate(characters):
        row = i // 2
        col = i % 2
        x = start_x + col * (card_width + padding)
        y = start_y + row * (card_height + padding)

        # Карточка
        draw.rectangle([x, y, x + card_width, y + card_height], fill=BUTTON_COLOR, outline=GOLD, width=2)

        # Имя
        name_bbox = draw.textbbox((0, 0), char["name"], font=text_font)
        name_width = name_bbox[2] - name_bbox[0]
        draw.text((x + card_width//2 - name_width//2, y + 20), char["name"], fill=GOLD, font=text_font)

        # Описание
        desc_bbox = draw.textbbox((0, 0), char["desc"], font=small_font)
        desc_width = desc_bbox[2] - desc_bbox[0]
        draw.text((x + card_width//2 - desc_width//2, y + 70), char["desc"], fill=WHITE, font=small_font)

        # Бонус
        bonus_bbox = draw.textbbox((0, 0), char["bonus"], font=small_font)
        bonus_width = bonus_bbox[2] - bonus_bbox[0]
        draw.text((x + card_width//2 - bonus_width//2, y + 110), char["bonus"], fill=GOLD, font=small_font)

        # Кнопка "Выбрать"
        button_text = "[ВЫБРАТЬ]"
        button_bbox = draw.textbbox((0, 0), button_text, font=small_font)
        button_width = button_bbox[2] - button_bbox[0]
        draw.text((x + card_width//2 - button_width//2, y + 150), button_text, fill=GOLD, font=small_font)

    return img

def create_gameplay_screen():
    """Создает скриншот игрового процесса"""
    img = Image.new('RGB', (WIDTH, HEIGHT), BG_COLOR)
    draw = ImageDraw.Draw(img)

    try:
        title_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 32)
        text_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 16)
        small_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 14)
    except:
        title_font = ImageFont.load_default()
        text_font = ImageFont.load_default()
        small_font = ImageFont.load_default()

    # Верхняя панель со статами
    stat_height = 120
    draw.rectangle([0, 0, WIDTH, stat_height], fill=STAT_BG)

    # Заголовок
    player_text = "Персонаж: Kendall Roy"
    draw.text((20, 15), player_text, fill=GOLD, font=text_font)

    # Статы
    stats = [
        ("Власть", 65, "#e74c3c"),
        ("Лояльность", 45, "#3498db"),
        ("Репутация", 70, "#2ecc71"),
        ("Богатство", 80, "#f39c12")
    ]

    stat_y = 50
    stat_width = 200
    stat_height_bar = 20

    for i, (name, value, color) in enumerate(stats):
        x = 20 + (i % 2) * 480
        y = stat_y + (i // 2) * 35

        # Название стата
        draw.text((x, y - 20), f"{name}: {value}", fill=WHITE, font=small_font)

        # Полоса стата
        draw.rectangle([x, y, x + stat_width, y + stat_height_bar], outline=GOLD, width=1)
        fill_width = int(stat_width * value / 100)
        draw.rectangle([x, y, x + fill_width, y + stat_height_bar], fill=color)

    # Сцена
    scene_y = stat_height + 30
    scene_title = "СЦЕНА 5: Семейный ужин"
    title_bbox = draw.textbbox((0, 0), scene_title, font=title_font)
    title_width = title_bbox[2] - title_bbox[0]
    draw.text((WIDTH//2 - title_width//2, scene_y), scene_title, fill=GOLD, font=title_font)

    # Текст сцены
    scene_text = [
        "Семейный ужин в поместье. Логан наблюдает за всеми.",
        "Shiv делает намёк на ваши последние неудачи.",
        "Roman усмехается. Атмосфера накаляется.",
        "",
        "Что вы делаете?"
    ]

    text_y = scene_y + 60
    for line in scene_text:
        line_bbox = draw.textbbox((0, 0), line, font=text_font)
        line_width = line_bbox[2] - line_bbox[0]
        draw.text((WIDTH//2 - line_width//2, text_y), line, fill=WHITE, font=text_font)
        text_y += 30

    # Кнопки выбора
    choice_y = text_y + 30
    choices = [
        "1. Публично поддержать Shiv, чтобы завоевать доверие",
        "2. Защищаться и контратаковать Roman",
        "3. Уйти от темы, сменив разговор на бизнес"
    ]

    button_height = 50
    for i, choice in enumerate(choices):
        y = choice_y + i * (button_height + 10)
        draw.rectangle([50, y, WIDTH-50, y + button_height], fill=BUTTON_COLOR, outline=GOLD, width=2)

        choice_bbox = draw.textbbox((0, 0), choice, font=small_font)
        choice_width = choice_bbox[2] - choice_bbox[0]
        draw.text((WIDTH//2 - choice_width//2, y + 15), choice, fill=WHITE, font=small_font)

    return img

def create_ending_screen():
    """Создает скриншот экрана концовки"""
    img = Image.new('RGB', (WIDTH, HEIGHT), BG_COLOR)
    draw = ImageDraw.Draw(img)

    try:
        title_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 48)
        text_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 20)
        small_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 16)
    except:
        title_font = ImageFont.load_default()
        text_font = ImageFont.load_default()
        small_font = ImageFont.load_default()

    # Заголовок
    title = "ПОБЕДА!"
    title_bbox = draw.textbbox((0, 0), title, font=title_font)
    title_width = title_bbox[2] - title_bbox[0]
    draw.text((WIDTH//2 - title_width//2, 50), title, fill=GOLD, font=title_font)

    # Подзаголовок
    subtitle = "Новый CEO Waystar Royco"
    subtitle_bbox = draw.textbbox((0, 0), subtitle, font=text_font)
    subtitle_width = subtitle_bbox[2] - subtitle_bbox[0]
    draw.text((WIDTH//2 - subtitle_width//2, 130), subtitle, fill=GOLD, font=text_font)

    # Текст концовки
    ending_text = [
        "",
        "Вы успешно прошли все испытания.",
        "Совет директоров единогласно проголосовал за вашу кандидатуру.",
        "",
        "Логан с гордостью пожимает вам руку.",
        "Семья Roy переходит под ваше управление.",
        "",
        "Империя в ваших руках!"
    ]

    text_y = 200
    for line in ending_text:
        line_bbox = draw.textbbox((0, 0), line, font=small_font)
        line_width = line_bbox[2] - line_bbox[0]
        draw.text((WIDTH//2 - line_width//2, text_y), line, fill=WHITE, font=small_font)
        text_y += 35

    # Финальные статы
    stats_y = text_y + 30
    draw.text((WIDTH//2 - 100, stats_y), "ФИНАЛЬНЫЕ ПОКАЗАТЕЛИ:", fill=GOLD, font=text_font)

    final_stats = [
        "Власть: 85/100",
        "Лояльность: 78/100",
        "Репутация: 92/100",
        "Богатство: 88/100"
    ]

    stats_y += 50
    for stat in final_stats:
        stat_bbox = draw.textbbox((0, 0), stat, font=small_font)
        stat_width = stat_bbox[2] - stat_bbox[0]
        draw.text((WIDTH//2 - stat_width//2, stats_y), stat, fill=WHITE, font=small_font)
        stats_y += 30

    # Кнопка "Начать заново"
    button_y = HEIGHT - 80
    draw.rectangle([WIDTH//2 - 150, button_y, WIDTH//2 + 150, button_y + 50],
                   fill=BUTTON_COLOR, outline=GOLD, width=2)
    button_text = "НАЧАТЬ ЗАНОВО"
    button_bbox = draw.textbbox((0, 0), button_text, font=text_font)
    button_width = button_bbox[2] - button_bbox[0]
    draw.text((WIDTH//2 - button_width//2, button_y + 12), button_text, fill=GOLD, font=text_font)

    return img

# Создаем директорию для скриншотов
os.makedirs("screenshots", exist_ok=True)

# Генерируем скриншоты
print("Генерирую скриншоты игры...")

print("1. Создаю экран выбора персонажа...")
screen1 = create_character_selection_screen()
screen1.save("screenshots/01_character_selection.png")
print("   ✓ Сохранено: screenshots/01_character_selection.png")

print("2. Создаю экран игрового процесса...")
screen2 = create_gameplay_screen()
screen2.save("screenshots/02_gameplay.png")
print("   ✓ Сохранено: screenshots/02_gameplay.png")

print("3. Создаю экран концовки...")
screen3 = create_ending_screen()
screen3.save("screenshots/03_ending.png")
print("   ✓ Сохранено: screenshots/03_ending.png")

print("\n✅ Все скриншоты успешно созданы в папке 'screenshots/'!")
