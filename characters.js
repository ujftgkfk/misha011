// Определение всех персонажей игры

const CHARACTERS = {
    kendall: {
        id: 'kendall',
        name: 'Кендалл Рой',
        position: 'Вице-президент',
        description: 'Старший сын Логана, амбициозный и непредсказуемый. Хочет доказать отцу свою ценность.',
        stats: {
            influence: 50,
            reputation: 60,
            wealth: 500,
            health: 100,
            business: 85,
            charisma: 70,
            intelligence: 80
        },
        traits: ['Амбициозный', 'Импульсивный', 'Стратег'],
        weaknesses: ['Зависимости', 'Неуверенность'],
        avatar: 'kendall'
    },
    shiv: {
        id: 'shiv',
        name: 'Шив Рой',
        position: 'Политический консультант',
        description: 'Единственная дочь Логана. Умна, расчетлива и амбициозна.',
        stats: {
            influence: 45,
            reputation: 70,
            wealth: 400,
            health: 100,
            business: 75,
            charisma: 85,
            intelligence: 90
        },
        traits: ['Манипулятор', 'Умная', 'Холодная'],
        weaknesses: ['Доверие', 'Семья'],
        avatar: 'shiv'
    },
    roman: {
        id: 'roman',
        name: 'Роман Рой',
        position: 'COO Waystar Royco',
        description: 'Младший сын, циничный и саркастичный. Скрывает свои истинные чувства за юмором.',
        stats: {
            influence: 40,
            reputation: 55,
            wealth: 450,
            health: 100,
            business: 70,
            charisma: 80,
            intelligence: 75
        },
        traits: ['Саркастичный', 'Циничный', 'Ранимый'],
        weaknesses: ['Эмоции', 'Серьезность'],
        avatar: 'roman'
    },
    tom: {
        id: 'tom',
        name: 'Том Вамбсганс',
        position: 'Глава ATN News',
        description: 'Муж Шив, жаждет признания и власти. Готов на все ради успеха.',
        stats: {
            influence: 35,
            reputation: 50,
            wealth: 300,
            health: 100,
            business: 65,
            charisma: 75,
            intelligence: 70
        },
        traits: ['Лояльный', 'Амбициозный', 'Гибкий'],
        weaknesses: ['Самоуважение', 'Власть'],
        avatar: 'tom'
    }
};

// NPC персонажи
const NPC_CHARACTERS = {
    logan: {
        id: 'logan',
        name: 'Логан Рой',
        position: 'CEO Waystar Royco',
        description: 'Основатель и CEO Waystar Royco. Безжалостный магнат, который держит всех в постоянном напряжении.',
        influence: 100,
        relationship: 40
    },
    connor: {
        id: 'connor',
        name: 'Коннор Рой',
        position: 'Старший брат',
        description: 'Старший сын от первого брака. Эксцентричный и отстраненный от бизнеса.',
        influence: 20,
        relationship: 60
    },
    marcia: {
        id: 'marcia',
        name: 'Марсия Рой',
        position: 'Жена Логана',
        description: 'Третья жена Логана. Умная и расчетливая.',
        influence: 50,
        relationship: 50
    },
    frank: {
        id: 'frank',
        name: 'Фрэнк Вернон',
        position: 'COO (ранее)',
        description: 'Старый друг семьи и бывший COO. Опытный советник.',
        influence: 60,
        relationship: 55
    },
    gerri: {
        id: 'gerri',
        name: 'Герри Келлман',
        position: 'Главный юрисконсульт',
        description: 'Умная и прагматичная юрист компании.',
        influence: 70,
        relationship: 50
    },
    karl: {
        id: 'karl',
        name: 'Карл Муллер',
        position: 'CFO',
        description: 'Финансовый директор с многолетним опытом.',
        influence: 55,
        relationship: 50
    },
    greg: {
        id: 'greg',
        name: 'Грег Хирш',
        position: 'Ассистент',
        description: 'Внучатый племянник Логана. Неуклюжий, но амбициозный.',
        influence: 25,
        relationship: 60
    },
    stewy: {
        id: 'stewy',
        name: 'Стьюи Хоскенни',
        position: 'Инвестор',
        description: 'Бывший друг Кендалла, теперь враг номер один.',
        influence: 75,
        relationship: 30
    },
    sandy: {
        id: 'sandy',
        name: 'Сэнди Фернесс',
        position: 'Инвестор',
        description: 'Враждебный инвестор, желающий получить контроль.',
        influence: 80,
        relationship: 20
    }
};

// Начальные отношения между персонажами
const INITIAL_RELATIONSHIPS = {
    kendall: {
        logan: 40,
        shiv: 45,
        roman: 60,
        connor: 55,
        tom: 50,
        greg: 65,
        gerri: 55,
        frank: 60,
        stewy: 30,
        sandy: 20
    },
    shiv: {
        logan: 50,
        kendall: 45,
        roman: 55,
        connor: 50,
        tom: 70,
        greg: 55,
        gerri: 60,
        frank: 55,
        marcia: 40
    },
    roman: {
        logan: 45,
        kendall: 60,
        shiv: 55,
        connor: 60,
        gerri: 75,
        greg: 60,
        karl: 50
    },
    tom: {
        logan: 55,
        shiv: 70,
        kendall: 50,
        roman: 55,
        greg: 80,
        gerri: 50
    }
};

// Функция получения начальных отношений для персонажа
function getInitialRelationships(characterId) {
    const relationships = {};
    const charRelations = INITIAL_RELATIONSHIPS[characterId] || {};

    for (const npcId in NPC_CHARACTERS) {
        relationships[npcId] = charRelations[npcId] || 50;
    }

    // Добавляем других игровых персонажей (если нужно)
    for (const charId in CHARACTERS) {
        if (charId !== characterId && charRelations[charId]) {
            relationships[charId] = charRelations[charId];
        }
    }

    return relationships;
}

// Функция для получения статуса отношений
function getRelationshipStatus(value) {
    if (value >= 70) return { status: 'positive', text: 'Союзник' };
    if (value >= 40) return { status: 'neutral', text: 'Нейтрально' };
    return { status: 'negative', text: 'Враг' };
}

// Функция для изменения отношений
function changeRelationship(relationships, characterId, delta) {
    if (relationships[characterId] !== undefined) {
        relationships[characterId] = Math.max(0, Math.min(100, relationships[characterId] + delta));
    }
}

// Получение информации о NPC
function getNPCInfo(npcId) {
    return NPC_CHARACTERS[npcId] || null;
}

// Получение информации о персонаже игрока
function getCharacterInfo(characterId) {
    return CHARACTERS[characterId] || null;
}
