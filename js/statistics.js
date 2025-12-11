// Media Mogul: Statistics & Charts System

class StatisticsSystem {
    constructor() {
        this.history = {
            cash: [],
            influence: [],
            reputation: [],
            bid: [],
            relationships: {}
        };
    }

    // Record current state
    recordState(gameState) {
        this.history.cash.push({
            day: gameState.currentDay,
            value: gameState.cash
        });

        this.history.influence.push({
            day: gameState.currentDay,
            value: gameState.influence
        });

        this.history.reputation.push({
            day: gameState.currentDay,
            value: gameState.reputation
        });

        this.history.bid.push({
            day: gameState.currentDay,
            value: gameState.currentBid
        });

        // Record relationships
        for (let npcId in gameState.relationships) {
            if (!this.history.relationships[npcId]) {
                this.history.relationships[npcId] = [];
            }
            this.history.relationships[npcId].push({
                day: gameState.currentDay,
                value: gameState.relationships[npcId]
            });
        }
    }

    // Generate statistics dashboard
    generateDashboard(gameState) {
        const lang = window.i18n.getLanguage();

        let html = `
            <div class="statistics-dashboard">
                <h2>${lang === 'ru' ? 'Статистика и аналитика' : 'Statistics & Analytics'}</h2>

                <!-- Summary Cards -->
                <div class="stat-cards">
                    ${this.generateStatCard('cash', gameState.cash, '💰', lang)}
                    ${this.generateStatCard('influence', gameState.influence, '🏛️', lang)}
                    ${this.generateStatCard('reputation', gameState.reputation, '⭐', lang)}
                    ${this.generateStatCard('bid', gameState.currentBid, '📊', lang)}
                </div>

                <!-- Charts -->
                <div class="charts-container">
                    <div class="chart-panel">
                        <h3>${lang === 'ru' ? 'Тренд ресурсов' : 'Resources Trend'}</h3>
                        ${this.generateLineChart(['cash', 'influence', 'reputation'])}
                    </div>

                    <div class="chart-panel">
                        <h3>${lang === 'ru' ? 'История ставок' : 'Bid History'}</h3>
                        ${this.generateLineChart(['bid'])}
                    </div>

                    <div class="chart-panel">
                        <h3>${lang === 'ru' ? 'Отношения с NPC' : 'NPC Relationships'}</h3>
                        ${this.generateRelationshipsChart(gameState)}
                    </div>
                </div>

                <!-- Detailed Stats -->
                <div class="detailed-stats">
                    <h3>${lang === 'ru' ? 'Подробная статистика' : 'Detailed Statistics'}</h3>
                    ${this.generateDetailedStats(gameState, lang)}
                </div>
            </div>
        `;

        return html;
    }

    // Generate stat card
    generateStatCard(type, value, icon, lang) {
        const labels = {
            cash: { en: 'Cash', ru: 'Наличные' },
            influence: { en: 'Influence', ru: 'Влияние' },
            reputation: { en: 'Reputation', ru: 'Репутация' },
            bid: { en: 'Current Bid', ru: 'Текущая ставка' }
        };

        const formatValue = (type, val) => {
            if (type === 'cash' || type === 'bid') return `$${val.toFixed(type === 'cash' ? 1 : 2)}${type === 'cash' ? 'B' : ''}`;
            return `${val}/100`;
        };

        const change = this.getChange(type);
        const changeIcon = change > 0 ? '📈' : change < 0 ? '📉' : '➖';
        const changeClass = change > 0 ? 'positive' : change < 0 ? 'negative' : 'neutral';

        return `
            <div class="stat-card ${type}">
                <div class="stat-icon">${icon}</div>
                <div class="stat-info">
                    <div class="stat-label">${labels[type][lang]}</div>
                    <div class="stat-value">${formatValue(type, value)}</div>
                    <div class="stat-change ${changeClass}">
                        ${changeIcon} ${change > 0 ? '+' : ''}${change.toFixed(1)}
                    </div>
                </div>
            </div>
        `;
    }

    // Get change from last record
    getChange(type) {
        const data = this.history[type];
        if (data.length < 2) return 0;

        const current = data[data.length - 1].value;
        const previous = data[data.length - 2].value;

        return current - previous;
    }

    // Generate simple line chart (ASCII/CSS based)
    generateLineChart(metrics) {
        let html = '<div class="simple-chart">';

        metrics.forEach(metric => {
            const data = this.history[metric];
            if (!data || data.length === 0) return;

            const maxValue = Math.max(...data.map(d => d.value));
            const minValue = Math.min(...data.map(d => d.value));

            html += `
                <div class="chart-line ${metric}">
                    <div class="chart-points">
            `;

            data.forEach((point, index) => {
                const percentage = ((point.value - minValue) / (maxValue - minValue)) * 100;
                html += `
                    <div class="chart-point"
                         style="left: ${(index / (data.length - 1)) * 100}%; bottom: ${percentage}%"
                         title="Day ${point.day}: ${point.value.toFixed(2)}">
                    </div>
                `;
            });

            html += `
                    </div>
                </div>
            `;
        });

        html += '</div>';
        return html;
    }

    // Generate relationships chart
    generateRelationshipsChart(gameState) {
        let html = '<div class="relationships-chart">';

        for (let npcId in gameState.relationships) {
            const npcData = GAME_DATA.npcs[npcId];
            if (!npcData) continue;

            const relationship = gameState.relationships[npcId];
            const percentage = relationship;

            html += `
                <div class="relationship-bar-item">
                    <div class="npc-label">
                        <span class="npc-portrait-small">${npcData.portrait}</span>
                        <span class="npc-name-small">${npcData.name}</span>
                    </div>
                    <div class="relationship-bar-container">
                        <div class="relationship-bar-fill"
                             style="width: ${percentage}%; background: ${this.getRelationshipColor(percentage)}">
                        </div>
                    </div>
                    <div class="relationship-value-small">${relationship}/100</div>
                </div>
            `;
        }

        html += '</div>';
        return html;
    }

    // Get relationship color
    getRelationshipColor(value) {
        if (value >= 80) return '#10b981';
        if (value >= 60) return '#3b82f6';
        if (value >= 40) return '#f59e0b';
        if (value >= 20) return '#f97316';
        return '#ef4444';
    }

    // Generate detailed stats
    generateDetailedStats(gameState, lang) {
        const daysPlayed = gameState.currentDay;
        const daysLeft = GAME_DATA.config.deadline_day - gameState.currentDay;
        const dealValue = gameState.currentBid * GAME_DATA.config.wbd_shares;
        const avgInfluence = this.getAverage('influence');
        const avgReputation = this.getAverage('reputation');

        const stats = [
            { label: lang === 'ru' ? 'Дней сыграно' : 'Days Played', value: daysPlayed },
            { label: lang === 'ru' ? 'Дней осталось' : 'Days Remaining', value: daysLeft },
            { label: lang === 'ru' ? 'Стоимость сделки' : 'Deal Value', value: `$${dealValue.toFixed(1)}B` },
            { label: lang === 'ru' ? 'Среднее влияние' : 'Avg Influence', value: avgInfluence.toFixed(1) },
            { label: lang === 'ru' ? 'Средняя репутация' : 'Avg Reputation', value: avgReputation.toFixed(1) },
            { label: lang === 'ru' ? 'Повышений ставки' : 'Bid Increases', value: this.history.bid.length - 1 },
            { label: lang === 'ru' ? 'События' : 'Events', value: gameState.eventLog.length }
        ];

        let html = '<div class="detailed-stats-grid">';

        stats.forEach(stat => {
            html += `
                <div class="stat-item-detailed">
                    <span class="stat-label-detailed">${stat.label}:</span>
                    <span class="stat-value-detailed">${stat.value}</span>
                </div>
            `;
        });

        html += '</div>';
        return html;
    }

    // Get average value
    getAverage(metric) {
        const data = this.history[metric];
        if (!data || data.length === 0) return 0;

        const sum = data.reduce((acc, point) => acc + point.value, 0);
        return sum / data.length;
    }

    // Get peak value
    getPeak(metric) {
        const data = this.history[metric];
        if (!data || data.length === 0) return 0;

        return Math.max(...data.map(d => d.value));
    }

    // Get low value
    getLow(metric) {
        const data = this.history[metric];
        if (!data || data.length === 0) return 0;

        return Math.min(...data.map(d => d.value));
    }

    // Export statistics
    exportStats() {
        return {
            history: this.history,
            summary: {
                avgCash: this.getAverage('cash'),
                avgInfluence: this.getAverage('influence'),
                avgReputation: this.getAverage('reputation'),
                peakBid: this.getPeak('bid')
            }
        };
    }

    // Clear history
    clearHistory() {
        this.history = {
            cash: [],
            influence: [],
            reputation: [],
            bid: [],
            relationships: {}
        };
    }
}

// Create global statistics instance
if (typeof window !== 'undefined') {
    window.Statistics = new StatisticsSystem();
}
