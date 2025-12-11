// Media Mogul: UI Controller

class UIController {
    constructor() {
        this.elements = {};
        this.modal = null;
    }

    // Initialize UI
    init() {
        // Cache DOM elements
        this.elements = {
            // Resources
            cashValue: document.getElementById('cash-value'),
            stockValue: document.getElementById('stock-value'),
            influenceBar: document.getElementById('influence-bar'),
            influenceValue: document.getElementById('influence-value'),
            reputationBar: document.getElementById('reputation-bar'),
            reputationValue: document.getElementById('reputation-value'),

            // Bid status
            yourBid: document.getElementById('your-bid'),

            // Date & time
            currentDate: document.getElementById('current-date'),
            daysRemaining: document.getElementById('days-remaining'),

            // Main display
            mainDisplay: document.getElementById('main-display'),
            eventList: document.getElementById('event-list'),

            // NPCs
            npcList: document.getElementById('npc-list'),

            // Modal
            modalOverlay: document.getElementById('modal-overlay'),
            modalTitle: document.getElementById('modal-title'),
            modalBody: document.getElementById('modal-body'),
            modalFooter: document.getElementById('modal-footer'),
            modalClose: document.getElementById('modal-close'),

            // Loading
            loadingScreen: document.getElementById('loading-screen')
        };

        // Setup event listeners
        this.setupEventListeners();

        // Initial render
        this.render();
    }

    // Setup event listeners
    setupEventListeners() {
        // Language switcher
        document.querySelectorAll('.lang-btn').forEach(btn => {
            btn.addEventListener('click', (e) => {
                const lang = e.target.dataset.lang;
                this.switchLanguage(lang);
            });
        });

        // Start game button
        const startBtn = document.getElementById('btn-start-game');
        if (startBtn) {
            startBtn.addEventListener('click', () => this.startGame());
        }

        // Action buttons
        document.getElementById('btn-negotiate')?.addEventListener('click', () => this.showNegotiationPanel());
        document.getElementById('btn-finance')?.addEventListener('click', () => this.showFinancePanel());
        document.getElementById('btn-politics')?.addEventListener('click', () => this.showPoliticsPanel());
        document.getElementById('btn-shareholders')?.addEventListener('click', () => this.showShareholdersPanel());
        document.getElementById('btn-next-turn')?.addEventListener('click', () => this.nextTurn());

        // Menu button
        document.getElementById('btn-menu')?.addEventListener('click', () => this.toggleMenu());

        // Menu items
        document.getElementById('menu-achievements')?.addEventListener('click', () => {
            this.hideMenu();
            this.showAchievementsPanel();
        });
        document.getElementById('menu-statistics')?.addEventListener('click', () => {
            this.hideMenu();
            this.showStatisticsPanel();
        });
        document.getElementById('menu-help')?.addEventListener('click', () => {
            this.hideMenu();
            this.showHelpPanel();
        });
        document.getElementById('menu-settings')?.addEventListener('click', () => {
            this.hideMenu();
            this.showSettingsPanel();
        });
        document.getElementById('menu-save')?.addEventListener('click', () => {
            this.hideMenu();
            window.Game.saveGame();
            this.showNotification(window.i18n.t('gameSaved'), 'success');
        });

        // Modal close
        this.elements.modalClose?.addEventListener('click', () => this.hideModal());
        this.elements.modalOverlay?.addEventListener('click', (e) => {
            if (e.target === this.elements.modalOverlay) {
                this.hideModal();
            }
        });

        // NPC click handlers
        document.querySelectorAll('.npc-item').forEach(item => {
            item.addEventListener('click', () => {
                const npcId = item.dataset.npc;
                this.showNPCInfo(npcId);
            });
        });
    }

    // Switch language
    switchLanguage(lang) {
        window.i18n.setLanguage(lang);

        // Update active button
        document.querySelectorAll('.lang-btn').forEach(btn => {
            btn.classList.remove('active');
        });
        document.getElementById(`lang-${lang}`).classList.add('active');

        // Update all translations
        this.updateTranslations();

        this.showNotification(window.i18n.t('language') + ': ' + window.i18n.t(lang === 'en' ? 'english' : 'russian'), 'info');
    }

    // Update all translations in the page
    updateTranslations() {
        // Update all elements with data-i18n attribute
        document.querySelectorAll('[data-i18n]').forEach(elem => {
            const key = elem.getAttribute('data-i18n');
            elem.textContent = window.i18n.t(key);
        });

        // Update elements with data-i18n-template (with parameters)
        document.querySelectorAll('[data-i18n-template]').forEach(elem => {
            const key = elem.getAttribute('data-i18n-template');
            const company = elem.getAttribute('data-company') || 'Paramount Skydance';
            const translation = window.i18n.t(key, { company: company });

            // Update the span content while preserving the <strong> tag
            const welcomeCompany = document.getElementById('welcome-company');
            if (welcomeCompany) {
                const parts = translation.split(company);
                elem.innerHTML = parts[0] + '<strong id="welcome-company">' + company + '</strong>' + (parts[1] || '');
            }
        });

        // Re-render if game is active
        if (window.Game && window.Game.state.isGameActive) {
            this.render();
            this.updateEventLog();
        }
    }

    // Start game
    startGame() {
        window.Game.init('paramount');
        this.showMainGameScreen();
        this.render();
        this.showNotification('Game started! Good luck!', 'success');
    }

    // Next turn
    nextTurn() {
        window.Game.nextDay();

        // Check for new achievements
        if (window.Achievements) {
            window.Achievements.checkAchievements(window.Game.getState());
        }

        // Record statistics
        if (window.Statistics) {
            window.Statistics.recordState(window.Game.getState());
        }

        this.render();
        this.updateEventLog();
    }

    // Toggle menu
    toggleMenu() {
        const menu = document.getElementById('game-menu');
        if (menu) {
            menu.classList.toggle('hidden');
        }
    }

    // Hide menu
    hideMenu() {
        const menu = document.getElementById('game-menu');
        if (menu) {
            menu.classList.add('hidden');
        }
    }

    // Main render function
    render() {
        const state = window.Game.getState();

        // Update resources
        this.elements.cashValue.textContent = `$${state.cash.toFixed(1)}B`;
        this.elements.stockValue.textContent = state.stock > 0 ? `$${state.stock.toFixed(1)}B` : 'N/A';

        this.elements.influenceBar.style.width = `${state.influence}%`;
        this.elements.influenceValue.textContent = `${state.influence}/100`;

        this.elements.reputationBar.style.width = `${state.reputation}%`;
        this.elements.reputationValue.textContent = `${state.reputation}/100`;

        // Update bid
        this.elements.yourBid.textContent = `$${state.currentBid.toFixed(2)}/share`;

        // Update date
        const dateStr = state.currentDate.toLocaleDateString('en-US', {
            year: 'numeric',
            month: 'long',
            day: 'numeric'
        });
        this.elements.currentDate.textContent = dateStr;

        const daysLeft = GAME_DATA.config.deadline_day - state.currentDay;
        this.elements.daysRemaining.innerHTML = `<span data-i18n="daysToDeadline">${window.i18n.t('daysToDeadline')}</span>: <strong>${daysLeft}</strong>`;

        // Update NPCs
        this.updateNPCs(state);
    }

    // Update NPCs
    updateNPCs(state) {
        const npcElements = document.querySelectorAll('.npc-item');
        npcElements.forEach(elem => {
            const npcId = elem.dataset.npc;
            if (state.relationships[npcId] !== undefined) {
                const relationship = state.relationships[npcId];
                const fillElem = elem.querySelector('.relationship-fill');
                const valueElem = elem.querySelector('.relationship-value');

                if (fillElem) fillElem.style.width = `${relationship}%`;
                if (valueElem) valueElem.textContent = `${relationship}/100`;

                // Update mood emoji
                const moodElem = elem.querySelector('.npc-mood');
                if (moodElem) {
                    let emoji = '😐';
                    let moodKey = 'neutral';

                    if (relationship >= 80) {
                        emoji = '😊';
                        moodKey = 'veryPositive';
                    } else if (relationship >= 60) {
                        emoji = '🙂';
                        moodKey = 'positive';
                    } else if (relationship >= 40) {
                        emoji = '😐';
                        moodKey = 'neutral';
                    } else if (relationship >= 20) {
                        emoji = '😠';
                        moodKey = 'negative';
                    } else {
                        emoji = '😡';
                        moodKey = 'veryNegative';
                    }

                    moodElem.innerHTML = `${emoji} <span data-i18n="${moodKey}">${window.i18n.t(moodKey)}</span>`;
                }
            }
        });
    }

    // Update event log
    updateEventLog() {
        const state = window.Game.getState();
        const eventList = this.elements.eventList;

        // Clear and rebuild
        eventList.innerHTML = '';

        // Show last 10 events
        const recentEvents = state.eventLog.slice(-10).reverse();
        recentEvents.forEach(event => {
            const eventDiv = document.createElement('div');
            eventDiv.className = `event-item ${event.type}`;
            eventDiv.innerHTML = `
                <span class="event-time"><span data-i18n="day">${window.i18n.t('day')}</span> ${event.day}</span>
                <span class="event-text">${event.text}</span>
            `;
            eventList.appendChild(eventDiv);
        });
    }

    // Show main game screen
    showMainGameScreen() {
        const currentDay = window.Game.getState().currentDay;
        this.elements.mainDisplay.innerHTML = `
            <h2 data-i18n-template="dayTitle">${window.i18n.t('dayTitle', {day: currentDay})}</h2>
            <p data-i18n="whatToDo">${window.i18n.t('whatToDo')}</p>
            <div class="action-guide">
                <h3 data-i18n="availableActions">${window.i18n.t('availableActions')}</h3>
                <ul>
                    <li><strong data-i18n="negotiate">${window.i18n.t('negotiate')}</strong> - <span data-i18n="actionNegotiate">${window.i18n.t('actionNegotiate')}</span></li>
                    <li><strong data-i18n="finance">${window.i18n.t('finance')}</strong> - <span data-i18n="actionFinance">${window.i18n.t('actionFinance')}</span></li>
                    <li><strong data-i18n="politics">${window.i18n.t('politics')}</strong> - <span data-i18n="actionPolitics">${window.i18n.t('actionPolitics')}</span></li>
                    <li><strong data-i18n="shareholders">${window.i18n.t('shareholders')}</strong> - <span data-i18n="actionShareholders">${window.i18n.t('actionShareholders')}</span></li>
                </ul>
            </div>
        `;
    }

    // Show negotiation panel
    showNegotiationPanel() {
        const state = window.Game.getState();

        let content = '<h3>Available Meetings</h3><div class="npc-meeting-list">';

        // Zaslav
        content += `
            <div class="meeting-option" data-npc="zaslav">
                <div class="meeting-header">
                    <h4>David Zaslav</h4>
                    <span class="relationship-badge" style="background: ${this.getRelationshipColor(state.relationships.zaslav)}">
                        ${state.relationships.zaslav}/100
                    </span>
                </div>
                <p>CEO of Warner Bros. Discovery - The key decision maker</p>
                <button class="btn-primary" onclick="window.Negotiations.startDialogue('zaslav_meeting_1')">
                    Schedule Meeting
                </button>
            </div>
        `;

        // Trump
        if (state.influence >= 30) {
            content += `
                <div class="meeting-option" data-npc="trump">
                    <div class="meeting-header">
                        <h4>Donald Trump</h4>
                        <span class="relationship-badge" style="background: ${this.getRelationshipColor(state.relationships.trump)}">
                            ${state.relationships.trump}/100
                        </span>
                    </div>
                    <p>President - Can provide political cover</p>
                    <button class="btn-primary" onclick="window.Negotiations.startDialogue('trump_call')">
                        Call Trump (30 influence)
                    </button>
                </div>
            `;
        } else {
            content += `
                <div class="meeting-option disabled">
                    <div class="meeting-header">
                        <h4>Donald Trump</h4>
                        <span class="relationship-badge">Locked</span>
                    </div>
                    <p>Requires 30+ political influence</p>
                </div>
            `;
        }

        content += '</div>';

        this.elements.mainDisplay.innerHTML = content;
    }

    // Show finance panel
    showFinancePanel() {
        const state = window.Game.getState();
        const lang = window.i18n.getLanguage();

        let content = `
            <h3 data-i18n="financialResources">${window.i18n.t('financialResources')}</h3>
            <div class="finance-summary">
                <div class="finance-item">
                    <span data-i18n="availableCash">${window.i18n.t('availableCash')}</span>
                    <strong>$${state.cash.toFixed(1)}B</strong>
                </div>
                <div class="finance-item">
                    <span data-i18n="debtCapacity">${window.i18n.t('debtCapacity')}</span>
                    <strong>$${state.debtCapacity.toFixed(1)}B</strong>
                </div>
                <div class="finance-item">
                    <span data-i18n="totalCapacity">${window.i18n.t('totalCapacity')}</span>
                    <strong>$${(state.cash + state.debtCapacity).toFixed(1)}B</strong>
                </div>
            </div>

            <h3 data-i18n="raiseYourBid">${window.i18n.t('raiseYourBid')}</h3>
            <div class="bid-controls">
                <p><span data-i18n="currentBid">${window.i18n.t('currentBid')}</span> <strong>$${state.currentBid.toFixed(2)}/share</strong></p>
                <p><span data-i18n="totalDealValue">${window.i18n.t('totalDealValue')}</span> <strong>$${(state.currentBid * GAME_DATA.config.wbd_shares).toFixed(1)}B</strong></p>
                <div class="bid-input">
                    <label data-i18n="newBidPerShare">${window.i18n.t('newBidPerShare')}</label>
                    <input type="number" id="new-bid-input" min="${state.currentBid + 0.01}" step="0.25" value="${(state.currentBid + 1).toFixed(2)}">
                    <button class="btn-primary" onclick="window.UI.raiseBid()" data-i18n="raiseBid">${window.i18n.t('raiseBid')}</button>
                </div>
            </div>
        `;

        // Add financing sources if system is available
        if (window.Financing) {
            content += `<h3 data-i18n="financingSources">${window.i18n.t('financingSources')}</h3>`;
            content += window.Financing.generateInvestorPanel(state, lang);
        }

        this.elements.mainDisplay.innerHTML = content;
    }

    // Raise bid
    raiseBid() {
        const input = document.getElementById('new-bid-input');
        const newBid = parseFloat(input.value);

        const result = window.Game.raiseBid(newBid);

        if (result.success) {
            this.showNotification(result.message, 'success');
            this.render();
            this.showFinancePanel();
        } else {
            this.showNotification(result.message, 'error');
        }
    }

    // Show politics panel
    showPoliticsPanel() {
        const state = window.Game.getState();

        let content = '<h3>Political Actions</h3><div class="politics-actions">';

        GAME_DATA.political_actions.forEach(action => {
            const onCooldown = state.cooldowns[action.id] && state.cooldowns[action.id] > 0;
            const canAfford = (!action.cost.influence || state.influence >= action.cost.influence) &&
                            (!action.cost.cash || state.cash >= action.cost.cash);

            content += `
                <div class="politics-action ${onCooldown || !canAfford ? 'disabled' : ''}">
                    <h4>${action.name}</h4>
                    <p>${action.description}</p>
                    <div class="politics-cost-row">
                        ${action.cost.influence ? `<span class="politics-cost">🏛️ ${action.cost.influence} Influence</span>` : ''}
                        ${action.cost.cash ? `<span class="politics-cost">💰 $${action.cost.cash}B</span>` : ''}
                    </div>
                    ${onCooldown ? `<p class="text-warning">Cooldown: ${state.cooldowns[action.id]} days</p>` : ''}
                    ${!onCooldown && canAfford ? `
                        <button class="btn-primary" onclick="window.UI.executePoliticalAction('${action.id}')">
                            Execute
                        </button>
                    ` : ''}
                </div>
            `;
        });

        content += '</div>';
        this.elements.mainDisplay.innerHTML = content;
    }

    // Execute political action
    executePoliticalAction(actionId) {
        const result = window.Game.executePoliticalAction(actionId);

        if (result.success) {
            this.showNotification(result.message, 'success');
            this.render();
            this.showPoliticsPanel();
        } else {
            this.showNotification(result.message, 'error');
        }
    }

    // Show shareholders panel
    showShareholdersPanel() {
        const state = window.Game.getState();

        let content = '<h3>Major Shareholders</h3><div class="shareholder-list">';

        for (let id in state.shareholderSupport) {
            const support = state.shareholderSupport[id];
            const shareholderData = GAME_DATA.shareholders[id];

            content += `
                <div class="shareholder-item">
                    <div class="shareholder-header">
                        <h4>${shareholderData.name}</h4>
                        <span class="ownership">${shareholderData.ownership}% ownership</span>
                    </div>
                    <div class="support-bar">
                        <div class="support-fill" style="width: ${support}%; background: ${this.getRelationshipColor(support)}"></div>
                    </div>
                    <p class="support-text">Support: ${support}%</p>
                </div>
            `;
        }

        content += '</div>';
        this.elements.mainDisplay.innerHTML = content;
    }

    // Show NPC info
    showNPCInfo(npcId) {
        const npcData = GAME_DATA.npcs[npcId];
        const state = window.Game.getState();

        const content = `
            <div class="npc-detail">
                <div class="npc-portrait-large">${npcData.portrait}</div>
                <h4>${npcData.name}</h4>
                <p class="npc-title-large">${npcData.title}</p>
                <div class="relationship-display">
                    <p>Your relationship: <strong>${state.relationships[npcId]}/100</strong></p>
                    <div class="progress-bar">
                        <div class="progress-fill" style="width: ${state.relationships[npcId]}%"></div>
                    </div>
                </div>
                <h5>Motivations:</h5>
                <ul>
                    ${npcData.motivations.map(m => `<li>${m}</li>`).join('')}
                </ul>
            </div>
        `;

        this.showModal(npcData.name, content);
    }

    // Modal system
    showModal(title, bodyHTML, footerHTML = '') {
        this.elements.modalTitle.textContent = title;
        this.elements.modalBody.innerHTML = bodyHTML;
        this.elements.modalFooter.innerHTML = footerHTML;
        this.elements.modalOverlay.classList.remove('hidden');
    }

    hideModal() {
        this.elements.modalOverlay.classList.add('hidden');
    }

    // Show event modal
    showEventModal(event, type) {
        const iconMap = {
            positive: '✅',
            negative: '❌',
            neutral: 'ℹ️'
        };

        const content = `
            <div class="event-modal ${type}">
                <div class="event-icon">${iconMap[type]}</div>
                <p class="event-description">${event.description}</p>
            </div>
        `;

        const footer = '<button class="btn-primary" onclick="window.UI.hideModal()">Continue</button>';

        this.showModal(event.title, content, footer);
    }

    // Show game end
    showGameEnd(reason, state) {
        let title, message, icon;

        switch(reason) {
            case 'victory':
                title = '🏆 Victory!';
                message = `Congratulations! You successfully acquired Warner Bros. Discovery for $${state.currentBid.toFixed(2)}/share!`;
                icon = '🎉';
                break;
            case 'timeout':
                title = '⏰ Time\'s Up!';
                message = 'The deadline has passed and you failed to secure the deal.';
                icon = '😞';
                break;
            case 'bankruptcy':
                title = '💸 Bankruptcy!';
                message = 'You ran out of money and can\'t continue the bid.';
                icon = '😱';
                break;
            case 'antitrust':
                title = '⚖️ Blocked!';
                message = 'Regulators have blocked your acquisition on antitrust grounds.';
                icon = '🚫';
                break;
        }

        const content = `
            <div class="game-end ${reason}">
                <div class="game-end-icon">${icon}</div>
                <h2>${title}</h2>
                <p>${message}</p>
                <div class="final-stats">
                    <h4>Final Statistics:</h4>
                    <ul>
                        <li>Days played: ${state.currentDay}</li>
                        <li>Final bid: $${state.currentBid.toFixed(2)}/share</li>
                        <li>Cash remaining: $${state.cash.toFixed(1)}B</li>
                        <li>Reputation: ${state.reputation}/100</li>
                        <li>Political influence: ${state.influence}/100</li>
                    </ul>
                </div>
            </div>
        `;

        const footer = `
            <button class="btn-primary" onclick="location.reload()">Play Again</button>
        `;

        this.showModal('Game Over', content, footer);
    }

    // Notifications
    showNotification(message, type = 'info') {
        const notification = document.createElement('div');
        notification.className = `notification-toast ${type}`;
        notification.textContent = message;

        document.body.appendChild(notification);

        setTimeout(() => {
            notification.remove();
        }, 4000);
    }

    // Helper: Get relationship color
    getRelationshipColor(value) {
        if (value >= 80) return '#10b981';
        if (value >= 60) return '#3b82f6';
        if (value >= 40) return '#f59e0b';
        if (value >= 20) return '#f97316';
        return '#ef4444';
    }

    // Show loading
    showLoading() {
        this.elements.loadingScreen.classList.remove('hidden');
    }

    hideLoading() {
        this.elements.loadingScreen.classList.add('hidden');
    }

    // Show bidding round
    showBiddingRound(round) {
        const content = `
            <div class="bidding-round">
                <h3>Round ${round.round}</h3>
                <p><strong>Date:</strong> ${round.date}</p>
                <p>${round.description}</p>
                <p><strong>Minimum bid:</strong> $${round.min_bid.toFixed(2)}/share</p>
                <p>This is your chance to make a competitive offer!</p>
            </div>
        `;

        const footer = '<button class="btn-primary" onclick="window.UI.hideModal(); window.UI.showFinancePanel()">Make Your Bid</button>';

        this.showModal(`Bidding Round ${round.round}`, content, footer);
    }

    // Show achievements panel
    showAchievementsPanel() {
        if (!window.Achievements) {
            this.showNotification('Achievements system not loaded', 'error');
            return;
        }

        const state = window.Game.getState();
        const lang = window.i18n.getLanguage();
        const content = window.Achievements.generateAchievementsPanel(state, lang);

        this.elements.mainDisplay.innerHTML = content;
    }

    // Show statistics panel
    showStatisticsPanel() {
        if (!window.Statistics) {
            this.showNotification('Statistics system not loaded', 'error');
            return;
        }

        const state = window.Game.getState();
        const lang = window.i18n.getLanguage();
        const content = window.Statistics.generateDashboard(state, lang);

        this.elements.mainDisplay.innerHTML = content;
    }

    // Show help panel
    showHelpPanel() {
        const lang = window.i18n.getLanguage();

        const content = `
            <div class="help-panel">
                <h3>${lang === 'ru' ? '📖 Справка' : '📖 Help'}</h3>

                <div class="help-section">
                    <h4>${lang === 'ru' ? '🎯 Цель игры' : '🎯 Game Objective'}</h4>
                    <p>${lang === 'ru'
                        ? 'Выиграйте торги на приобретение Warner Bros. Discovery, предложив не менее $35 за акцию и получив одобрение ключевых игроков.'
                        : 'Win the bidding war for Warner Bros. Discovery by offering at least $35/share and gaining approval from key stakeholders.'
                    }</p>
                </div>

                <div class="help-section">
                    <h4>${lang === 'ru' ? '💰 Ресурсы' : '💰 Resources'}</h4>
                    <ul>
                        <li><strong>${lang === 'ru' ? 'Наличные' : 'Cash'}</strong> - ${lang === 'ru' ? 'Используйте для повышения ставок' : 'Use to raise your bid'}</li>
                        <li><strong>${lang === 'ru' ? 'Политическое влияние' : 'Political Influence'}</strong> - ${lang === 'ru' ? 'Нужно для лоббирования регуляторов' : 'Required for lobbying regulators'}</li>
                        <li><strong>${lang === 'ru' ? 'Репутация' : 'Reputation'}</strong> - ${lang === 'ru' ? 'Влияет на поддержку акционеров' : 'Affects shareholder support'}</li>
                    </ul>
                </div>

                <div class="help-section">
                    <h4>${lang === 'ru' ? '🎮 Действия' : '🎮 Actions'}</h4>
                    <ul>
                        <li><strong>${lang === 'ru' ? 'Переговоры' : 'Negotiate'}</strong> - ${lang === 'ru' ? 'Встречайтесь с ключевыми фигурами' : 'Meet with key decision makers'}</li>
                        <li><strong>${lang === 'ru' ? 'Финансы' : 'Finance'}</strong> - ${lang === 'ru' ? 'Управляйте финансированием и ставками' : 'Manage financing and bids'}</li>
                        <li><strong>${lang === 'ru' ? 'Политика' : 'Politics'}</strong> - ${lang === 'ru' ? 'Лоббируйте регуляторов' : 'Lobby regulators'}</li>
                        <li><strong>${lang === 'ru' ? 'Акционеры' : 'Shareholders'}</strong> - ${lang === 'ru' ? 'Завоевывайте поддержку инвесторов' : 'Win investor support'}</li>
                    </ul>
                </div>

                <div class="help-section">
                    <h4>${lang === 'ru' ? '⌨️ Горячие клавиши' : '⌨️ Keyboard Shortcuts'}</h4>
                    <ul>
                        <li><kbd>Space</kbd>/<kbd>Enter</kbd> - ${lang === 'ru' ? 'Следующий день' : 'Next day'}</li>
                        <li><kbd>1</kbd>-<kbd>4</kbd> - ${lang === 'ru' ? 'Быстрые действия' : 'Quick actions'}</li>
                        <li><kbd>Esc</kbd> - ${lang === 'ru' ? 'Закрыть окно' : 'Close modal'}</li>
                        <li><kbd>Ctrl+S</kbd> - ${lang === 'ru' ? 'Сохранить игру' : 'Save game'}</li>
                    </ul>
                </div>

                <div class="help-section">
                    <h4>${lang === 'ru' ? '🏆 Условия победы' : '🏆 Win Conditions'}</h4>
                    <ul>
                        <li>${lang === 'ru' ? 'Ставка ≥ $35/акция' : 'Bid ≥ $35/share'}</li>
                        <li>${lang === 'ru' ? 'Отношения с Заславом ≥ 70/100' : 'Zaslav relationship ≥ 70/100'}</li>
                        <li>${lang === 'ru' ? 'Поддержка акционеров > 50%' : 'Shareholder support > 50%'}</li>
                        <li>${lang === 'ru' ? 'Антимонопольное давление < 50' : 'Antitrust pressure < 50'}</li>
                    </ul>
                </div>
            </div>
        `;

        this.elements.mainDisplay.innerHTML = content;
    }

    // Show settings panel
    showSettingsPanel() {
        const lang = window.i18n.getLanguage();

        const content = `
            <div class="settings-panel">
                <h3>${lang === 'ru' ? '⚙️ Настройки' : '⚙️ Settings'}</h3>

                <div class="setting-item">
                    <h4 data-i18n="language">${window.i18n.t('language')}</h4>
                    <div class="language-switcher">
                        <button class="lang-btn ${lang === 'en' ? 'active' : ''}" onclick="window.UI.switchLanguage('en')">EN</button>
                        <button class="lang-btn ${lang === 'ru' ? 'active' : ''}" onclick="window.UI.switchLanguage('ru')">RU</button>
                    </div>
                </div>

                <div class="setting-item">
                    <h4>${lang === 'ru' ? 'Сохранения' : 'Save Game'}</h4>
                    <button class="btn-primary" onclick="window.Game.saveGame(); window.UI.showNotification('${lang === 'ru' ? 'Игра сохранена!' : 'Game saved!'}', 'success')">
                        💾 ${lang === 'ru' ? 'Сохранить сейчас' : 'Save Now'}
                    </button>
                    <button class="btn-secondary" onclick="if(confirm('${lang === 'ru' ? 'Удалить сохранение?' : 'Delete save?'}')) { localStorage.removeItem(window.Game.saveKey); location.reload(); }">
                        🗑️ ${lang === 'ru' ? 'Удалить сохранение' : 'Delete Save'}
                    </button>
                </div>

                <div class="setting-item">
                    <h4>${lang === 'ru' ? 'О игре' : 'About'}</h4>
                    <p><strong>Media Mogul: The Warner Bros. War</strong></p>
                    <p>Version: ${window.GAME_VERSION || '1.0.0'}</p>
                    <p>Build: ${window.GAME_BUILD || 'Alpha'}</p>
                    <p style="margin-top: 10px; color: var(--text-secondary);">
                        ${lang === 'ru'
                            ? 'Это вымышленная игра, основанная на публичных новостях. Все персонажи и события используются исключительно в развлекательных целях.'
                            : 'This is a fictional game based on public news. All characters and events are used for entertainment purposes only.'
                        }
                    </p>
                </div>
            </div>
        `;

        this.elements.mainDisplay.innerHTML = content;
    }
}

// Create global UI instance
if (typeof window !== 'undefined') {
    window.UI = new UIController();
}
