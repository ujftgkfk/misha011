// Media Mogul: Game Engine

class GameEngine {
    constructor() {
        this.state = {
            currentDay: 1,
            currentDate: new Date('2025-09-01'),
            playerFaction: 'paramount',

            // Resources
            cash: 40.7,
            stock: 0,
            influence: 75,
            reputation: 60,
            debtCapacity: 54,

            // Bid tracking
            currentBid: 30.00,
            competitorBids: {
                netflix: 27.75,
                comcast: 0 // withdrawn
            },

            // Relationships (0-100)
            relationships: {
                zaslav: 45,
                trump: 60,
                kanter: 30,
                khan: 25,
                ellison_larry: 95
            },

            // Shareholder support (%)
            shareholderSupport: {
                vanguard: 50,
                blackrock: 50,
                statestreet: 50,
                oakmark: 50
            },

            // Game state
            antitrustPressure: 30,
            isGameActive: false,
            gamePhase: 'preparation', // preparation, bidding, hostile, regulatory
            bidRound: 0,

            // Event log
            eventLog: [],

            // Action cooldowns
            cooldowns: {},

            // Achievements
            achievements: []
        };

        this.saveKey = 'mediaMogulSaveGame';
    }

    // Initialize game
    init(faction = 'paramount') {
        this.state.playerFaction = faction;
        const factionData = GAME_DATA.factions[faction];

        this.state.cash = factionData.resources.cash;
        this.state.stock = factionData.resources.stock;
        this.state.influence = factionData.resources.influence;
        this.state.reputation = factionData.resources.reputation;
        this.state.debtCapacity = factionData.resources.debt_capacity;

        this.addEvent('Game started. The battle for Warner Bros. Discovery begins!', 'neutral');
        this.state.isGameActive = true;
    }

    // Advance game by one day
    nextDay() {
        if (!this.state.isGameActive) return;

        this.state.currentDay++;
        this.state.currentDate.setDate(this.state.currentDate.getDate() + 1);

        // Update cooldowns
        for (let action in this.state.cooldowns) {
            if (this.state.cooldowns[action] > 0) {
                this.state.cooldowns[action]--;
            }
        }

        // Check for bidding rounds
        this.checkBiddingRounds();

        // Random events
        this.triggerRandomEvent();

        // AI competitor actions
        this.competitorActions();

        // Check win/loss conditions
        this.checkGameEnd();

        // Auto-save
        this.saveGame();
    }

    // Check if bidding round should trigger
    checkBiddingRounds() {
        const round = GAME_DATA.bidding_rounds.find(r => r.day === this.state.currentDay);
        if (round) {
            this.state.bidRound = round.round;
            this.state.gamePhase = 'bidding';
            this.addEvent(`Bidding Round ${round.round}: ${round.description}`, 'neutral');

            // Trigger bidding round event
            if (typeof window !== 'undefined' && window.UI) {
                window.UI.showBiddingRound(round);
            }
        }
    }

    // Random events system
    triggerRandomEvent() {
        const roll = Math.random();

        // Check positive events
        for (let event of GAME_DATA.events.positive) {
            if (roll < event.probability) {
                this.applyEvent(event, 'positive');
                return;
            }
        }

        // Check negative events
        for (let event of GAME_DATA.events.negative) {
            if (roll < event.probability) {
                this.applyEvent(event, 'negative');
                return;
            }
        }
    }

    // Apply event effects
    applyEvent(event, type) {
        this.addEvent(event.description, type);

        if (event.effects.influence) {
            this.modifyInfluence(event.effects.influence);
        }
        if (event.effects.reputation) {
            this.modifyReputation(event.effects.reputation);
        }
        if (event.effects.shareholder_support) {
            this.modifyShareholderSupport(event.effects.shareholder_support);
        }
        if (event.effects.relationship_loss) {
            // Damage random relationship
            const npcs = Object.keys(this.state.relationships);
            const randomNpc = npcs[Math.floor(Math.random() * npcs.length)];
            this.modifyRelationship(randomNpc, -event.effects.relationship_loss);
        }

        // Show event modal
        if (typeof window !== 'undefined' && window.UI) {
            window.UI.showEventModal(event, type);
        }
    }

    // Competitor AI actions
    competitorActions() {
        // Netflix occasionally raises bid
        if (Math.random() < 0.05 && this.state.competitorBids.netflix < this.state.currentBid) {
            const increase = (Math.random() * 2 + 1).toFixed(2);
            this.state.competitorBids.netflix = parseFloat(this.state.competitorBids.netflix) + parseFloat(increase);
            this.addEvent(`Netflix raised their bid to $${this.state.competitorBids.netflix.toFixed(2)}/share!`, 'negative');
        }

        // Random competitor moves
        if (Math.random() < 0.03) {
            const events = [
                'Netflix executives met with David Zaslav in secret.',
                'Comcast is rumored to be reconsidering their withdrawal.',
                'Netflix hired additional antitrust lawyers.',
                'Industry analysts predict a bidding war.'
            ];
            this.addEvent(events[Math.floor(Math.random() * events.length)], 'neutral');
        }
    }

    // Resource modification methods
    modifyInfluence(amount) {
        this.state.influence = Math.max(0, Math.min(100, this.state.influence + amount));
    }

    modifyReputation(amount) {
        this.state.reputation = Math.max(0, Math.min(100, this.state.reputation + amount));
    }

    modifyCash(amount) {
        this.state.cash += amount;
        if (this.state.cash < 0) {
            this.addEvent('WARNING: Running out of cash!', 'negative');
        }
    }

    modifyRelationship(npcId, amount) {
        if (this.state.relationships[npcId] !== undefined) {
            this.state.relationships[npcId] = Math.max(0, Math.min(100, this.state.relationships[npcId] + amount));
        }
    }

    modifyShareholderSupport(amount) {
        for (let shareholder in this.state.shareholderSupport) {
            this.state.shareholderSupport[shareholder] = Math.max(0, Math.min(100,
                this.state.shareholderSupport[shareholder] + amount));
        }
    }

    // Raise bid
    raiseBid(newBid) {
        if (newBid <= this.state.currentBid) {
            return { success: false, message: 'New bid must be higher than current bid!' };
        }

        const increase = newBid - this.state.currentBid;
        const totalCost = increase * GAME_DATA.config.wbd_shares;

        if (totalCost > this.state.cash + this.state.debtCapacity) {
            return { success: false, message: 'Not enough financing available!' };
        }

        this.state.currentBid = newBid;
        this.addEvent(`You raised your bid to $${newBid.toFixed(2)}/share`, 'positive');

        // Improve shareholder support
        this.modifyShareholderSupport(5);

        return { success: true, message: 'Bid increased successfully!' };
    }

    // Execute political action
    executePoliticalAction(actionId) {
        const action = GAME_DATA.political_actions.find(a => a.id === actionId);
        if (!action) return { success: false, message: 'Action not found!' };

        // Check cooldown
        if (this.state.cooldowns[actionId] && this.state.cooldowns[actionId] > 0) {
            return { success: false, message: `Action on cooldown for ${this.state.cooldowns[actionId]} more days!` };
        }

        // Check costs
        if (action.cost.influence && this.state.influence < action.cost.influence) {
            return { success: false, message: 'Not enough political influence!' };
        }
        if (action.cost.cash && this.state.cash < action.cost.cash) {
            return { success: false, message: 'Not enough cash!' };
        }

        // Pay costs
        if (action.cost.influence) this.modifyInfluence(-action.cost.influence);
        if (action.cost.cash) this.modifyCash(-action.cost.cash);

        // Apply effects
        if (action.effects === 'dialogue') {
            // Trigger dialogue
            if (typeof window !== 'undefined' && window.Negotiations) {
                window.Negotiations.startDialogue(actionId);
            }
        } else {
            if (action.effects.antitrust_pressure) {
                this.state.antitrustPressure += action.effects.antitrust_pressure;
            }
            if (action.effects.reputation) {
                this.modifyReputation(action.effects.reputation);
            }
            if (action.effects.shareholder_support) {
                this.modifyShareholderSupport(action.effects.shareholder_support);
            }
        }

        // Set cooldown
        if (action.cooldown) {
            this.state.cooldowns[actionId] = action.cooldown;
        }

        this.addEvent(`Executed: ${action.name}`, 'positive');
        return { success: true, message: `${action.name} executed successfully!` };
    }

    // Event log
    addEvent(text, type = 'neutral') {
        this.state.eventLog.push({
            day: this.state.currentDay,
            text: text,
            type: type,
            timestamp: Date.now()
        });

        // Keep only last 50 events
        if (this.state.eventLog.length > 50) {
            this.state.eventLog.shift();
        }
    }

    // Check win/loss conditions
    checkGameEnd() {
        const daysRemaining = GAME_DATA.config.deadline_day - this.state.currentDay;

        // Time's up
        if (daysRemaining <= 0) {
            this.endGame('timeout');
            return;
        }

        // Bankruptcy
        if (this.state.cash < -10) {
            this.endGame('bankruptcy');
            return;
        }

        // Antitrust blocked
        if (this.state.antitrustPressure > GAME_DATA.config.antitrust_threshold) {
            this.endGame('antitrust');
            return;
        }

        // Check if won
        if (this.state.currentBid >= GAME_DATA.config.min_winning_bid &&
            this.state.relationships.zaslav >= 70) {
            this.endGame('victory');
            return;
        }
    }

    // End game
    endGame(reason) {
        this.state.isGameActive = false;

        if (typeof window !== 'undefined' && window.UI) {
            window.UI.showGameEnd(reason, this.state);
        }
    }

    // Save/Load game
    saveGame() {
        try {
            localStorage.setItem(this.saveKey, JSON.stringify(this.state));
        } catch (e) {
            console.error('Failed to save game:', e);
        }
    }

    loadGame() {
        try {
            const saved = localStorage.getItem(this.saveKey);
            if (saved) {
                this.state = JSON.parse(saved);
                this.state.currentDate = new Date(this.state.currentDate);
                return true;
            }
        } catch (e) {
            console.error('Failed to load game:', e);
        }
        return false;
    }

    // Get state
    getState() {
        return { ...this.state };
    }
}

// Create global game instance
if (typeof window !== 'undefined') {
    window.Game = new GameEngine();
}
