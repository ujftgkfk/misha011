// Media Mogul: Internationalization (i18n)

const TRANSLATIONS = {
    en: {
        // Header
        gameTitle: "MEDIA MOGUL: The Warner Bros. War",
        currentDate: "Current Date",
        daysToDeadline: "Days to deadline",

        // Resources
        resources: "Resources",
        cash: "Cash",
        stockValue: "Stock Value",
        politicalInfluence: "Political Influence",
        reputation: "Reputation",

        // Bid Status
        bidStatus: "Current Bid Status",
        yourOffer: "Your Offer",
        competitors: "Competitors",
        withdrawn: "Withdrawn",

        // Actions
        negotiate: "Negotiate",
        finance: "Finance",
        politics: "Politics",
        shareholders: "Shareholders",
        nextDay: "Next Day",

        // Key People
        keyPeople: "Key People",
        relationship: "Relationship",

        // Intelligence
        intelligence: "Intelligence",

        // NPC Titles
        ceo_wbd: "CEO, Warner Bros. Discovery",
        president: "President of the United States",
        doj_chief: "DOJ Antitrust Chief",
        ftc_chair: "FTC Chair",
        oracle_founder: "Founder, Oracle",

        // Moods
        neutral: "Neutral",
        watching: "Watching",
        skeptical: "Skeptical",
        concerned: "Concerned",
        supportive: "Supportive",
        veryPositive: "Very Positive",
        positive: "Positive",
        negative: "Negative",
        veryNegative: "Very Negative",

        // Welcome Screen
        welcomeTitle: "Welcome to Media Mogul",
        welcomeText1: "September 2025. Warner Bros. Discovery is up for sale.",
        welcomeText2: "As CEO of {company}, you must outbid Netflix and Comcast to secure the deal of the century.",
        welcomeText3: "Use your resources wisely:",
        welcomeList1: "Cash - Make competitive offers",
        welcomeList2: "Political Influence - Lobby regulators and Trump",
        welcomeList3: "Reputation - Win over shareholders and the board",
        welcomeText4: "You have 120 days until the final deadline.",
        startGame: "Start Game",
        continueGame: "Continue Saved Game",

        // Main Screen
        dayTitle: "Day {day}",
        whatToDo: "What would you like to do today?",
        availableActions: "Available Actions:",
        actionNegotiate: "Meet with key decision makers",
        actionFinance: "Secure funding and manage resources",
        actionPolitics: "Lobby regulators and build influence",
        actionShareholders: "Win over institutional investors",

        // Negotiations
        availableMeetings: "Available Meetings",
        scheduleMeeting: "Schedule Meeting",
        callTrump: "Call Trump",
        locked: "Locked",
        requires: "Requires {amount}+ political influence",
        keyDecisionMaker: "The key decision maker",
        canProvide: "Can provide political cover",
        yourResponse: "Your Response:",

        // Finance Panel
        financialResources: "Financial Resources",
        availableCash: "Available Cash:",
        debtCapacity: "Debt Capacity:",
        totalCapacity: "Total Capacity:",
        raiseYourBid: "Raise Your Bid",
        currentBid: "Current bid:",
        totalDealValue: "Total deal value:",
        newBidPerShare: "New bid per share:",
        raiseBid: "Raise Bid",
        financingSources: "Financing Sources",
        comingSoon: "Coming soon: Detailed financing options",

        // Politics Panel
        politicalActions: "Political Actions",
        cooldown: "Cooldown: {days} days",
        execute: "Execute",

        // Shareholders Panel
        majorShareholders: "Major Shareholders",
        ownership: "ownership",
        support: "Support:",

        // Events
        recentEvents: "Recent Events",
        day: "Day",
        gameStarted: "Game started. The battle for Warner Bros. Discovery begins!",

        // Dialogue
        meetingWith: "Meeting with {name}",
        result: "Result",
        youChose: "You chose:",
        effects: "Effects:",
        continue: "Continue",

        // Choice Effects
        cost: "Cost",
        risk: "Risk",

        // Notifications
        gameLoaded: "Game loaded!",
        gameSaved: "Game saved!",
        bidIncreased: "Bid increased successfully!",
        notEnoughCash: "Not enough cash!",
        notEnoughInfluence: "Not enough political influence!",
        actionExecuted: "{action} executed successfully!",
        actionOnCooldown: "Action on cooldown for {days} more days!",
        bidTooLow: "New bid must be higher than current bid!",
        notEnoughFinancing: "Not enough financing available!",

        // Game End
        victory: "Victory!",
        timeUp: "Time's Up!",
        bankruptcy: "Bankruptcy!",
        blocked: "Blocked!",
        gameOver: "Game Over",
        victoryMessage: "Congratulations! You successfully acquired Warner Bros. Discovery for ${bid}/share!",
        timeUpMessage: "The deadline has passed and you failed to secure the deal.",
        bankruptcyMessage: "You ran out of money and can't continue the bid.",
        antitrustMessage: "Regulators have blocked your acquisition on antitrust grounds.",
        playAgain: "Play Again",

        // Final Stats
        finalStatistics: "Final Statistics:",
        daysPlayed: "Days played:",
        finalBid: "Final bid:",
        cashRemaining: "Cash remaining:",
        finalReputation: "Reputation:",
        finalInfluence: "Political influence:",

        // Political Actions
        lobbyDOJ: "Lobby Department of Justice",
        lobbyDOJDesc: "Hire top lawyers and lobbyists to make your case to the DOJ Antitrust Division.",
        lobbyFTC: "Lobby FTC",
        lobbyFTCDesc: "Present your case to the Federal Trade Commission.",
        callTrumpAction: "Call Trump",
        callTrumpDesc: "Reach out to President Trump for support.",
        mediaCampaign: "Public Media Campaign",
        mediaCampaignDesc: "Launch a PR campaign to build public support.",
        shareholderPresentation: "Investor Roadshow",
        shareholderPresentationDesc: "Present your vision to major institutional shareholders.",

        // Bidding Rounds
        biddingRound: "Bidding Round {round}",
        date: "Date:",
        minimumBid: "Minimum bid:",
        chanceToMakeBid: "This is your chance to make a competitive offer!",
        makeYourBid: "Make Your Bid",

        // Events
        successIcon: "✅",
        failureIcon: "❌",
        approachWorked: "Your approach worked!",
        didntGoAsPlanned: "That didn't go as planned...",

        // Relationship changes
        relationshipWith: "Relationship with {name}:",

        // Language
        language: "Language",
        english: "English",
        russian: "Русский"
    },

    ru: {
        // Header
        gameTitle: "МЕДИА МАГНАТ: Война за Warner Bros.",
        currentDate: "Текущая дата",
        daysToDeadline: "Дней до дедлайна",

        // Resources
        resources: "Ресурсы",
        cash: "Наличные",
        stockValue: "Стоимость акций",
        politicalInfluence: "Политическое влияние",
        reputation: "Репутация",

        // Bid Status
        bidStatus: "Статус ставки",
        yourOffer: "Ваше предложение:",
        competitors: "Конкуренты:",
        withdrawn: "Вышел",

        // Actions
        negotiate: "Переговоры",
        finance: "Финансы",
        politics: "Политика",
        shareholders: "Акционеры",
        nextDay: "Следующий день",

        // Key People
        keyPeople: "Ключевые люди",
        relationship: "Отношения",

        // Intelligence
        intelligence: "Разведданные",

        // NPC Titles
        ceo_wbd: "CEO, Warner Bros. Discovery",
        president: "Президент США",
        doj_chief: "Глава антимонопольного отдела Минюста",
        ftc_chair: "Председатель FTC",
        oracle_founder: "Основатель Oracle",

        // Moods
        neutral: "Нейтрально",
        watching: "Наблюдает",
        skeptical: "Скептичен",
        concerned: "Озабочен",
        supportive: "Поддерживает",
        veryPositive: "Очень позитивно",
        positive: "Позитивно",
        negative: "Негативно",
        veryNegative: "Очень негативно",

        // Welcome Screen
        welcomeTitle: "Добро пожаловать в Media Mogul",
        welcomeText1: "Сентябрь 2025. Warner Bros. Discovery выставлен на продажу.",
        welcomeText2: "Как CEO компании {company}, вы должны обыграть Netflix и Comcast, чтобы заключить сделку века.",
        welcomeText3: "Используйте свои ресурсы с умом:",
        welcomeList1: "Наличные - Делайте конкурентные предложения",
        welcomeList2: "Политическое влияние - Лоббируйте регуляторов и Трампа",
        welcomeList3: "Репутация - Завоюйте акционеров и совет директоров",
        welcomeText4: "У вас есть 120 дней до финального дедлайна.",
        startGame: "Начать игру",
        continueGame: "Продолжить сохраненную игру",

        // Main Screen
        dayTitle: "День {day}",
        whatToDo: "Что вы хотите сделать сегодня?",
        availableActions: "Доступные действия:",
        actionNegotiate: "Встречи с ключевыми фигурами",
        actionFinance: "Управление финансами и ресурсами",
        actionPolitics: "Лоббирование регуляторов и наращивание влияния",
        actionShareholders: "Работа с институциональными инвесторами",

        // Negotiations
        availableMeetings: "Доступные встречи",
        scheduleMeeting: "Назначить встречу",
        callTrump: "Позвонить Трампу",
        locked: "Заблокировано",
        requires: "Требуется {amount}+ политического влияния",
        keyDecisionMaker: "Главный судья",
        canProvide: "Может обеспечить политическую поддержку",
        yourResponse: "Ваш ответ:",

        // Finance Panel
        financialResources: "Финансовые ресурсы",
        availableCash: "Доступные наличные:",
        debtCapacity: "Долговая емкость:",
        totalCapacity: "Общая емкость:",
        raiseYourBid: "Повысить ставку",
        currentBid: "Текущая ставка:",
        totalDealValue: "Общая стоимость сделки:",
        newBidPerShare: "Новая ставка за акцию:",
        raiseBid: "Повысить ставку",
        financingSources: "Источники финансирования",
        comingSoon: "Скоро: Детальные опции финансирования",

        // Politics Panel
        politicalActions: "Политические действия",
        cooldown: "Перезарядка: {days} дней",
        execute: "Выполнить",

        // Shareholders Panel
        majorShareholders: "Крупные акционеры",
        ownership: "владение",
        support: "Поддержка:",

        // Events
        recentEvents: "Последние события",
        day: "День",
        gameStarted: "Игра началась. Битва за Warner Bros. Discovery начинается!",

        // Dialogue
        meetingWith: "Встреча с {name}",
        result: "Результат",
        youChose: "Вы выбрали:",
        effects: "Эффекты:",
        continue: "Продолжить",

        // Choice Effects
        cost: "Цена",
        risk: "Риск",

        // Notifications
        gameLoaded: "Игра загружена!",
        gameSaved: "Игра сохранена!",
        bidIncreased: "Ставка успешно повышена!",
        notEnoughCash: "Недостаточно наличных!",
        notEnoughInfluence: "Недостаточно политического влияния!",
        actionExecuted: "{action} выполнено успешно!",
        actionOnCooldown: "Действие на перезарядке еще {days} дней!",
        bidTooLow: "Новая ставка должна быть выше текущей!",
        notEnoughFinancing: "Недостаточно доступного финансирования!",

        // Game End
        victory: "Победа!",
        timeUp: "Время вышло!",
        bankruptcy: "Банкротство!",
        blocked: "Заблокировано!",
        gameOver: "Игра окончена",
        victoryMessage: "Поздравляем! Вы успешно приобрели Warner Bros. Discovery за ${bid}/акцию!",
        timeUpMessage: "Дедлайн прошел, и вы не смогли заключить сделку.",
        bankruptcyMessage: "У вас закончились деньги, и вы не можете продолжить торги.",
        antitrustMessage: "Регуляторы заблокировали ваше поглощение по антимонопольным основаниям.",
        playAgain: "Играть снова",

        // Final Stats
        finalStatistics: "Финальная статистика:",
        daysPlayed: "Дней сыграно:",
        finalBid: "Финальная ставка:",
        cashRemaining: "Осталось наличных:",
        finalReputation: "Репутация:",
        finalInfluence: "Политическое влияние:",

        // Political Actions
        lobbyDOJ: "Лоббировать Министерство юстиции",
        lobbyDOJDesc: "Нанять топовых юристов и лоббистов для работы с антимонопольным отделом Минюста.",
        lobbyFTC: "Лоббировать FTC",
        lobbyFTCDesc: "Представить ваше дело Федеральной торговой комиссии.",
        callTrumpAction: "Позвонить Трампу",
        callTrumpDesc: "Обратиться к президенту Трампу за поддержкой.",
        mediaCampaign: "Публичная медиа-кампания",
        mediaCampaignDesc: "Запустить PR-кампанию для создания общественной поддержки.",
        shareholderPresentation: "Роудшоу для инвесторов",
        shareholderPresentationDesc: "Представить ваше видение крупным институциональным акционерам.",

        // Bidding Rounds
        biddingRound: "Раунд торгов {round}",
        date: "Дата:",
        minimumBid: "Минимальная ставка:",
        chanceToMakeBid: "Это ваш шанс сделать конкурентное предложение!",
        makeYourBid: "Сделать ставку",

        // Events
        successIcon: "✅",
        failureIcon: "❌",
        approachWorked: "Ваш подход сработал!",
        didntGoAsPlanned: "Всё пошло не по плану...",

        // Relationship changes
        relationshipWith: "Отношения с {name}:",

        // Language
        language: "Язык",
        english: "English",
        russian: "Русский"
    }
};

// i18n System
class I18n {
    constructor() {
        this.currentLanguage = 'en';
        this.storageKey = 'mediaMogulLanguage';
        this.loadLanguage();
    }

    // Load saved language
    loadLanguage() {
        const saved = localStorage.getItem(this.storageKey);
        if (saved && TRANSLATIONS[saved]) {
            this.currentLanguage = saved;
        } else {
            // Auto-detect browser language
            const browserLang = navigator.language || navigator.userLanguage;
            if (browserLang.startsWith('ru')) {
                this.currentLanguage = 'ru';
            }
        }
    }

    // Save language preference
    saveLanguage() {
        localStorage.setItem(this.storageKey, this.currentLanguage);
    }

    // Get translation
    t(key, params = {}) {
        let translation = TRANSLATIONS[this.currentLanguage][key];

        if (!translation) {
            console.warn(`Translation missing for key: ${key} in language: ${this.currentLanguage}`);
            return key;
        }

        // Replace parameters
        Object.keys(params).forEach(param => {
            translation = translation.replace(`{${param}}`, params[param]);
        });

        return translation;
    }

    // Switch language
    setLanguage(lang) {
        if (TRANSLATIONS[lang]) {
            this.currentLanguage = lang;
            this.saveLanguage();
            return true;
        }
        return false;
    }

    // Get current language
    getLanguage() {
        return this.currentLanguage;
    }

    // Get available languages
    getAvailableLanguages() {
        return Object.keys(TRANSLATIONS);
    }
}

// Create global i18n instance
if (typeof window !== 'undefined') {
    window.i18n = new I18n();
}
