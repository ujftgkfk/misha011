#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🔥 SUCCESSION: БИТВА ЗА WAYSTAR ROYCO 🔥
Десктопная игра с расширенным сюжетом

Требования: Python 3.6+, tkinter (встроен в Python)
Запуск: python succession_game.py
"""

import tkinter as tk
from tkinter import ttk, messagebox, font
import json
import random
import time
from datetime import datetime
import os
import threading

# ============================================
# КОНСТАНТЫ И НАСТРОЙКИ
# ============================================

WINDOW_WIDTH = 1200
WINDOW_HEIGHT = 800
BG_COLOR = "#16213e"
GOLD = "#d4af37"
LIGHT_GOLD = "#ffd700"
RED = "#ff0000"
GREEN = "#4ade80"
GRAY = "#c0c0c0"

# ============================================
# ПЕРСОНАЖИ
# ============================================

CHARACTERS = {
    "kendall": {
        "name": "Кендалл Рой",
        "emoji": "🎯",
        "description": "Амбициозный наследник с жаждой власти.\nНестабилен, но опасен.",
        "stats": {"power": 60, "loyalty": 40, "reputation": 50, "wealth": 60},
        "bonuses": {"power": 1.3, "loyalty": 0.8}
    },
    "shiv": {
        "name": "Шив Рой",
        "emoji": "👩‍💼",
        "description": "Политически подкованная дочь Логана.\nУмна и расчетлива.",
        "stats": {"power": 50, "loyalty": 55, "reputation": 65, "wealth": 50},
        "bonuses": {"reputation": 1.3, "loyalty": 1.2}
    },
    "roman": {
        "name": "Роман Рой",
        "emoji": "😎",
        "description": "Непредсказуемый и креативный.\nИспользует юмор как оружие.",
        "stats": {"power": 45, "loyalty": 60, "reputation": 45, "wealth": 65},
        "bonuses": {"wealth": 1.3, "power": 0.9}
    },
    "connor": {
        "name": "Коннор Рой",
        "emoji": "🤵",
        "description": "Старший брат-эксцентрик.\nАутсайдер с неожиданными козырями.",
        "stats": {"power": 40, "loyalty": 65, "reputation": 40, "wealth": 75},
        "bonuses": {"wealth": 1.4, "power": 0.7}
    }
}

# ============================================
# РАСШИРЕННЫЕ СЦЕНАРИИ (30+ сценариев!)
# ============================================

SCENARIOS = [
    # Начало (сцены 0-4)
    {
        "id": 0,
        "title": "🏢 ЭКСТРЕННОЕ СОВЕЩАНИЕ",
        "text": "Вы - {character}! Логан созывает ЭКСТРЕННОЕ совещание совета директоров. Все нервничают. В воздухе пахнет предательством и большими деньгами.",
        "choices": [
            {"text": "⚡ Прийти первым и подготовить союзников", "effects": {"power": 15, "loyalty": 10}, "next": 1},
            {"text": "😎 Появиться с опозданием, показав превосходство", "effects": {"power": 10, "loyalty": -15, "reputation": 15}, "next": 1},
            {"text": "🤝 Провести тайную встречу с Герри до совещания", "effects": {"power": 20, "wealth": 10}, "next": 1}
        ]
    },
    {
        "id": 1,
        "title": "💥 МЕДИА-СКАНДАЛ!",
        "text": "Ваш телеканал слил компромат на влиятельного сенатора! Грозит суд на миллиарды! Логан ВЗБЕШЕН и требует НЕМЕДЛЕННЫХ действий!",
        "choices": [
            {"text": "😨 Принести публичные извинения", "effects": {"power": -15, "loyalty": 20, "reputation": -20}, "next": 2},
            {"text": "⚔️ Защищать свободу прессы до конца!", "effects": {"power": 25, "reputation": 30, "wealth": -25}, "next": 2},
            {"text": "💰 Подкупить сенатора миллионами", "effects": {"power": 30, "wealth": -35, "reputation": -15}, "next": 2}
        ]
    },
    {
        "id": 2,
        "title": "🗡️ СЕМЕЙНЫЙ ЗАГОВОР",
        "text": "Ваши братья и сестры тайно встречаются. Они предлагают объединиться и СВЕРГНУТЬ Логана! Обещают вам пост CEO. Но можно ли им доверять?",
        "choices": [
            {"text": "🔥 Присоединиться к заговору!", "effects": {"power": 40, "loyalty": -35}, "next": 3},
            {"text": "👴 Доложить Логану о предательстве", "effects": {"power": -15, "loyalty": 40, "reputation": 15}, "next": 3},
            {"text": "😈 Играть на обе стороны", "effects": {"power": 45, "loyalty": -25, "reputation": -20}, "next": 3}
        ]
    },
    {
        "id": 3,
        "title": "🎬 ВСТРЕЧА С ТОМОМ",
        "text": "Том Вамбсганс просит о частной встрече. Он явно что-то скрывает и сильно нервничает. Говорит, что у него есть ВАЖНАЯ информация о планах Логана.",
        "choices": [
            {"text": "💸 Подкупить Тома деньгами", "effects": {"power": 20, "wealth": -15}, "next": 4},
            {"text": "😠 Пригрозить ему разоблачением", "effects": {"power": 25, "loyalty": -20}, "next": 4},
            {"text": "🤝 Предложить союз против Шив", "effects": {"power": 30, "loyalty": 15}, "next": 4}
        ]
    },
    {
        "id": 4,
        "title": "📊 ПАДЕНИЕ АКЦИЙ!",
        "text": "Акции Waystar Royco обвалились на 30%! Инвесторы в панике! Совет директоров требует НЕМЕДЛЕННЫХ действий. Ваша репутация на кону!",
        "choices": [
            {"text": "🔄 Радикальная реструктуризация компании", "effects": {"power": 30, "loyalty": -25}, "next": 5},
            {"text": "😤 Найти козла отпущения", "effects": {"power": 20, "loyalty": -30, "reputation": -15}, "next": 5},
            {"text": "💰 Лично выкупить падающие акции", "effects": {"wealth": -40, "power": 40, "reputation": 25}, "next": 5}
        ]
    },

    # Середина игры (сцены 5-14)
    {
        "id": 5,
        "title": "🍷 СЕМЕЙНЫЙ УЖИН",
        "text": "Логан устраивает семейный ужин в своем поместье. За столом - вся семья. Атмосфера напряженная. Логан внезапно спрашивает КАЖДОГО, почему именно ОН достоин стать CEO.",
        "choices": [
            {"text": "🎤 Страстная речь о своих достижениях", "effects": {"power": 25, "reputation": 20}, "next": 6},
            {"text": "🗡️ Унизить остальных наследников", "effects": {"power": 30, "loyalty": -35, "reputation": -20}, "next": 6},
            {"text": "🧘 Промолчать, сохранив достоинство", "effects": {"power": 5, "reputation": 25, "loyalty": 15}, "next": 6}
        ]
    },
    {
        "id": 6,
        "title": "⚖️ ФБР НАЧИНАЕТ РАССЛЕДОВАНИЕ",
        "text": "Федеральные агенты пришли в офис! Они расследуют незаконную деятельность Waystar Royco. Вам ЛИЧНО предлагают иммунитет в обмен на показания против Логана!",
        "choices": [
            {"text": "🐀 Согласиться на сделку с властями", "effects": {"power": -40, "loyalty": -50, "wealth": 35}, "next": 7},
            {"text": "🛡️ Защищать семью любой ценой", "effects": {"power": 20, "loyalty": 40, "wealth": -25}, "next": 7},
            {"text": "🎭 Использовать ситуацию для шантажа", "effects": {"power": 35, "loyalty": -20, "wealth": 20}, "next": 7}
        ]
    },
    {
        "id": 7,
        "title": "📱 ГРЕГ ПРИНОСИТ ДОСЬЕ",
        "text": "Грег случайно нашел ВЗРЫВООПАСНОЕ досье на всех директоров компании! Он не понимает ценности информации и просит вашего совета. Что с этим делать?",
        "choices": [
            {"text": "💰 Забрать досье себе", "effects": {"power": 30, "loyalty": -15}, "next": 8},
            {"text": "🤝 Помочь Грегу использовать это", "effects": {"power": 15, "loyalty": 20}, "next": 8},
            {"text": "🔥 Уничтожить досье", "effects": {"power": -10, "loyalty": 30, "reputation": 20}, "next": 8}
        ]
    },
    {
        "id": 8,
        "title": "🌐 ПРЕДЛОЖЕНИЕ КОНКУРЕНТА",
        "text": "Главный конкурент Waystar Royco предлагает СЛИЯНИЕ на выгодных условиях. Вы получите огромное влияние, но это конец семейной империи Роев!",
        "choices": [
            {"text": "✅ Поддержать слияние", "effects": {"power": -25, "loyalty": -40, "wealth": 50, "reputation": 20}, "next": 9},
            {"text": "❌ Саботировать сделку", "effects": {"power": 25, "loyalty": 20, "reputation": -20}, "next": 9},
            {"text": "🦈 Поглотить конкурента!", "effects": {"power": 50, "wealth": 25, "loyalty": 15}, "next": 9}
        ]
    },
    {
        "id": 9,
        "title": "💔 ЛИЧНЫЙ СКАНДАЛ",
        "text": "Таблоиды опубликовали КОМПРОМЕТИРУЮЩИЕ фотографии из вашей личной жизни! Скандал набирает обороты! Семья в ШОКЕ!",
        "choices": [
            {"text": "😢 Публичные извинения", "effects": {"reputation": -25, "loyalty": 20}, "next": 10},
            {"text": "😤 Игнорировать скандал", "effects": {"reputation": -35, "power": 15}, "next": 10},
            {"text": "⚔️ Атаковать СМИ через юристов", "effects": {"power": 20, "wealth": -20, "reputation": -15}, "next": 10}
        ]
    },
    {
        "id": 10,
        "title": "🏰 ПРИГЛАШЕНИЕ ОТ ЛОГАНА",
        "text": "Логан приглашает ВАС ОДНОГО на выходные в свое частное поместье. Остальные наследники НЕ приглашены. Это ваш ШАНС или ЛОВУШКА?",
        "choices": [
            {"text": "🎉 Принять с энтузиазмом", "effects": {"power": 25, "loyalty": 15}, "next": 11},
            {"text": "🤔 Взять с собой союзников", "effects": {"power": 15, "loyalty": 20}, "next": 11},
            {"text": "🚫 Вежливо отказаться", "effects": {"power": -20, "loyalty": -15}, "next": 11}
        ]
    },
    {
        "id": 11,
        "title": "🎯 ДЕТЕКТИВ С ДОСЬЕ",
        "text": "Частный детектив приносит вам ПОЛНОЕ ДОСЬЕ на всех конкурентов - братьев, сестер, даже на самого Логана! Информация ВЗРЫВООПАСНАЯ!",
        "choices": [
            {"text": "💣 Использовать НЕМЕДЛЕННО!", "effects": {"power": 50, "loyalty": -50, "reputation": -30}, "next": 12},
            {"text": "💼 Сохранить как страховку", "effects": {"power": 25, "loyalty": -15}, "next": 12},
            {"text": "🔥 Уничтожить из принципа", "effects": {"power": -15, "loyalty": 35, "reputation": 20}, "next": 12}
        ]
    },
    {
        "id": 12,
        "title": "🌐 ХАКЕР ПРЕДЛАГАЕТ УСЛУГИ",
        "text": "Хакер-инсайдер предлагает доступ к КОНФИДЕНЦИАЛЬНОЙ переписке совета директоров. Цена высока, но информация БЕСЦЕННА!",
        "choices": [
            {"text": "💰 Заплатить и получить доступ", "effects": {"power": 35, "wealth": -30}, "next": 13},
            {"text": "👮 Арестовать хакера", "effects": {"power": 20, "reputation": 15, "wealth": -10}, "next": 13},
            {"text": "🚫 Отказаться от сделки", "effects": {"power": -5, "reputation": 15, "loyalty": 15}, "next": 13}
        ]
    },
    {
        "id": 13,
        "title": "📺 МЕДИА-КОНФЕРЕНЦИЯ",
        "text": "Вас приглашают выступить на крупнейшей медиа-конференции мира! Это шанс ЗАЯВИТЬ о себе, но и риск опозориться перед всем миром!",
        "choices": [
            {"text": "🔥 Провокационная речь!", "effects": {"power": 25, "reputation": 30, "loyalty": -20}, "next": 14},
            {"text": "💼 Безопасная корпоративная риторика", "effects": {"power": 10, "reputation": 10, "loyalty": 15}, "next": 14},
            {"text": "🚫 Отказаться от выступления", "effects": {"power": -15, "reputation": -10}, "next": 14}
        ]
    },
    {
        "id": 14,
        "title": "🎪 КОРПОРАТИВНАЯ ВЕЧЕРИНКА",
        "text": "Waystar Royco устраивает грандиозную вечеринку для инвесторов. ВСЕ топ-менеджеры и акционеры здесь. Идеальное место для ИНТРИГ!",
        "choices": [
            {"text": "🍾 Подпоить ключевых людей", "effects": {"power": 20, "loyalty": -10, "reputation": -15}, "next": 15},
            {"text": "🎭 Устроить публичное шоу", "effects": {"power": 30, "reputation": 25, "loyalty": -15}, "next": 15},
            {"text": "🤝 Тихо провести переговоры", "effects": {"power": 25, "loyalty": 20}, "next": 15}
        ]
    },

    # Кульминация (сцены 15-24)
    {
        "id": 15,
        "title": "💰 ТАЙНАЯ СДЕЛКА С БАНКОМ",
        "text": "Крупнейший банк предлагает вам ЛИЧНЫЙ кредит на миллиарды под выкуп акций компании. Но это привяжет вас к ним НАВСЕГДА!",
        "choices": [
            {"text": "✅ Принять предложение банка", "effects": {"wealth": 50, "power": 30, "loyalty": -20}, "next": 16},
            {"text": "❌ Отказаться и найти другие источники", "effects": {"power": 10, "reputation": 15}, "next": 16},
            {"text": "🎭 Использовать предложение для шантажа Логана", "effects": {"power": 40, "loyalty": -25}, "next": 16}
        ]
    },
    {
        "id": 16,
        "title": "🎬 ГЕРРИ ПРОСИТ ПОМОЩИ",
        "text": "Герри Келлман, главный юрист компании, приходит к вам В ОТЧАЯНИИ. На нее давят федералы. Она просит вашей защиты в обмен на ПОЛНУЮ лояльность!",
        "choices": [
            {"text": "🛡️ Защитить Герри любой ценой", "effects": {"loyalty": 30, "wealth": -20, "power": 20}, "next": 17},
            {"text": "🤷 Бросить ее на произвол судьбы", "effects": {"power": -10, "loyalty": -25, "reputation": -20}, "next": 17},
            {"text": "🎯 Использовать ситуацию в своих целях", "effects": {"power": 35, "loyalty": -15}, "next": 17}
        ]
    },
    {
        "id": 17,
        "title": "📉 КРИЗИС В КОМПАНИИ",
        "text": "Waystar Royco на грани БАНКРОТСТВА! Нужно СРОЧНО принять радикальные меры! Совет директоров требует решений СЕГОДНЯ!",
        "choices": [
            {"text": "✂️ Массовые увольнения", "effects": {"power": 20, "loyalty": -30, "wealth": 20, "reputation": -25}, "next": 18},
            {"text": "💰 Продать активы компании", "effects": {"wealth": 40, "power": -20, "reputation": -15}, "next": 18},
            {"text": "🎲 Рискованная инвестиция", "effects": {"power": 35, "wealth": -30, "reputation": 20}, "next": 18}
        ]
    },
    {
        "id": 18,
        "title": "🗳️ ГОЛОСОВАНИЕ СОВЕТА ДИРЕКТОРОВ",
        "text": "Совет директоров проводит ТАЙНОЕ голосование о будущем CEO компании! Каждый голос на счету! Нужно СРОЧНО заручиться поддержкой!",
        "choices": [
            {"text": "💸 Подкупить директоров", "effects": {"power": 40, "wealth": -40, "loyalty": -20}, "next": 19},
            {"text": "🎤 Убедительная презентация", "effects": {"power": 30, "reputation": 25, "loyalty": 15}, "next": 19},
            {"text": "🗡️ Шантаж компроматом", "effects": {"power": 50, "loyalty": -40, "reputation": -30}, "next": 19}
        ]
    },
    {
        "id": 19,
        "title": "👥 КОНФРОНТАЦИЯ С КЕНДАЛЛОМ",
        "text": "Кендалл ОТКРЫТО бросает вам вызов на совещании! Он обвиняет вас в ПРЕДАТЕЛЬСТВЕ семьи! Все смотрят на вас! Как реагировать?",
        "choices": [
            {"text": "⚔️ Принять вызов и ответить ударом", "effects": {"power": 35, "loyalty": -25, "reputation": 20}, "next": 20},
            {"text": "🧘 Игнорировать провокацию", "effects": {"power": 10, "reputation": 15, "loyalty": 20}, "next": 20},
            {"text": "😈 Разоблачить его секреты", "effects": {"power": 40, "loyalty": -30, "reputation": -15}, "next": 20}
        ]
    },
    {
        "id": 20,
        "title": "🌍 МЕЖДУНАРОДНЫЙ СКАНДАЛ",
        "text": "Ваша сделка с иностранной компанией вызвала МЕЖДУНАРОДНЫЙ скандал! Правительство требует объяснений! СМИ всего мира обсуждают это!",
        "choices": [
            {"text": "📺 Дать интервью и всё объяснить", "effects": {"reputation": -20, "loyalty": 15, "power": 10}, "next": 21},
            {"text": "🤐 Нанять пиар-команду для отмазок", "effects": {"wealth": -25, "reputation": 10, "power": 15}, "next": 21},
            {"text": "🎭 Обвинить конкурентов в клевете", "effects": {"power": 30, "reputation": -25, "loyalty": -15}, "next": 21}
        ]
    },
    {
        "id": 21,
        "title": "💼 СЕКРЕТНАЯ ВСТРЕЧА В ЛОНДОНЕ",
        "text": "Вас тайно приглашают на встречу в Лондон с представителями КОРОЛЕВСКОЙ семьи. Они предлагают стратегическое партнерство!",
        "choices": [
            {"text": "🤝 Принять предложение", "effects": {"power": 45, "wealth": 35, "reputation": 30}, "next": 22},
            {"text": "🤔 Запросить время на размышление", "effects": {"power": 15, "reputation": 10}, "next": 22},
            {"text": "❌ Отказаться в пользу американских партнеров", "effects": {"power": 20, "loyalty": 25, "reputation": -10}, "next": 22}
        ]
    },
    {
        "id": 22,
        "title": "🎰 РИСКОВАННАЯ ИНВЕСТИЦИЯ",
        "text": "Роман предлагает вам СОВМЕСТНУЮ инвестицию в рискованный стартап. Он обещает, что это 'ТОЧНО выстрелит'. Но можно ли ему доверять?",
        "choices": [
            {"text": "💰 Инвестировать по-крупному", "effects": {"wealth": -40, "power": 30, "loyalty": 20}, "next": 23},
            {"text": "💸 Вложить символическую сумму", "effects": {"wealth": -10, "loyalty": 10}, "next": 23},
            {"text": "🚫 Отказаться полностью", "effects": {"loyalty": -15, "power": -5}, "next": 23}
        ]
    },
    {
        "id": 23,
        "title": "⚡ ЛОГАН В БОЛЬНИЦЕ!",
        "text": "Логан срочно госпитализирован! Состояние КРИТИЧЕСКОЕ! Вся семья срочно собирается! Это может быть КОНЕЦ эпохи или начало ВОЙНЫ за трон!",
        "choices": [
            {"text": "🏃 Немедленно лететь к нему", "effects": {"loyalty": 25, "power": 15, "reputation": 15}, "next": 24},
            {"text": "📱 Остаться и укрепить позиции", "effects": {"power": 40, "loyalty": -30, "reputation": -20}, "next": 24},
            {"text": "🤝 Собрать семью для переговоров", "effects": {"power": 25, "loyalty": 20, "reputation": 10}, "next": 24}
        ]
    },
    {
        "id": 24,
        "title": "📜 ЗАВЕЩАНИЕ ЛОГАНА",
        "text": "Пока Логан в больнице, юристы находят его НОВОЕ завещание! Оно кардинально меняет всё! Но есть подозрение, что оно ПОДДЕЛКА!",
        "choices": [
            {"text": "🔍 Расследовать подлинность", "effects": {"power": 20, "reputation": 20}, "next": 25},
            {"text": "📝 Использовать завещание в своих целях", "effects": {"power": 45, "loyalty": -40, "reputation": -25}, "next": 25},
            {"text": "🔥 Уничтожить документ", "effects": {"power": 15, "loyalty": 15, "reputation": -15}, "next": 25}
        ]
    },

    # Финал (сцены 25-29)
    {
        "id": 25,
        "title": "👔 СОВЕТ ДИРЕКТОРОВ: РЕШАЮЩИЙ ДЕНЬ",
        "text": "Это ОНО! Совет директоров собирается для ФИНАЛЬНОГО решения о новом CEO! Все кандидаты присутствуют. Напряжение МАКСИМАЛЬНОЕ!",
        "choices": [
            {"text": "🎤 Произнести речь века", "effects": {"power": 35, "reputation": 30}, "next": 26},
            {"text": "💰 Последний раунд подкупа", "effects": {"power": 45, "wealth": -50, "loyalty": -25}, "next": 26},
            {"text": "🗡️ Разоблачить всех конкурентов", "effects": {"power": 50, "loyalty": -45, "reputation": -30}, "next": 26}
        ]
    },
    {
        "id": 26,
        "title": "🏆 ГОЛОСОВАНИЕ НАЧИНАЕТСЯ",
        "text": "Директора начинают голосование! Каждый поднимает руку... Счет идет... Кто победит?!",
        "choices": [
            {"text": "🙏 Молча ждать результатов", "effects": {"power": 10, "loyalty": 15}, "next": 27},
            {"text": "😠 Потребовать пересчета голосов", "effects": {"power": 20, "loyalty": -20, "reputation": -15}, "next": 27},
            {"text": "🎭 Покинуть зал демонстративно", "effects": {"power": -15, "reputation": 25}, "next": 27}
        ]
    },
    {
        "id": 27,
        "title": "📊 РЕЗУЛЬТАТЫ ГОЛОСОВАНИЯ",
        "text": "Голоса подсчитаны! Председатель совета готов огласить имя нового CEO Waystar Royco! Тишина...",
        "choices": [
            {"text": "😤 Заранее объявить себя победителем", "effects": {"power": 25, "loyalty": -30, "reputation": -20}, "next": 28},
            {"text": "🧘 Спокойно дождаться объявления", "effects": {"power": 15, "reputation": 15, "loyalty": 10}, "next": 28},
            {"text": "🚶 Уйти до объявления результатов", "effects": {"power": -20, "loyalty": -25}, "next": 28}
        ]
    },
    {
        "id": 28,
        "title": "⚡ ЛОГАН ВОЗВРАЩАЕТСЯ!",
        "text": "ВНЕЗАПНО! Логан входит в зал! Он ЖИВ! Он ЗДОРОВ! И у него есть ПОСЛЕДНЕЕ слово! Что он скажет?!",
        "choices": [
            {"text": "😱 Обняться с отцом", "effects": {"loyalty": 30, "power": 10}, "next": 29},
            {"text": "😠 Потребовать объяснений", "effects": {"power": 20, "loyalty": -20}, "next": 29},
            {"text": "🎭 Подыграть его появлению", "effects": {"power": 25, "reputation": 15, "loyalty": 15}, "next": 29}
        ]
    },
    {
        "id": 29,
        "title": "👑 ФИНАЛЬНОЕ РЕШЕНИЕ ЛОГАНА",
        "text": "Логан смотрит на каждого наследника... Время остановилось... Кого он выберет?! Кто станет главой империи Waystar Royco?!",
        "choices": [
            {"text": "💪 Показать силу и уверенность", "effects": {"power": 30, "reputation": 20}, "next": "END"},
            {"text": "🙏 Проявить уважение и смирение", "effects": {"loyalty": 35, "power": 15}, "next": "END"},
            {"text": "😈 Забрать власть силой!", "effects": {"power": 50, "loyalty": -50, "reputation": -40}, "next": "END"}
        ]
    }
]

# ============================================
# КЛАСС ИГРЫ
# ============================================

class SuccessionGame:
    def __init__(self, root):
        self.root = root
        self.root.title("🔥 SUCCESSION: БИТВА ЗА WAYSTAR ROYCO 🔥")
        self.root.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")
        self.root.configure(bg=BG_COLOR)

        # Состояние игры
        self.character = None
        self.stats = {"power": 50, "loyalty": 50, "reputation": 50, "wealth": 50}
        self.current_scene = 0
        self.history = []

        # Настройка шрифтов
        self.title_font = font.Font(family="Georgia", size=24, weight="bold")
        self.subtitle_font = font.Font(family="Georgia", size=14)
        self.text_font = font.Font(family="Georgia", size=12)
        self.button_font = font.Font(family="Georgia", size=11, weight="bold")

        # Запуск
        self.show_character_selection()

    def clear_screen(self):
        """Очистить экран"""
        for widget in self.root.winfo_children():
            widget.destroy()

    def show_character_selection(self):
        """Экран выбора персонажа"""
        self.clear_screen()

        # Заголовок
        title = tk.Label(
            self.root,
            text="🔥 ВЫБЕРИТЕ ВАШЕГО БОЙЦА! 🔥",
            font=self.title_font,
            fg=GOLD,
            bg=BG_COLOR
        )
        title.pack(pady=30)

        # Фрейм для карточек персонажей
        cards_frame = tk.Frame(self.root, bg=BG_COLOR)
        cards_frame.pack(expand=True)

        # Создаем карточки для каждого персонажа
        for char_id, char_data in CHARACTERS.items():
            self.create_character_card(cards_frame, char_id, char_data)

    def create_character_card(self, parent, char_id, char_data):
        """Создать карточку персонажа"""
        card = tk.Frame(
            parent,
            bg="#1a1a2e",
            relief=tk.RAISED,
            borderwidth=3,
            highlightbackground=GOLD,
            highlightthickness=2
        )
        card.pack(side=tk.LEFT, padx=20, pady=20, ipadx=20, ipady=20)

        # Эмодзи
        emoji_label = tk.Label(
            card,
            text=char_data["emoji"],
            font=("Arial", 60),
            bg="#1a1a2e"
        )
        emoji_label.pack()

        # Имя
        name_label = tk.Label(
            card,
            text=char_data["name"],
            font=self.subtitle_font,
            fg=GOLD,
            bg="#1a1a2e"
        )
        name_label.pack(pady=10)

        # Описание
        desc_label = tk.Label(
            card,
            text=char_data["description"],
            font=self.text_font,
            fg=GRAY,
            bg="#1a1a2e",
            justify=tk.CENTER
        )
        desc_label.pack(pady=10)

        # Статы
        stats_text = f"⚡ Власть: {char_data['stats']['power']}\n"
        stats_text += f"🤝 Лояльность: {char_data['stats']['loyalty']}\n"
        stats_text += f"⭐ Репутация: {char_data['stats']['reputation']}\n"
        stats_text += f"💰 Богатство: {char_data['stats']['wealth']}"

        stats_label = tk.Label(
            card,
            text=stats_text,
            font=self.text_font,
            fg=LIGHT_GOLD,
            bg="#1a1a2e",
            justify=tk.LEFT
        )
        stats_label.pack(pady=10)

        # Кнопка выбора
        select_btn = tk.Button(
            card,
            text="ВЫБРАТЬ",
            font=self.button_font,
            bg=GOLD,
            fg="#000",
            command=lambda: self.select_character(char_id),
            cursor="hand2",
            relief=tk.RAISED,
            borderwidth=3
        )
        select_btn.pack(pady=10)

    def select_character(self, char_id):
        """Выбрать персонажа"""
        self.character = char_id
        char_data = CHARACTERS[char_id]
        self.stats = char_data["stats"].copy()
        self.current_scene = 0
        self.history = []

        # Показываем игру
        self.show_game_screen()

    def show_game_screen(self):
        """Главный экран игры"""
        self.clear_screen()

        # Основной контейнер
        main_frame = tk.Frame(self.root, bg=BG_COLOR)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        # Верхняя панель (персонаж + кнопки)
        top_frame = tk.Frame(main_frame, bg=BG_COLOR)
        top_frame.pack(fill=tk.X, pady=(0, 20))

        # Инфо о персонаже
        char_data = CHARACTERS[self.character]
        char_info = tk.Label(
            top_frame,
            text=f"{char_data['emoji']} {char_data['name']}",
            font=self.subtitle_font,
            fg=GOLD,
            bg=BG_COLOR
        )
        char_info.pack(side=tk.LEFT)

        # Кнопка рестарта
        restart_btn = tk.Button(
            top_frame,
            text="🔄 НАЧАТЬ ЗАНОВО",
            font=self.button_font,
            bg=GOLD,
            fg="#000",
            command=self.restart_game,
            cursor="hand2"
        )
        restart_btn.pack(side=tk.RIGHT)

        # Панель статов
        stats_frame = tk.Frame(main_frame, bg=BG_COLOR)
        stats_frame.pack(fill=tk.X, pady=(0, 20))

        self.create_stat_bars(stats_frame)

        # Текст сцены
        self.scene_frame = tk.Frame(main_frame, bg="#1a1a2e", relief=tk.RAISED, borderwidth=3)
        self.scene_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 20))

        self.load_scene()

    def create_stat_bars(self, parent):
        """Создать полосы статов"""
        stats_labels = {
            "power": "⚡ Власть",
            "loyalty": "🤝 Лояльность",
            "reputation": "⭐ Репутация",
            "wealth": "💰 Богатство"
        }

        for i, (stat_key, stat_label) in enumerate(stats_labels.items()):
            # Контейнер для стата
            stat_container = tk.Frame(parent, bg=BG_COLOR)
            stat_container.grid(row=0, column=i, padx=10, sticky="ew")
            parent.grid_columnconfigure(i, weight=1)

            # Название
            name_label = tk.Label(
                stat_container,
                text=stat_label,
                font=self.text_font,
                fg=GRAY,
                bg=BG_COLOR
            )
            name_label.pack()

            # Значение
            value_label = tk.Label(
                stat_container,
                text=str(self.stats[stat_key]),
                font=("Georgia", 20, "bold"),
                fg=GOLD,
                bg=BG_COLOR
            )
            value_label.pack()

            # Прогресс-бар
            progress = ttk.Progressbar(
                stat_container,
                length=200,
                mode='determinate',
                maximum=100,
                value=self.stats[stat_key]
            )
            progress.pack(pady=5)

            # Стилизация прогресс-бара
            style = ttk.Style()
            style.theme_use('default')
            style.configure("TProgressbar",
                           background=GOLD,
                           troughcolor="#2d2d44",
                           bordercolor=GOLD,
                           lightcolor=LIGHT_GOLD,
                           darkcolor=GOLD)

    def load_scene(self):
        """Загрузить текущую сцену"""
        # Очищаем фрейм сцены
        for widget in self.scene_frame.winfo_children():
            widget.destroy()

        # Проверка на конец игры
        if self.current_scene >= len(SCENARIOS):
            self.show_ending()
            return

        scene = SCENARIOS[self.current_scene]

        # Заголовок сцены
        title_label = tk.Label(
            self.scene_frame,
            text=scene["title"],
            font=self.title_font,
            fg=GOLD,
            bg="#1a1a2e"
        )
        title_label.pack(pady=20)

        # Номер сцены
        scene_number = tk.Label(
            self.scene_frame,
            text=f"Сцена {self.current_scene + 1} / {len(SCENARIOS)}",
            font=self.text_font,
            fg=GRAY,
            bg="#1a1a2e"
        )
        scene_number.pack()

        # Текст сцены (с подстановкой персонажа)
        char_data = CHARACTERS[self.character]
        text = scene["text"].format(
            character=f"{char_data['emoji']} {char_data['name']}"
        )

        text_label = tk.Label(
            self.scene_frame,
            text=text,
            font=("Georgia", 14),
            fg="#fff",
            bg="#1a1a2e",
            wraplength=800,
            justify=tk.LEFT
        )
        text_label.pack(pady=30, padx=40)

        # Кнопки выборов
        choices_frame = tk.Frame(self.scene_frame, bg="#1a1a2e")
        choices_frame.pack(fill=tk.BOTH, expand=True, padx=40, pady=20)

        for choice in scene["choices"]:
            self.create_choice_button(choices_frame, choice)

    def create_choice_button(self, parent, choice):
        """Создать кнопку выбора"""
        btn = tk.Button(
            parent,
            text=choice["text"],
            font=("Georgia", 12, "bold"),
            bg="#2d2d44",
            fg="#fff",
            activebackground=GOLD,
            activeforeground="#000",
            command=lambda: self.make_choice(choice),
            cursor="hand2",
            relief=tk.RAISED,
            borderwidth=3,
            pady=15,
            anchor="w",
            justify=tk.LEFT
        )
        btn.pack(fill=tk.X, pady=10)

        # Эффект при наведении
        btn.bind("<Enter>", lambda e: btn.config(bg=GOLD, fg="#000"))
        btn.bind("<Leave>", lambda e: btn.config(bg="#2d2d44", fg="#fff"))

    def make_choice(self, choice):
        """Сделать выбор"""
        # Применяем эффекты
        self.apply_effects(choice["effects"])

        # Сохраняем в историю
        self.history.append({
            "scene": self.current_scene,
            "choice": choice["text"],
            "effects": choice["effects"]
        })

        # Проверяем game over
        if self.check_game_over():
            return

        # Переходим к следующей сцене
        if choice["next"] == "END" or self.current_scene >= len(SCENARIOS) - 1:
            self.show_ending()
        else:
            self.current_scene = choice["next"]
            self.show_game_screen()

    def apply_effects(self, effects):
        """Применить эффекты выбора"""
        char_data = CHARACTERS[self.character]
        bonuses = char_data.get("bonuses", {})

        for stat, value in effects.items():
            # Применяем бонусы персонажа
            if stat in bonuses:
                value = int(value * bonuses[stat])

            self.stats[stat] += value
            # Ограничиваем значения
            self.stats[stat] = max(0, min(100, self.stats[stat]))

    def check_game_over(self):
        """Проверить условия окончания игры"""
        if self.stats["power"] <= 0:
            self.show_game_over("💔 ПОРАЖЕНИЕ!", "Вы потеряли всю власть!\nВас изгнали из компании.")
            return True
        if self.stats["loyalty"] <= 0:
            self.show_game_over("🗡️ ПРЕДАТЕЛЬСТВО!", "Все союзники отвернулись от вас!\nОдиночество в бизнесе - это смерть.")
            return True
        if self.stats["reputation"] <= 0:
            self.show_game_over("😱 ПОЗОР!", "Ваша репутация уничтожена!\nСМИ называют вас худшим из Роев.")
            return True
        return False

    def show_game_over(self, title, message):
        """Показать экран проигрыша"""
        self.clear_screen()

        emoji = "💔"

        # Заголовок
        title_label = tk.Label(
            self.root,
            text=emoji,
            font=("Arial", 100),
            bg=BG_COLOR
        )
        title_label.pack(pady=30)

        title_text = tk.Label(
            self.root,
            text=title,
            font=self.title_font,
            fg=RED,
            bg=BG_COLOR
        )
        title_text.pack()

        # Сообщение
        msg_label = tk.Label(
            self.root,
            text=message,
            font=("Georgia", 16),
            fg="#fff",
            bg=BG_COLOR,
            justify=tk.CENTER
        )
        msg_label.pack(pady=30)

        # Статы
        stats_text = f"⚡ Власть: {self.stats['power']}\n"
        stats_text += f"🤝 Лояльность: {self.stats['loyalty']}\n"
        stats_text += f"⭐ Репутация: {self.stats['reputation']}\n"
        stats_text += f"💰 Богатство: {self.stats['wealth']}"

        stats_label = tk.Label(
            self.root,
            text=stats_text,
            font=("Georgia", 14),
            fg=GRAY,
            bg=BG_COLOR,
            justify=tk.CENTER
        )
        stats_label.pack(pady=20)

        # Кнопка рестарта
        restart_btn = tk.Button(
            self.root,
            text="🔄 ПОПРОБОВАТЬ СНОВА",
            font=("Georgia", 16, "bold"),
            bg=GOLD,
            fg="#000",
            command=self.restart_game,
            cursor="hand2",
            pady=15,
            padx=30
        )
        restart_btn.pack(pady=30)

    def show_ending(self):
        """Показать концовку игры"""
        self.clear_screen()

        # Определяем концовку
        total_score = sum(self.stats.values())

        if self.stats["power"] >= 80:
            emoji = "👑"
            title = "🎉 АБСОЛЮТНАЯ ПОБЕДА! 🎉"
            message = f"Поздравляем, {CHARACTERS[self.character]['name']}!\n\nВы стали НОВЫМ ГЛАВОЙ Waystar Royco!\nЛоган признал ваше превосходство!"
            color = GREEN
        elif self.stats["power"] >= 60:
            emoji = "🏆"
            title = "✨ ПОБЕДА! ✨"
            message = f"{CHARACTERS[self.character]['name']}, вы заняли\nВЫСОКУЮ позицию в компании!\nНе CEO, но близко к трону!"
            color = GOLD
        elif total_score >= 200:
            emoji = "😐"
            title = "Частичный успех"
            message = "Вы выжили в битве за Waystar Royco,\nно трон достался другому."
            color = GRAY
        else:
            emoji = "😔"
            title = "Неоднозначный финал"
            message = "Игра окончена. Вы не получили трон,\nно хотя бы остались в компании."
            color = GRAY

        # Эмодзи
        emoji_label = tk.Label(
            self.root,
            text=emoji,
            font=("Arial", 100),
            bg=BG_COLOR
        )
        emoji_label.pack(pady=30)

        # Заголовок
        title_label = tk.Label(
            self.root,
            text=title,
            font=self.title_font,
            fg=color,
            bg=BG_COLOR
        )
        title_label.pack()

        # Сообщение
        msg_label = tk.Label(
            self.root,
            text=message,
            font=("Georgia", 16),
            fg="#fff",
            bg=BG_COLOR,
            justify=tk.CENTER
        )
        msg_label.pack(pady=30)

        # Финальные статы
        stats_text = "⚡ ФИНАЛЬНЫЕ ПОКАЗАТЕЛИ ⚡\n\n"
        stats_text += f"⚡ Власть: {self.stats['power']}\n"
        stats_text += f"🤝 Лояльность: {self.stats['loyalty']}\n"
        stats_text += f"⭐ Репутация: {self.stats['reputation']}\n"
        stats_text += f"💰 Богатство: {self.stats['wealth']}\n\n"
        stats_text += f"📊 Общий счет: {total_score} / 400"

        stats_label = tk.Label(
            self.root,
            text=stats_text,
            font=("Georgia", 14),
            fg=LIGHT_GOLD,
            bg=BG_COLOR,
            justify=tk.CENTER
        )
        stats_label.pack(pady=20)

        # Кнопки
        btn_frame = tk.Frame(self.root, bg=BG_COLOR)
        btn_frame.pack(pady=30)

        restart_btn = tk.Button(
            btn_frame,
            text="🔄 ИГРАТЬ СНОВА",
            font=("Georgia", 14, "bold"),
            bg=GOLD,
            fg="#000",
            command=self.restart_game,
            cursor="hand2",
            pady=10,
            padx=20
        )
        restart_btn.pack(side=tk.LEFT, padx=10)

        quit_btn = tk.Button(
            btn_frame,
            text="❌ ВЫХОД",
            font=("Georgia", 14, "bold"),
            bg=RED,
            fg="#fff",
            command=self.root.quit,
            cursor="hand2",
            pady=10,
            padx=20
        )
        quit_btn.pack(side=tk.LEFT, padx=10)

    def restart_game(self):
        """Перезапустить игру"""
        self.character = None
        self.stats = {"power": 50, "loyalty": 50, "reputation": 50, "wealth": 50}
        self.current_scene = 0
        self.history = []
        self.show_character_selection()

# ============================================
# ЗАПУСК ИГРЫ
# ============================================

if __name__ == "__main__":
    root = tk.Tk()
    game = SuccessionGame(root)
    root.mainloop()
