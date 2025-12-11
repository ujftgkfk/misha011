// Media Mogul: Main Entry Point

// Wait for DOM to be ready
document.addEventListener('DOMContentLoaded', function() {
    console.log('🎮 Media Mogul: The Warner Bros. War');
    console.log('Loading game...');

    // Initialize game systems
    initializeGame();

    // Check for saved game
    checkForSavedGame();

    console.log('✅ Game loaded successfully!');
});

// Initialize all game systems
function initializeGame() {
    // Initialize UI
    window.UI.init();

    // Initialize language and apply translations
    const currentLang = window.i18n.getLanguage();
    document.querySelectorAll('.lang-btn').forEach(btn => {
        btn.classList.remove('active');
        if (btn.dataset.lang === currentLang) {
            btn.classList.add('active');
        }
    });
    window.UI.updateTranslations();

    // Initialize game engine
    // Game is initialized when player clicks "Start Game"

    // Initialize events system
    window.Events = new EventsSystem();

    // Initialize negotiations system
    // Already initialized in negotiations.js

    // Initialize financing system
    if (typeof FinancingSystem !== 'undefined') {
        window.Financing = new FinancingSystem();
        console.log('✅ Financing system initialized');
    }

    // Initialize achievements system
    if (typeof AchievementsSystem !== 'undefined') {
        window.Achievements = new AchievementsSystem();
        console.log('✅ Achievements system initialized');
    }

    // Initialize statistics system
    if (typeof StatisticsSystem !== 'undefined') {
        window.Statistics = new StatisticsSystem();
        console.log('✅ Statistics system initialized');
    }

    // Setup keyboard shortcuts
    setupKeyboardShortcuts();

    // Setup auto-save
    setupAutoSave();
}

// Check for saved game
function checkForSavedGame() {
    const hasSave = window.Game.loadGame();

    if (hasSave) {
        const state = window.Game.getState();

        // Show notification
        const loadBtn = document.createElement('button');
        loadBtn.setAttribute('data-i18n', 'continueGame');
        loadBtn.textContent = window.i18n.t('continueGame');
        loadBtn.className = 'btn-large btn-primary';
        loadBtn.style.marginTop = '20px';
        loadBtn.onclick = function() {
            window.UI.showMainGameScreen();
            window.UI.render();
            window.UI.updateEventLog();
            window.UI.showNotification(window.i18n.t('gameLoaded'), 'success');
        };

        // Add to welcome screen
        const welcomeScreen = document.querySelector('.welcome-screen');
        if (welcomeScreen) {
            welcomeScreen.appendChild(loadBtn);
        }
    }
}

// Setup keyboard shortcuts
function setupKeyboardShortcuts() {
    document.addEventListener('keydown', function(e) {
        // Don't trigger if typing in input
        if (e.target.tagName === 'INPUT' || e.target.tagName === 'TEXTAREA') {
            return;
        }

        // Space or Enter - Next turn
        if (e.code === 'Space' || e.code === 'Enter') {
            e.preventDefault();
            const nextTurnBtn = document.getElementById('btn-next-turn');
            if (nextTurnBtn && !nextTurnBtn.disabled) {
                nextTurnBtn.click();
            }
        }

        // Number keys for quick actions
        if (e.code === 'Digit1' || e.code === 'Numpad1') {
            document.getElementById('btn-negotiate')?.click();
        }
        if (e.code === 'Digit2' || e.code === 'Numpad2') {
            document.getElementById('btn-finance')?.click();
        }
        if (e.code === 'Digit3' || e.code === 'Numpad3') {
            document.getElementById('btn-politics')?.click();
        }
        if (e.code === 'Digit4' || e.code === 'Numpad4') {
            document.getElementById('btn-shareholders')?.click();
        }

        // Escape - Close modal
        if (e.code === 'Escape') {
            window.UI.hideModal();
        }

        // S - Save game manually
        if (e.code === 'KeyS' && e.ctrlKey) {
            e.preventDefault();
            window.Game.saveGame();
            window.UI.showNotification('Game saved!', 'success');
        }
    });
}

// Setup auto-save every minute
function setupAutoSave() {
    setInterval(function() {
        if (window.Game && window.Game.state.isGameActive) {
            window.Game.saveGame();
            console.log('🔄 Auto-saved');
        }
    }, 60000); // Every 60 seconds
}

// Extended game loop - called every turn
function extendedGameLoop() {
    const state = window.Game.getState();

    // Check story events
    window.Events.checkStoryEvents(state);

    // Check special conditions
    window.Events.checkSpecialConditions(state);

    // Random encounters
    if (Math.random() < 0.15) {
        window.Negotiations.triggerRandomEncounter();
    }

    // Update UI
    window.UI.render();
    window.UI.updateEventLog();
}

// Monkey-patch the game's nextDay to include extended loop
if (window.Game) {
    const originalNextDay = window.Game.nextDay.bind(window.Game);

    window.Game.nextDay = function() {
        originalNextDay();
        extendedGameLoop();
    };
}

// Debug functions (accessible from console)
window.DEBUG = {
    // Add resources
    addCash: (amount) => {
        window.Game.modifyCash(amount);
        window.UI.render();
        console.log(`Added $${amount}B cash`);
    },

    addInfluence: (amount) => {
        window.Game.modifyInfluence(amount);
        window.UI.render();
        console.log(`Added ${amount} influence`);
    },

    addReputation: (amount) => {
        window.Game.modifyReputation(amount);
        window.UI.render();
        console.log(`Added ${amount} reputation`);
    },

    // Set relationship
    setRelationship: (npcId, value) => {
        window.Game.state.relationships[npcId] = value;
        window.UI.render();
        console.log(`Set ${npcId} relationship to ${value}`);
    },

    // Jump to day
    jumpToDay: (day) => {
        window.Game.state.currentDay = day;
        window.UI.render();
        console.log(`Jumped to day ${day}`);
    },

    // Trigger specific event
    triggerEvent: (eventId) => {
        const allEvents = [
            ...GAME_DATA.events.positive,
            ...GAME_DATA.events.negative,
            ...GAME_DATA.events.neutral
        ];

        const event = allEvents.find(e => e.id === eventId);
        if (event) {
            window.Game.applyEvent(event, event.type || 'neutral');
            console.log(`Triggered event: ${eventId}`);
        } else {
            console.error(`Event not found: ${eventId}`);
        }
    },

    // Win the game instantly
    win: () => {
        window.Game.state.currentBid = GAME_DATA.config.min_winning_bid;
        window.Game.state.relationships.zaslav = 80;
        window.Game.checkGameEnd();
        console.log('🏆 Instant win!');
    },

    // Show all game data
    showState: () => {
        console.log('📊 Current Game State:');
        console.table(window.Game.getState());
    },

    // List all available events
    listEvents: () => {
        console.log('📋 Available Events:');
        const allEvents = [
            ...GAME_DATA.events.positive.map(e => ({...e, type: 'positive'})),
            ...GAME_DATA.events.negative.map(e => ({...e, type: 'negative'})),
            ...GAME_DATA.events.neutral.map(e => ({...e, type: 'neutral'}))
        ];
        console.table(allEvents.map(e => ({
            id: e.id,
            title: e.title,
            type: e.type,
            probability: e.probability || 'N/A'
        })));
    },

    // Reset game
    reset: () => {
        localStorage.removeItem(window.Game.saveKey);
        location.reload();
        console.log('🔄 Game reset');
    }
};

// Easter eggs and fun commands
window.konami = function() {
    console.log('🎮 Konami Code Activated!');
    window.Game.modifyCash(100);
    window.Game.modifyInfluence(50);
    window.Game.modifyReputation(50);
    window.UI.showNotification('KONAMI CODE! Resources boosted!', 'success');
    window.UI.render();
};

// Konami code listener
let konamiCode = '';
const konamiPattern = 'ArrowUpArrowUpArrowDownArrowDownArrowLeftArrowRightArrowLeftArrowRightba';

document.addEventListener('keydown', function(e) {
    konamiCode += e.key;

    if (konamiCode.length > konamiPattern.length) {
        konamiCode = konamiCode.slice(-konamiPattern.length);
    }

    if (konamiCode === konamiPattern) {
        window.konami();
        konamiCode = '';
    }
});

// Welcome message
console.log('%c🎬 Welcome to Media Mogul! 🎬', 'font-size: 20px; font-weight: bold; color: #B8860B;');
console.log('%cDebug commands available via window.DEBUG', 'color: #3b82f6;');
console.log('%cType DEBUG.showState() to see current game state', 'color: #10b981;');
console.log('%cTry the Konami Code for a surprise! ⬆️⬆️⬇️⬇️⬅️➡️⬅️➡️BA', 'color: #f59e0b;');

// Export for debugging
window.GAME_VERSION = '1.0.0';
window.GAME_BUILD = 'Alpha';
