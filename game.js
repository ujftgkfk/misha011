// ОСНОВНАЯ ИГРОВАЯ ЛОГИКА

// Состояние игры
let gameState = {
    currentScreen: 'intro',
    selectedCharacter: null,
    day: 1,
    week: 1,
    month: 1,
    monthName: 'Январь',
    stats: {
        influence: 50,
        reputation: 60,
        wealth: 500,
        health: 100
    },
    relationships: {},
    news: [],
    currentEvent: null,
    eventHistory: [],
    gameStarted: false
};

const MONTHS = [
    'Январь', 'Февраль', 'Март', 'Апрель', 'Май', 'Июнь',
    'Июль', 'Август', 'Сентябрь', 'Октябрь', 'Ноябрь', 'Декабрь'
];

// Инициализация игры
function initGame() {
    console.log('Инициализация игры...');
    loadGameState();
    updateUI();
}

// Показать экран
function showScreen(screenId) {
    document.querySelectorAll('.screen').forEach(screen => {
        screen.classList.remove('active');
    });
    document.getElementById(screenId).classList.add('active');
    gameState.currentScreen = screenId;
}

// Начать игру
function startGame() {
    if (!gameState.selectedCharacter) {
        showCharacterSelect();
    } else {
        initializeGameState();
        showScreen('game-screen');
        loadFirstEvent();
    }
}

// Показать выбор персонажа
function showCharacterSelect() {
    showScreen('character-select');
}

// Вернуться к intro
function showIntro() {
    showScreen('intro-screen');
}

// Выбрать персонажа
function selectCharacter(characterId) {
    const character = getCharacterInfo(characterId);
    if (!character) return;

    gameState.selectedCharacter = characterId;
    gameState.stats = { ...character.stats };
    gameState.relationships = getInitialRelationships(characterId);

    // Обновляем UI
    document.getElementById('player-name').textContent = character.name;
    document.getElementById('sidebar-name').textContent = character.name;
    document.getElementById('player-position').textContent = character.position;

    const avatar = document.getElementById('player-avatar');
    avatar.className = `player-avatar ${character.avatar}`;
    avatar.style.background = document.querySelector(`.character-image.${character.avatar}`).style.background;

    startGame();
}

// Инициализация игрового состояния
function initializeGameState() {
    gameState.gameStarted = true;
    gameState.day = 1;
    gameState.week = 1;
    gameState.month = 1;
    gameState.monthName = MONTHS[0];
    gameState.news = [{
        time: 'Сегодня',
        text: 'Совет директоров обсуждает будущее компании'
    }];

    updateAllUI();
}

// Загрузить первое событие
function loadFirstEvent() {
    const event = getEventForWeek(1);
    if (event) {
        displayEvent(event);
    }
}

// Отобразить событие
function displayEvent(event) {
    gameState.currentEvent = event;

    const eventCard = document.getElementById('current-event');
    const eventTitle = eventCard.querySelector('.event-title');
    const eventDescription = eventCard.querySelector('.event-description');
    const eventChoices = document.getElementById('event-choices');

    eventTitle.textContent = event.title;
    eventDescription.innerHTML = `<p>${event.description}</p>`;

    // Очистить выборы
    eventChoices.innerHTML = '';

    // Добавить варианты выбора
    if (event.choices && event.choices.length > 0) {
        event.choices.forEach((choice, index) => {
            const button = document.createElement('button');
            button.className = 'choice-btn';
            button.textContent = choice.text;
            button.onclick = () => makeChoice(choice, index);
            eventChoices.appendChild(button);
        });
    } else if (event.isGameEnd) {
        // Финальное событие
        showGameEnd();
    }
}

// Сделать выбор
function makeChoice(choice, choiceIndex) {
    // Применить эффекты
    if (choice.effects) {
        applyEffects(choice.effects);
    }

    // Добавить новость
    if (choice.news) {
        addNews(choice.news);
    }

    // Сохранить в историю
    gameState.eventHistory.push({
        event: gameState.currentEvent.id,
        choice: choiceIndex,
        week: gameState.week
    });

    // Анимация выбора
    const allButtons = document.querySelectorAll('.choice-btn');
    allButtons.forEach(btn => btn.style.opacity = '0.5');
    event.target.style.opacity = '1';
    event.target.style.borderColor = 'var(--accent-gold)';

    // Переход к следующему событию
    setTimeout(() => {
        if (choice.nextEvent) {
            const nextEvent = findEventById(choice.nextEvent);
            if (nextEvent) {
                displayEvent(nextEvent);
            } else {
                advanceTime();
            }
        } else {
            advanceTime();
        }
    }, 1000);
}

// Применить эффекты выбора
function applyEffects(effects) {
    // Базовые характеристики
    if (effects.influence) {
        gameState.stats.influence = clamp(gameState.stats.influence + effects.influence, 0, 100);
    }
    if (effects.reputation) {
        gameState.stats.reputation = clamp(gameState.stats.reputation + effects.reputation, 0, 100);
    }
    if (effects.wealth) {
        gameState.stats.wealth = Math.max(0, gameState.stats.wealth + effects.wealth);
    }
    if (effects.health) {
        gameState.stats.health = clamp(gameState.stats.health + effects.health, 0, 100);
    }

    // Отношения
    for (const npcId in NPC_CHARACTERS) {
        if (effects[npcId]) {
            changeRelationship(gameState.relationships, npcId, effects[npcId]);
        }
    }

    // Специальные эффекты для братьев/сестер
    if (effects.siblings) {
        const siblings = ['kendall', 'shiv', 'roman'];
        siblings.forEach(sibId => {
            if (sibId !== gameState.selectedCharacter && gameState.relationships[sibId] !== undefined) {
                changeRelationship(gameState.relationships, sibId, effects.siblings);
            }
        });
    }

    updateAllUI();
}

// Ограничить значение
function clamp(value, min, max) {
    return Math.min(Math.max(value, min), max);
}

// Продвинуть время
function advanceTime() {
    gameState.day++;

    // Каждые 7 дней - новая неделя
    if (gameState.day % 7 === 1 && gameState.day > 1) {
        gameState.week++;

        // Каждые 4 недели - новый месяц
        if (gameState.week % 4 === 1 && gameState.week > 1) {
            gameState.month++;
            if (gameState.month <= 12) {
                gameState.monthName = MONTHS[gameState.month - 1];
            }
        }

        // Загрузить событие для новой недели
        loadWeekEvent();
    } else {
        // Обычный день - случайное событие или отдых
        const randomEvent = checkRandomEvent(gameState);
        if (randomEvent) {
            displayEvent(randomEvent);
        } else {
            displayDailyUpdate();
        }
    }

    updateAllUI();
}

// Загрузить событие недели
function loadWeekEvent() {
    const event = getEventForWeek(gameState.week);
    if (event) {
        displayEvent(event);
    } else {
        displayDailyUpdate();
    }
}

// Показать ежедневное обновление
function displayDailyUpdate() {
    const updates = [
        'Обычный рабочий день. Встречи, звонки, email...',
        'Вы проводите время в офисе, работая над текущими проектами.',
        'День проходит в рутинной работе.',
        'Встречи с командой и планирование следующих шагов.',
        'Вы анализируете финансовые отчеты и тренды рынка.'
    ];

    const eventCard = document.getElementById('current-event');
    const eventTitle = eventCard.querySelector('.event-title');
    const eventDescription = eventCard.querySelector('.event-description');
    const eventChoices = document.getElementById('event-choices');

    eventTitle.textContent = `День ${gameState.day}`;
    eventDescription.innerHTML = `<p>${updates[Math.floor(Math.random() * updates.length)]}</p>`;

    eventChoices.innerHTML = '';
    const button = document.createElement('button');
    button.className = 'choice-btn';
    button.textContent = 'Продолжить';
    button.onclick = () => advanceTime();
    eventChoices.appendChild(button);

    // Небольшое восстановление здоровья
    if (gameState.stats.health < 100) {
        gameState.stats.health = Math.min(100, gameState.stats.health + 2);
    }
}

// Найти событие по ID
function findEventById(eventId) {
    for (const monthKey in EVENTS_DATABASE) {
        const events = EVENTS_DATABASE[monthKey];
        const found = events.find(e => e.id === eventId);
        if (found) return found;
    }
    return null;
}

// Добавить новость
function addNews(newsText) {
    if (newsText === 'Нет новостей') return;

    gameState.news.unshift({
        time: `День ${gameState.day}`,
        text: newsText
    });

    // Оставляем только последние 10 новостей
    if (gameState.news.length > 10) {
        gameState.news = gameState.news.slice(0, 10);
    }

    updateNewsUI();
}

// Обновить все UI
function updateAllUI() {
    updateStatsUI();
    updateTimeUI();
    updateRelationshipsUI();
    updateNewsUI();
}

// Обновить статистику
function updateStatsUI() {
    // Влияние
    document.getElementById('influence-bar').style.width = gameState.stats.influence + '%';
    document.getElementById('influence-value').textContent = `${gameState.stats.influence}/100`;

    // Репутация
    document.getElementById('reputation-bar').style.width = gameState.stats.reputation + '%';
    document.getElementById('reputation-value').textContent = `${gameState.stats.reputation}/100`;

    // Капитал
    document.getElementById('wealth-bar').style.width = Math.min(100, (gameState.stats.wealth / 10)); // масштабируем
    document.getElementById('wealth-value').textContent = `$${gameState.stats.wealth}M`;

    // Здоровье
    document.getElementById('health-bar').style.width = gameState.stats.health + '%';
    document.getElementById('health-value').textContent = `${gameState.stats.health}/100`;
}

// Обновить время
function updateTimeUI() {
    document.getElementById('current-day').textContent = gameState.day;
    document.getElementById('current-week').textContent = gameState.week;
    document.getElementById('current-month').textContent = gameState.monthName;
}

// Обновить отношения
function updateRelationshipsUI() {
    const container = document.getElementById('relationships-list');
    container.innerHTML = '';

    // Показываем только ключевых персонажей
    const keyNPCs = ['logan', 'shiv', 'kendall', 'roman', 'tom', 'gerri', 'stewy'];

    keyNPCs.forEach(npcId => {
        if (npcId === gameState.selectedCharacter) return; // не показываем себя

        const npc = getNPCInfo(npcId) || getCharacterInfo(npcId);
        if (!npc) return;

        const value = gameState.relationships[npcId] || 50;
        const status = getRelationshipStatus(value);

        const item = document.createElement('div');
        item.className = 'relationship-item';
        item.innerHTML = `
            <span class="relationship-name">${npc.name}</span>
            <span class="relationship-value ${status.status}">${value}</span>
        `;
        container.appendChild(item);
    });
}

// Обновить новости
function updateNewsUI() {
    const container = document.getElementById('news-list');
    container.innerHTML = '';

    gameState.news.forEach(news => {
        const item = document.createElement('div');
        item.className = 'news-item';
        item.innerHTML = `
            <span class="news-time">${news.time}</span>
            <p>${news.text}</p>
        `;
        container.appendChild(item);
    });
}

// Показать меню
function showMenu() {
    document.getElementById('menu-modal').classList.add('active');
}

// Закрыть меню
function closeMenu() {
    document.getElementById('menu-modal').classList.remove('active');
}

// Сохранить игру
function saveGame() {
    try {
        localStorage.setItem('succession_game_save', JSON.stringify(gameState));
        alert('Игра сохранена!');
    } catch (e) {
        alert('Ошибка сохранения: ' + e.message);
    }
}

// Загрузить игру
function loadGame() {
    try {
        const saved = localStorage.getItem('succession_game_save');
        if (saved) {
            gameState = JSON.parse(saved);

            // Восстановить UI
            if (gameState.selectedCharacter) {
                const character = getCharacterInfo(gameState.selectedCharacter);
                selectCharacter(gameState.selectedCharacter);
                showScreen('game-screen');
                updateAllUI();

                // Загрузить текущее событие или обновление
                if (gameState.currentEvent) {
                    displayEvent(gameState.currentEvent);
                } else {
                    loadWeekEvent();
                }
            }

            alert('Игра загружена!');
            closeMenu();
        } else {
            alert('Нет сохраненной игры');
        }
    } catch (e) {
        alert('Ошибка загрузки: ' + e.message);
    }
}

// Загрузить состояние при старте
function loadGameState() {
    const saved = localStorage.getItem('succession_game_save');
    if (saved) {
        try {
            const savedState = JSON.parse(saved);
            // Проверяем, есть ли активная игра
            if (savedState.gameStarted) {
                // Предлагаем продолжить
                if (confirm('Найдена сохраненная игра. Продолжить?')) {
                    gameState = savedState;
                    if (gameState.selectedCharacter) {
                        selectCharacter(gameState.selectedCharacter);
                        showScreen('game-screen');
                        updateAllUI();
                        if (gameState.currentEvent) {
                            displayEvent(gameState.currentEvent);
                        } else {
                            loadWeekEvent();
                        }
                    }
                }
            }
        } catch (e) {
            console.error('Ошибка загрузки:', e);
        }
    }
}

// Перезапустить игру
function restartGame() {
    if (confirm('Вы уверены? Весь прогресс будет потерян.')) {
        localStorage.removeItem('succession_game_save');
        location.reload();
    }
}

// Показать окончание игры
function showGameEnd() {
    const eventCard = document.getElementById('current-event');
    const eventTitle = eventCard.querySelector('.event-title');
    const eventDescription = eventCard.querySelector('.event-description');
    const eventChoices = document.getElementById('event-choices');

    // Определяем концовку на основе статистики
    let ending = determineEnding();

    eventTitle.textContent = ending.title;
    eventDescription.innerHTML = ending.description;

    eventChoices.innerHTML = '';
    const button = document.createElement('button');
    button.className = 'btn-primary';
    button.textContent = 'Начать заново';
    button.onclick = () => restartGame();
    eventChoices.appendChild(button);
}

// Определить концовку
function determineEnding() {
    const stats = gameState.stats;
    const loganRelation = gameState.relationships.logan || 50;

    // Лучшая концовка - стать CEO
    if (stats.influence >= 70 && loganRelation >= 70 && stats.reputation >= 60) {
        return {
            title: 'Победа: Новый CEO',
            description: `
                <p>Логан смотрит на вас с... гордостью? Это редкое выражение на его лице.</p>
                <p>"Ты доказал, что достоин. Waystar Royco теперь твоя ответственность. Не разочаруй меня."</p>
                <p><strong>Вы стали CEO Waystar Royco!</strong></p>
                <p>Итоговые характеристики:</p>
                <p>💼 Влияние: ${stats.influence}/100</p>
                <p>⭐ Репутация: ${stats.reputation}/100</p>
                <p>💰 Капитал: $${stats.wealth}M</p>
                <p>❤️ Здоровье: ${stats.health}/100</p>
            `
        };
    }

    // Хорошая концовка - важная роль
    if (stats.influence >= 50 && loganRelation >= 50) {
        return {
            title: 'Успех: Место в совете',
            description: `
                <p>"Ты не готов быть CEO," - говорит Логан. "Но ты заслужил место в совете директоров."</p>
                <p>Это не то, на что вы надеялись, но это важная позиция. Игра продолжается.</p>
                <p><strong>Вы получили место в совете директоров.</strong></p>
                <p>Итоговые характеристики:</p>
                <p>💼 Влияние: ${stats.influence}/100</p>
                <p>⭐ Репутация: ${stats.reputation}/100</p>
            `
        };
    }

    // Средняя концовка - остались в компании
    if (stats.influence >= 30) {
        return {
            title: 'Сохранение статуса',
            description: `
                <p>Логан выбрал другого преемника. Вы остаетесь в компании, но без повышения.</p>
                <p>"Продолжай работать. Может быть, когда-нибудь ты будешь готов."</p>
                <p><strong>Вы остались на текущей позиции.</strong></p>
                <p>Итоговые характеристики:</p>
                <p>💼 Влияние: ${stats.influence}/100</p>
                <p>⭐ Репутация: ${stats.reputation}/100</p>
            `
        };
    }

    // Плохая концовка - вылетели
    return {
        title: 'Поражение: Изгнание',
        description: `
            <p>Логан смотрит на вас с презрением.</p>
            <p>"Ты разочаровал меня. Уходи. Я не хочу тебя больше видеть в этой компании."</p>
            <p><strong>Вы покинули Waystar Royco.</strong></p>
            <p>Итоговые характеристики:</p>
            <p>💼 Влияние: ${stats.influence}/100</p>
            <p>⭐ Репутация: ${stats.reputation}/100</p>
            <p>💰 Капитал: $${stats.wealth}M</p>
        `
    };
}

// Обновить UI при загрузке
function updateUI() {
    if (gameState.gameStarted) {
        updateAllUI();
    }
}

// Инициализация при загрузке страницы
window.addEventListener('DOMContentLoaded', initGame);

// Автосохранение каждые 2 минуты
setInterval(() => {
    if (gameState.gameStarted) {
        saveGame();
    }
}, 120000);
