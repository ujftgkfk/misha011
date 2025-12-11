// Media Mogul: Achievements System

class AchievementsSystem {
    constructor() {
        this.achievements = this.initializeAchievements();
        this.unlockedAchievements = this.loadUnlocked();
    }

    // Initialize all achievements
    initializeAchievements() {
        return {
            // Deal-related
            first_bid: {
                id: 'first_bid',
                name: 'First Offer',
                nameRu: 'Первое предложение',
                description: 'Make your first bid increase',
                descriptionRu: 'Сделайте первое повышение ставки',
                icon: '💰',
                rarity: 'common',
                points: 10,
                condition: (state) => state.currentBid > 30
            },
            high_roller: {
                id: 'high_roller',
                name: 'High Roller',
                nameRu: 'Крупная игра',
                description: 'Bid $35+ per share',
                descriptionRu: 'Ставка $35+ за акцию',
                icon: '💎',
                rarity: 'rare',
                points: 50,
                condition: (state) => state.currentBid >= 35
            },
            all_cash: {
                id: 'all_cash',
                name: 'Cash King',
                nameRu: 'Король наличности',
                description: 'Fund entire deal with cash',
                descriptionRu: 'Профинансируйте всю сделку наличными',
                icon: '🤑',
                rarity: 'epic',
                points: 100,
                condition: (state) => {
                    const dealCost = state.currentBid * GAME_DATA.config.wbd_shares;
                    return state.cash >= dealCost;
                }
            },

            // Relationship-related
            best_friends: {
                id: 'best_friends',
                name: 'Best Friends Forever',
                nameRu: 'Лучшие друзья',
                description: 'Reach 90+ relationship with Zaslav',
                descriptionRu: 'Достигните отношений 90+ с Zaslav',
                icon: '🤝',
                rarity: 'rare',
                points: 75,
                condition: (state) => state.relationships.zaslav >= 90
            },
            trump_card: {
                id: 'trump_card',
                name: 'Trump Card',
                nameRu: 'Козырная карта',
                description: 'Get Trump endorsement',
                descriptionRu: 'Получите поддержку Трампа',
                icon: '🎺',
                rarity: 'epic',
                points: 100,
                condition: (state) => state.relationships.trump >= 85
            },
            universal_love: {
                id: 'universal_love',
                name: 'Everybody Loves You',
                nameRu: 'Всеобщий любимец',
                description: 'All relationships above 70',
                descriptionRu: 'Все отношения выше 70',
                icon: '❤️',
                rarity: 'legendary',
                points: 200,
                condition: (state) => {
                    return Object.values(state.relationships).every(r => r >= 70);
                }
            },

            // Speed achievements
            speedrunner: {
                id: 'speedrunner',
                name: 'Speed Demon',
                nameRu: 'Спидраннер',
                description: 'Win before day 60',
                descriptionRu: 'Победите до дня 60',
                icon: '⚡',
                rarity: 'legendary',
                points: 250,
                condition: (state) => state.currentDay < 60 && state.gameWon
            },
            last_minute: {
                id: 'last_minute',
                name: 'Down to the Wire',
                nameRu: 'В последнюю минуту',
                description: 'Win with less than 10 days remaining',
                descriptionRu: 'Победите с менее чем 10 днями до дедлайна',
                icon: '⏰',
                rarity: 'rare',
                points: 75,
                condition: (state) => {
                    const daysLeft = GAME_DATA.config.deadline_day - state.currentDay;
                    return daysLeft < 10 && state.gameWon;
                }
            },

            // Political achievements
            political_mastermind: {
                id: 'political_mastermind',
                name: 'Political Mastermind',
                nameRu: 'Политический гений',
                description: 'Reach 95+ political influence',
                descriptionRu: 'Достигните 95+ политического влияния',
                icon: '🏛️',
                rarity: 'epic',
                points: 100,
                condition: (state) => state.influence >= 95
            },
            lobby_master: {
                id: 'lobby_master',
                name: 'Master Lobbyist',
                nameRu: 'Мастер лоббизма',
                description: 'Successfully lobby all regulators',
                descriptionRu: 'Успешно пролоббируйте всех регуляторов',
                icon: '📜',
                rarity: 'rare',
                points: 80,
                condition: (state) => state.antitrustPressure < 20
            },

            // Reputation achievements
            hollywood_darling: {
                id: 'hollywood_darling',
                name: 'Hollywood Darling',
                nameRu: 'Любимец Голливуда',
                description: 'Reputation above 90',
                descriptionRu: 'Репутация выше 90',
                icon: '⭐',
                rarity: 'rare',
                points: 75,
                condition: (state) => state.reputation >= 90
            },

            // Special achievements
            hostile_takeover: {
                id: 'hostile_takeover',
                name: 'Hostile Takeover',
                nameRu: 'Враждебное поглощение',
                description: 'Launch a hostile takeover',
                descriptionRu: 'Запустите враждебное поглощение',
                icon: '⚔️',
                rarity: 'epic',
                points: 150,
                condition: (state) => state.gamePhase === 'hostile'
            },
            perfect_game: {
                id: 'perfect_game',
                name: 'Perfect Game',
                nameRu: 'Идеальная игра',
                description: 'Win with max influence, reputation and relationships',
                descriptionRu: 'Победите с максимальным влиянием, репутацией и отношениями',
                icon: '🏆',
                rarity: 'legendary',
                points: 500,
                condition: (state) => {
                    return state.gameWon &&
                           state.influence >= 90 &&
                           state.reputation >= 90 &&
                           Object.values(state.relationships).every(r => r >= 80);
                }
            },

            // Financial achievements
            debt_free: {
                id: 'debt_free',
                name: 'Debt Free',
                nameRu: 'Без долгов',
                description: 'Win without using any debt',
                descriptionRu: 'Победите без использования долгов',
                icon: '💳',
                rarity: 'rare',
                points: 100,
                condition: (state) => {
                    return state.gameWon && window.Financing.getTotalDebt() === 0;
                }
            },
            leveraged_buyout: {
                id: 'leveraged_buyout',
                name: 'Leveraged Buyout Master',
                nameRu: 'Мастер выкупа с плечом',
                description: 'Use 80%+ debt financing',
                descriptionRu: 'Используйте 80%+ долгового финансирования',
                icon: '📊',
                rarity: 'epic',
                points: 120,
                condition: (state) => {
                    const totalDebt = window.Financing.getTotalDebt();
                    const dealCost = state.currentBid * GAME_DATA.config.wbd_shares;
                    return (totalDebt / dealCost) >= 0.8;
                }
            },

            // Collection achievements
            collector: {
                id: 'collector',
                name: 'Achievement Hunter',
                nameRu: 'Охотник за достижениями',
                description: 'Unlock 10 achievements',
                descriptionRu: 'Разблокируйте 10 достижений',
                icon: '🎯',
                rarity: 'epic',
                points: 100,
                condition: (state) => this.unlockedAchievements.length >= 10
            },
            completionist: {
                id: 'completionist',
                name: 'Completionist',
                nameRu: 'Перфекционист',
                description: 'Unlock all achievements',
                descriptionRu: 'Разблокируйте все достижения',
                icon: '👑',
                rarity: 'legendary',
                points: 1000,
                condition: (state) => {
                    return this.unlockedAchievements.length === Object.keys(this.achievements).length - 2;
                }
            }
        };
    }

    // Check all achievements
    checkAchievements(gameState) {
        const newlyUnlocked = [];

        for (let id in this.achievements) {
            const achievement = this.achievements[id];

            // Skip if already unlocked
            if (this.unlockedAchievements.includes(id)) continue;

            // Check condition
            try {
                if (achievement.condition(gameState)) {
                    this.unlockAchievement(id);
                    newlyUnlocked.push(achievement);
                }
            } catch (e) {
                console.error(`Error checking achievement ${id}:`, e);
            }
        }

        return newlyUnlocked;
    }

    // Unlock achievement
    unlockAchievement(achievementId) {
        if (!this.unlockedAchievements.includes(achievementId)) {
            this.unlockedAchievements.push(achievementId);
            this.saveUnlocked();

            // Show notification
            const achievement = this.achievements[achievementId];
            if (window.UI) {
                this.showAchievementUnlock(achievement);
            }

            // Play sound (if available)
            this.playUnlockSound();

            return true;
        }
        return false;
    }

    // Show achievement unlock notification
    showAchievementUnlock(achievement) {
        const lang = window.i18n.getLanguage();
        const name = lang === 'ru' ? achievement.nameRu : achievement.name;
        const description = lang === 'ru' ? achievement.descriptionRu : achievement.description;

        // Create custom achievement notification
        const notification = document.createElement('div');
        notification.className = `achievement-unlock ${achievement.rarity}`;
        notification.innerHTML = `
            <div class="achievement-content">
                <div class="achievement-icon">${achievement.icon}</div>
                <div class="achievement-info">
                    <div class="achievement-rarity">${achievement.rarity.toUpperCase()}</div>
                    <div class="achievement-name">${name}</div>
                    <div class="achievement-desc">${description}</div>
                    <div class="achievement-points">+${achievement.points} points</div>
                </div>
            </div>
        `;

        document.body.appendChild(notification);

        // Animate in
        setTimeout(() => notification.classList.add('show'), 100);

        // Remove after 5 seconds
        setTimeout(() => {
            notification.classList.remove('show');
            setTimeout(() => notification.remove(), 500);
        }, 5000);
    }

    // Play unlock sound
    playUnlockSound() {
        // TODO: Add sound effect
        console.log('🎵 Achievement unlocked!');
    }

    // Get total points
    getTotalPoints() {
        let total = 0;
        this.unlockedAchievements.forEach(id => {
            if (this.achievements[id]) {
                total += this.achievements[id].points;
            }
        });
        return total;
    }

    // Get progress percentage
    getProgress() {
        const total = Object.keys(this.achievements).length;
        const unlocked = this.unlockedAchievements.length;
        return (unlocked / total) * 100;
    }

    // Get achievements by rarity
    getByRarity(rarity) {
        return Object.values(this.achievements).filter(a => a.rarity === rarity);
    }

    // Save unlocked achievements
    saveUnlocked() {
        localStorage.setItem('mediaMogulAchievements', JSON.stringify(this.unlockedAchievements));
    }

    // Load unlocked achievements
    loadUnlocked() {
        try {
            const saved = localStorage.getItem('mediaMogulAchievements');
            return saved ? JSON.parse(saved) : [];
        } catch (e) {
            return [];
        }
    }

    // Generate achievements panel HTML
    generateAchievementsPanel() {
        const lang = window.i18n.getLanguage();
        const rarityOrder = ['legendary', 'epic', 'rare', 'common'];

        let html = `
            <div class="achievements-panel">
                <div class="achievements-header">
                    <h2>${lang === 'ru' ? 'Достижения' : 'Achievements'}</h2>
                    <div class="achievements-stats">
                        <div class="stat-item">
                            <span class="stat-label">${lang === 'ru' ? 'Разблокировано' : 'Unlocked'}:</span>
                            <span class="stat-value">${this.unlockedAchievements.length}/${Object.keys(this.achievements).length}</span>
                        </div>
                        <div class="stat-item">
                            <span class="stat-label">${lang === 'ru' ? 'Очки' : 'Points'}:</span>
                            <span class="stat-value">${this.getTotalPoints()}</span>
                        </div>
                        <div class="stat-item">
                            <span class="stat-label">${lang === 'ru' ? 'Прогресс' : 'Progress'}:</span>
                            <div class="progress-bar">
                                <div class="progress-fill" style="width: ${this.getProgress()}%"></div>
                            </div>
                            <span class="stat-value">${this.getProgress().toFixed(0)}%</span>
                        </div>
                    </div>
                </div>

                <div class="achievements-list">
        `;

        rarityOrder.forEach(rarity => {
            const achievementsOfRarity = this.getByRarity(rarity);

            if (achievementsOfRarity.length > 0) {
                html += `<h3 class="rarity-header ${rarity}">${rarity.toUpperCase()}</h3>`;

                achievementsOfRarity.forEach(achievement => {
                    const unlocked = this.unlockedAchievements.includes(achievement.id);
                    const name = lang === 'ru' ? achievement.nameRu : achievement.name;
                    const description = lang === 'ru' ? achievement.descriptionRu : achievement.description;

                    html += `
                        <div class="achievement-item ${unlocked ? 'unlocked' : 'locked'} ${achievement.rarity}">
                            <div class="achievement-icon">${unlocked ? achievement.icon : '🔒'}</div>
                            <div class="achievement-details">
                                <div class="achievement-name">${unlocked ? name : '???'}</div>
                                <div class="achievement-desc">${unlocked ? description : 'Locked'}</div>
                                <div class="achievement-points">${achievement.points} ${lang === 'ru' ? 'очков' : 'points'}</div>
                            </div>
                        </div>
                    `;
                });
            }
        });

        html += `
                </div>
            </div>
        `;

        return html;
    }
}

// Create global achievements instance
if (typeof window !== 'undefined') {
    window.Achievements = new AchievementsSystem();
}
