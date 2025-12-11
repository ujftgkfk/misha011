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
        this.render();
        this.updateEventLog();
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
        this.elements.daysRemaining.innerHTML = `Days to deadline: <strong>${daysLeft}</strong>`;

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
                    if (relationship >= 80) emoji = '😊';
                    else if (relationship >= 60) emoji = '🙂';
                    else if (relationship >= 40) emoji = '😐';
                    else if (relationship >= 20) emoji = '😠';
                    else emoji = '😡';

                    let mood = 'Neutral';
                    if (relationship >= 80) mood = 'Very Positive';
                    else if (relationship >= 60) mood = 'Positive';
                    else if (relationship >= 40) mood = 'Neutral';
                    else if (relationship >= 20) mood = 'Negative';
                    else mood = 'Very Negative';

                    moodElem.textContent = `${emoji} ${mood}`;
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
                <span class="event-time">Day ${event.day}</span>
                <span class="event-text">${event.text}</span>
            `;
            eventList.appendChild(eventDiv);
        });
    }

    // Show main game screen
    showMainGameScreen() {
        this.elements.mainDisplay.innerHTML = `
            <h2>Day ${window.Game.getState().currentDay}</h2>
            <p>What would you like to do today?</p>
            <div class="action-guide">
                <h3>Available Actions:</h3>
                <ul>
                    <li><strong>Negotiate</strong> - Meet with key decision makers</li>
                    <li><strong>Finance</strong> - Secure funding and manage resources</li>
                    <li><strong>Politics</strong> - Lobby regulators and build influence</li>
                    <li><strong>Shareholders</strong> - Win over institutional investors</li>
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

        let content = `
            <h3>Financial Resources</h3>
            <div class="finance-summary">
                <div class="finance-item">
                    <span>Available Cash:</span>
                    <strong>$${state.cash.toFixed(1)}B</strong>
                </div>
                <div class="finance-item">
                    <span>Debt Capacity:</span>
                    <strong>$${state.debtCapacity.toFixed(1)}B</strong>
                </div>
                <div class="finance-item">
                    <span>Total Capacity:</span>
                    <strong>$${(state.cash + state.debtCapacity).toFixed(1)}B</strong>
                </div>
            </div>

            <h3>Raise Your Bid</h3>
            <div class="bid-controls">
                <p>Current bid: <strong>$${state.currentBid.toFixed(2)}/share</strong></p>
                <p>Total deal value: <strong>$${(state.currentBid * GAME_DATA.config.wbd_shares).toFixed(1)}B</strong></p>
                <div class="bid-input">
                    <label>New bid per share:</label>
                    <input type="number" id="new-bid-input" min="${state.currentBid + 0.01}" step="0.25" value="${(state.currentBid + 1).toFixed(2)}">
                    <button class="btn-primary" onclick="window.UI.raiseBid()">Raise Bid</button>
                </div>
            </div>

            <h3>Financing Sources</h3>
            <p class="text-secondary">Coming soon: Detailed financing options</p>
        `;

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
}

// Create global UI instance
if (typeof window !== 'undefined') {
    window.UI = new UIController();
}
