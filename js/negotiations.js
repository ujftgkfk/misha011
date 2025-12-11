// Media Mogul: Negotiations System

class NegotiationsSystem {
    constructor() {
        this.currentDialogue = null;
    }

    // Start a dialogue
    startDialogue(dialogueId) {
        const dialogue = GAME_DATA.dialogues[dialogueId];
        if (!dialogue) {
            console.error('Dialogue not found:', dialogueId);
            return;
        }

        this.currentDialogue = dialogue;
        this.showDialogue(dialogue);
    }

    // Show dialogue UI
    showDialogue(dialogue) {
        const npcData = GAME_DATA.npcs[dialogue.npc];
        const state = window.Game.getState();

        let content = `
            <div class="dialogue-container">
                <div class="dialogue-character">
                    <div class="dialogue-portrait">${npcData.portrait}</div>
                    <div class="dialogue-info">
                        <div class="dialogue-name">${npcData.name}</div>
                        <div class="dialogue-title">${npcData.title}</div>
                        <div class="dialogue-mood">
                            ${this.getMoodEmoji(state.relationships[dialogue.npc])}
                            Relationship: ${state.relationships[dialogue.npc]}/100
                        </div>
                    </div>
                </div>

                <div class="dialogue-text">
                    "${dialogue.text}"
                </div>

                <h4>Your Response:</h4>
                <div class="dialogue-choices">
                    ${dialogue.choices.map((choice, index) =>
                        this.renderChoice(choice, index, state)
                    ).join('')}
                </div>
            </div>
        `;

        window.UI.showModal(`Meeting with ${npcData.name}`, content);
    }

    // Render a dialogue choice
    renderChoice(choice, index, state) {
        const canAfford = this.canAffordChoice(choice, state);
        const costText = this.getChoiceCostText(choice);

        return `
            <button class="choice-button ${!canAfford ? 'disabled' : ''}"
                    onclick="window.Negotiations.selectChoice(${index})"
                    ${!canAfford ? 'disabled' : ''}>
                <span class="choice-text">${choice.text}</span>
                <div class="choice-meta">
                    ${costText}
                    ${choice.risk > 0 ? `<span class="choice-risk">Risk: ${(choice.risk * 100).toFixed(0)}%</span>` : ''}
                </div>
            </button>
        `;
    }

    // Check if player can afford choice
    canAffordChoice(choice, state) {
        if (choice.cost.cash && state.cash < choice.cost.cash) return false;
        if (choice.cost.influence && state.influence < choice.cost.influence) return false;
        if (choice.cost.reputation && state.reputation < choice.cost.reputation) return false;
        return true;
    }

    // Get cost text for choice
    getChoiceCostText(choice) {
        let costParts = [];

        if (choice.cost.cash) {
            costParts.push(`<span class="choice-cost">💰 $${choice.cost.cash}B</span>`);
        }
        if (choice.cost.influence) {
            costParts.push(`<span class="choice-cost">🏛️ ${choice.cost.influence} Influence</span>`);
        }
        if (choice.cost.reputation) {
            costParts.push(`<span class="choice-cost">⭐ ${choice.cost.reputation} Reputation</span>`);
        }

        return costParts.join(' ');
    }

    // Select a choice
    selectChoice(index) {
        if (!this.currentDialogue) return;

        const choice = this.currentDialogue.choices[index];
        const state = window.Game.getState();

        // Pay costs
        if (choice.cost.cash) window.Game.modifyCash(-choice.cost.cash);
        if (choice.cost.influence) window.Game.modifyInfluence(-choice.cost.influence);
        if (choice.cost.reputation) window.Game.modifyReputation(-choice.cost.reputation);

        // Determine success/failure
        const roll = Math.random();
        const success = roll > choice.risk;

        // Apply effects
        const effects = success ? choice.success_effects : choice.failure_effects;

        if (effects.relationship) {
            window.Game.modifyRelationship(this.currentDialogue.npc, effects.relationship);
        }
        if (effects.influence) {
            window.Game.modifyInfluence(effects.influence);
        }
        if (effects.reputation) {
            window.Game.modifyReputation(effects.reputation);
        }
        if (effects.bid_increase) {
            const newBid = state.currentBid + effects.bid_increase;
            window.Game.raiseBid(newBid);
        }

        // Show result
        this.showDialogueResult(choice, success, effects);

        // Update UI
        window.UI.render();
    }

    // Show dialogue result
    showDialogueResult(choice, success, effects) {
        const npcData = GAME_DATA.npcs[this.currentDialogue.npc];

        let resultText = success
            ? `<p class="text-success">✅ Your approach worked!</p>`
            : `<p class="text-danger">❌ That didn't go as planned...</p>`;

        let effectsList = '<ul>';
        if (effects.relationship) {
            const sign = effects.relationship > 0 ? '+' : '';
            effectsList += `<li>Relationship with ${npcData.name}: ${sign}${effects.relationship}</li>`;
        }
        if (effects.influence) {
            const sign = effects.influence > 0 ? '+' : '';
            effectsList += `<li>Political Influence: ${sign}${effects.influence}</li>`;
        }
        if (effects.reputation) {
            const sign = effects.reputation > 0 ? '+' : '';
            effectsList += `<li>Reputation: ${sign}${effects.reputation}</li>`;
        }
        if (effects.bid_increase) {
            effectsList += `<li>Bid increased by $${effects.bid_increase.toFixed(2)}/share</li>`;
        }
        effectsList += '</ul>';

        const content = `
            <div class="dialogue-result">
                ${resultText}
                <p><strong>You chose:</strong> ${choice.text}</p>
                <h4>Effects:</h4>
                ${effectsList}
            </div>
        `;

        const footer = '<button class="btn-primary" onclick="window.UI.hideModal()">Continue</button>';

        window.UI.showModal('Result', content, footer);

        this.currentDialogue = null;
    }

    // Get mood emoji based on relationship
    getMoodEmoji(relationship) {
        if (relationship >= 80) return '😊';
        if (relationship >= 60) return '🙂';
        if (relationship >= 40) return '😐';
        if (relationship >= 20) return '😠';
        return '😡';
    }

    // Random encounter system
    triggerRandomEncounter() {
        // Chance for random NPC encounter
        const state = window.Game.getState();

        if (Math.random() < 0.1) {
            const npcs = Object.keys(GAME_DATA.npcs);
            const randomNpc = npcs[Math.floor(Math.random() * npcs.length)];

            const encounters = [
                {
                    text: `You ran into ${GAME_DATA.npcs[randomNpc].name} at a Hollywood event.`,
                    effect: 5
                },
                {
                    text: `${GAME_DATA.npcs[randomNpc].name} called you unexpectedly.`,
                    effect: 3
                },
                {
                    text: `You had an informal chat with ${GAME_DATA.npcs[randomNpc].name}.`,
                    effect: 2
                }
            ];

            const encounter = encounters[Math.floor(Math.random() * encounters.length)];

            window.Game.modifyRelationship(randomNpc, encounter.effect);
            window.Game.addEvent(encounter.text, 'positive');
        }
    }

    // Hostile takeover attempt
    launchHostileTakeover() {
        const state = window.Game.getState();

        // Check if player has enough shareholder support
        let totalSupport = 0;
        let totalOwnership = 0;

        for (let id in state.shareholderSupport) {
            const shareholder = GAME_DATA.shareholders[id];
            totalSupport += (state.shareholderSupport[id] / 100) * shareholder.ownership;
            totalOwnership += shareholder.ownership;
        }

        const averageSupport = (totalSupport / totalOwnership) * 100;

        if (averageSupport < GAME_DATA.config.shareholder_threshold) {
            window.UI.showNotification('Not enough shareholder support for hostile takeover!', 'error');
            return false;
        }

        // Launch hostile takeover
        window.Game.state.gamePhase = 'hostile';
        window.Game.addEvent('You have launched a HOSTILE TAKEOVER attempt!', 'positive');

        const content = `
            <div class="hostile-takeover">
                <h3>🚨 Hostile Takeover Launched!</h3>
                <p>You have bypassed the board and are going directly to shareholders.</p>
                <p>Current shareholder support: <strong>${averageSupport.toFixed(1)}%</strong></p>
                <p>You need 50%+ support to succeed.</p>
                <p>⚠️ This is a high-risk move that will damage relationships!</p>
            </div>
        `;

        const footer = '<button class="btn-primary" onclick="window.UI.hideModal()">Continue</button>';

        window.UI.showModal('Hostile Takeover', content, footer);

        // Apply penalties
        window.Game.modifyRelationship('zaslav', -30);
        window.Game.modifyReputation(-20);

        return true;
    }
}

// Create global negotiations instance
if (typeof window !== 'undefined') {
    window.Negotiations = new NegotiationsSystem();
}
