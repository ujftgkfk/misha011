// Media Mogul: Advanced Financing System

class FinancingSystem {
    constructor() {
        this.activeLoans = [];
        this.investors = this.initializeInvestors();
    }

    // Initialize investor data
    initializeInvestors() {
        return {
            ellison_family: {
                id: 'ellison_family',
                name: 'Ellison Family Trust',
                type: 'equity',
                available: 40.7,
                used: 0,
                cost: 0, // No interest - family
                terms: 'Family backing - no strings attached',
                relationship: 100,
                icon: '👨‍👦',
                available_to: ['paramount']
            },
            saudi_pif: {
                id: 'saudi_pif',
                name: 'Saudi Public Investment Fund',
                type: 'equity',
                available: 8,
                used: 0,
                cost: 0.05,
                terms: 'Requires board seat + 5% equity stake',
                relationship: 50,
                icon: '🇸🇦',
                requirements: { reputation: 40 },
                available_to: ['paramount']
            },
            qatar_qia: {
                id: 'qatar_qia',
                name: 'Qatar Investment Authority',
                type: 'equity',
                available: 8,
                used: 0,
                cost: 0.06,
                terms: 'Requires 6% equity stake',
                relationship: 45,
                icon: '🇶🇦',
                requirements: { reputation: 35 },
                available_to: ['paramount']
            },
            bofa: {
                id: 'bofa',
                name: 'Bank of America',
                type: 'debt',
                available: 20,
                used: 0,
                cost: 0.065,
                terms: '6.5% annual interest, 10-year term',
                relationship: 60,
                icon: '🏦',
                available_to: ['all']
            },
            jpmorgan: {
                id: 'jpmorgan',
                name: 'JPMorgan Chase',
                type: 'debt',
                available: 18,
                used: 0,
                cost: 0.07,
                terms: '7% annual interest, 10-year term',
                relationship: 55,
                icon: '🏦',
                available_to: ['all']
            },
            apollo: {
                id: 'apollo',
                name: 'Apollo Global Management',
                type: 'debt',
                available: 16,
                used: 0,
                cost: 0.085,
                terms: '8.5% interest - high risk lending',
                relationship: 50,
                icon: '🏛️',
                requirements: { cash: 10 },
                available_to: ['all']
            },
            bridge_loan: {
                id: 'bridge_loan',
                name: 'Bridge Financing',
                type: 'debt',
                available: 12,
                used: 0,
                cost: 0.10,
                terms: '10% interest - short term (2 years)',
                relationship: 40,
                icon: '⚡',
                available_to: ['all']
            },
            kushner_affinity: {
                id: 'kushner_affinity',
                name: 'Affinity Partners (Kushner)',
                type: 'equity',
                available: 5,
                used: 0,
                cost: 0.08,
                terms: 'Political connections included',
                relationship: 70,
                icon: '🤝',
                bonus: { influence: 20 },
                requirements: { trump_relationship: 60 },
                available_to: ['paramount']
            }
        };
    }

    // Get available investors for player
    getAvailableInvestors(playerFaction, gameState) {
        const available = [];

        for (let id in this.investors) {
            const investor = this.investors[id];

            // Check faction availability
            if (!investor.available_to.includes('all') &&
                !investor.available_to.includes(playerFaction)) {
                continue;
            }

            // Check requirements
            if (investor.requirements) {
                if (investor.requirements.reputation &&
                    gameState.reputation < investor.requirements.reputation) {
                    continue;
                }
                if (investor.requirements.cash &&
                    gameState.cash < investor.requirements.cash) {
                    continue;
                }
                if (investor.requirements.trump_relationship &&
                    gameState.relationships.trump < investor.requirements.trump_relationship) {
                    continue;
                }
            }

            available.push(investor);
        }

        return available;
    }

    // Raise funding from investor
    raiseFunding(investorId, amount, gameState) {
        const investor = this.investors[investorId];

        if (!investor) {
            return { success: false, message: 'Investor not found!' };
        }

        if (amount > investor.available - investor.used) {
            return { success: false, message: `Only $${(investor.available - investor.used).toFixed(1)}B available!` };
        }

        // Update investor
        investor.used += amount;

        // Update game state
        gameState.cash += amount;

        // Apply costs/bonuses
        if (investor.type === 'debt') {
            this.activeLoans.push({
                investor: investorId,
                amount: amount,
                rate: investor.cost,
                monthlyPayment: (amount * investor.cost) / 12
            });
        }

        if (investor.bonus) {
            if (investor.bonus.influence) {
                window.Game.modifyInfluence(investor.bonus.influence);
            }
        }

        // Improve relationship
        investor.relationship = Math.min(100, investor.relationship + 5);

        return {
            success: true,
            message: `Secured $${amount.toFixed(1)}B from ${investor.name}!`,
            investor: investor
        };
    }

    // Calculate monthly debt service
    getMonthlyDebtService() {
        let total = 0;
        this.activeLoans.forEach(loan => {
            total += loan.monthlyPayment;
        });
        return total;
    }

    // Get total debt
    getTotalDebt() {
        let total = 0;
        this.activeLoans.forEach(loan => {
            total += loan.amount;
        });
        return total;
    }

    // Calculate deal financing structure
    calculateDealFinancing(bidPerShare, gameState) {
        const totalShares = GAME_DATA.config.wbd_shares;
        const totalCost = bidPerShare * totalShares;

        const availableCash = gameState.cash;
        const needFinancing = Math.max(0, totalCost - availableCash);

        return {
            totalCost: totalCost,
            cashUsed: Math.min(totalCost, availableCash),
            financingNeeded: needFinancing,
            percentCash: (Math.min(totalCost, availableCash) / totalCost) * 100,
            percentDebt: (needFinancing / totalCost) * 100
        };
    }

    // Generate financing proposal
    generateProposal(bidPerShare, gameState) {
        const deal = this.calculateDealFinancing(bidPerShare, gameState);

        let proposal = `
            <div class="financing-proposal">
                <h3>Deal Financing Structure</h3>
                <div class="deal-summary">
                    <div class="deal-line">
                        <span>Bid per share:</span>
                        <strong>$${bidPerShare.toFixed(2)}</strong>
                    </div>
                    <div class="deal-line">
                        <span>Total shares:</span>
                        <strong>${GAME_DATA.config.wbd_shares.toFixed(2)}B</strong>
                    </div>
                    <div class="deal-line total">
                        <span>Total deal value:</span>
                        <strong>$${deal.totalCost.toFixed(1)}B</strong>
                    </div>
                </div>

                <h4>Financing Sources:</h4>
                <div class="financing-sources">
                    <div class="source-item cash">
                        <span class="source-label">💰 Cash on hand:</span>
                        <span class="source-amount">$${deal.cashUsed.toFixed(1)}B</span>
                        <span class="source-percent">(${deal.percentCash.toFixed(0)}%)</span>
                    </div>
                    ${deal.financingNeeded > 0 ? `
                        <div class="source-item debt">
                            <span class="source-label">📊 Financing needed:</span>
                            <span class="source-amount">$${deal.financingNeeded.toFixed(1)}B</span>
                            <span class="source-percent">(${deal.percentDebt.toFixed(0)}%)</span>
                        </div>
                    ` : ''}
                </div>

                ${deal.financingNeeded > 0 ? `
                    <div class="financing-warning">
                        ⚠️ You need to raise $${deal.financingNeeded.toFixed(1)}B in additional financing
                    </div>
                ` : `
                    <div class="financing-success">
                        ✅ Fully funded with cash - no debt needed!
                    </div>
                `}
            </div>
        `;

        return proposal;
    }
}

// Create global financing instance
if (typeof window !== 'undefined') {
    window.Financing = new FinancingSystem();
}
