// Media Mogul: Events System

class EventsSystem {
    constructor() {
        this.triggeredEvents = new Set();
        this.scheduledEvents = [];
    }

    // Check and trigger scheduled events
    checkScheduledEvents(currentDay) {
        this.scheduledEvents = this.scheduledEvents.filter(event => {
            if (event.day === currentDay) {
                this.triggerEvent(event);
                return false; // Remove from scheduled
            }
            return true; // Keep in scheduled
        });
    }

    // Schedule an event for future
    scheduleEvent(event, day) {
        this.scheduledEvents.push({
            ...event,
            day: day
        });
    }

    // Trigger a specific event
    triggerEvent(event) {
        if (this.triggeredEvents.has(event.id)) {
            return; // Event already triggered
        }

        this.triggeredEvents.add(event.id);
        window.Game.applyEvent(event, event.type || 'neutral');
    }

    // Story events based on game progression
    checkStoryEvents(state) {
        // Early game events (Days 1-30)
        if (state.currentDay === 5 && !this.triggeredEvents.has('intro_competition')) {
            this.triggerEvent({
                id: 'intro_competition',
                title: 'The Competition Heats Up',
                description: 'Netflix has officially entered the race for Warner Bros. Discovery. This won\'t be easy.',
                effects: {},
                type: 'neutral'
            });
        }

        if (state.currentDay === 10 && state.currentBid < 28) {
            this.triggerEvent({
                id: 'low_bid_warning',
                title: 'Analysts Question Your Bid',
                description: 'Industry analysts are questioning whether your bid is competitive enough.',
                effects: { reputation: -10 },
                type: 'negative'
            });
        }

        // Mid game events (Days 31-80)
        if (state.currentDay === 40 && state.relationships.zaslav < 50) {
            this.triggerEvent({
                id: 'zaslav_concerns',
                title: 'Zaslav Has Concerns',
                description: 'David Zaslav has privately expressed doubts about your offer.',
                effects: { reputation: -15 },
                type: 'negative'
            });
        }

        if (state.currentDay === 50 && state.influence > 70) {
            this.triggerEvent({
                id: 'washington_insider',
                title: 'Washington Insider',
                description: 'Your political connections are paying off. Word in DC is that you have strong support.',
                effects: { reputation: 20 },
                type: 'positive'
            });
        }

        // Late game events (Days 81-120)
        if (state.currentDay === 90 && state.currentBid > state.competitorBids.netflix) {
            this.triggerEvent({
                id: 'leading_bid',
                title: 'You\'re in the Lead!',
                description: 'Your bid is now the highest. Netflix is scrambling to respond.',
                effects: { reputation: 15, shareholder_support: 10 },
                type: 'positive'
            });
        }

        if (state.currentDay === 100 && state.antitrustPressure > 40) {
            this.triggerEvent({
                id: 'regulatory_pressure',
                title: 'Regulatory Scrutiny Intensifies',
                description: 'The DOJ and FTC are taking a close look at all bids. Antitrust concerns are mounting.',
                effects: { antitrust_pressure: 10 },
                type: 'negative'
            });
        }

        // Relationship-based events
        if (state.relationships.trump >= 80 && !this.triggeredEvents.has('trump_endorsement')) {
            this.triggerEvent({
                id: 'trump_endorsement',
                title: 'Trump Endorsement!',
                description: 'President Trump has publicly endorsed your bid on Truth Social!',
                effects: { influence: 30, reputation: 25 },
                type: 'positive'
            });
        }

        if (state.relationships.zaslav >= 70 && !this.triggeredEvents.has('zaslav_support')) {
            this.triggerEvent({
                id: 'zaslav_support',
                title: 'Zaslav\'s Support',
                description: 'David Zaslav has indicated that he favors your offer.',
                effects: { shareholder_support: 20, reputation: 20 },
                type: 'positive'
            });
        }

        // Crisis events
        if (state.cash < 10 && !this.triggeredEvents.has('cash_crisis')) {
            this.triggerEvent({
                id: 'cash_crisis',
                title: 'Cash Flow Crisis',
                description: 'You\'re running dangerously low on cash. Time to secure more financing!',
                effects: { reputation: -20 },
                type: 'negative'
            });
        }
    }

    // Special scenario events
    triggerMarketCrash() {
        this.triggerEvent({
            id: 'market_crash',
            title: 'Market Crash!',
            description: 'The stock market has crashed! All stock-based financing is now worth significantly less.',
            effects: { stock_value: -30 },
            type: 'negative'
        });
    }

    triggerRegulatoryInvestigation() {
        this.triggerEvent({
            id: 'doj_investigation',
            title: 'DOJ Investigation Launched',
            description: 'The Department of Justice has launched a formal antitrust investigation into your proposed merger.',
            effects: { antitrust_pressure: 25, delay: 60 },
            type: 'negative'
        });
    }

    // Trump-specific events
    trumpEvents = {
        dinner_invitation: {
            id: 'trump_dinner',
            title: 'Mar-a-Lago Dinner Invitation',
            description: 'President Trump has personally invited you to dinner at Mar-a-Lago. This is a golden opportunity!',
            effects: { influence: 40, relationship_trump: 20 },
            type: 'positive',
            choices: [
                {
                    text: 'Accept immediately',
                    cost: { cash: 0.1 },
                    effects: { relationship_trump: 25 }
                },
                {
                    text: 'Decline politely',
                    cost: {},
                    effects: { relationship_trump: -10 }
                }
            ]
        },

        truth_social_attack: {
            id: 'trump_attack',
            title: 'Trump Attacks on Truth Social',
            description: 'President Trump has posted a harsh criticism of your company on Truth Social!',
            effects: { influence: -30, reputation: -20 },
            type: 'negative'
        },

        regulatory_help: {
            id: 'trump_regulatory',
            title: 'Trump Clears the Way',
            description: 'President Trump has made calls to DOJ and FTC on your behalf.',
            effects: { antitrust_pressure: -30 },
            type: 'positive'
        }
    };

    // Media events
    mediaEvents = [
        {
            id: 'hollywood_reporter',
            title: 'Hollywood Reporter Feature',
            description: 'The Hollywood Reporter published a major feature about your bid.',
            probability: 0.08
        },
        {
            id: 'cnbc_interview',
            title: 'CNBC Interview Opportunity',
            description: 'CNBC wants to interview you about the acquisition.',
            probability: 0.1
        },
        {
            id: 'leak_to_press',
            title: 'Internal Memo Leaked',
            description: 'An internal strategy memo has been leaked to the press!',
            effects: { reputation: -15 },
            probability: 0.05,
            type: 'negative'
        }
    ];

    // Competitor events
    competitorEvents = {
        netflix_raises: [
            {
                amount: 1.5,
                description: 'Netflix has raised their bid by $1.50/share!',
                probability: 0.15
            },
            {
                amount: 2.0,
                description: 'Netflix has made a aggressive bid increase of $2.00/share!',
                probability: 0.08
            }
        ],

        netflix_problems: [
            {
                description: 'Netflix is facing regulatory pushback on their bid.',
                effects: { competitor_pressure: -10 },
                probability: 0.1
            },
            {
                description: 'Netflix executives had a poor meeting with Zaslav.',
                effects: { reputation: 10 },
                probability: 0.12
            }
        ],

        comcast_returns: {
            description: 'BREAKING: Comcast has re-entered the bidding war!',
            effects: { pressure: 20 },
            probability: 0.05
        }
    };

    // Guild and union events
    industryEvents = [
        {
            id: 'sag_support',
            title: 'SAG-AFTRA Support',
            description: 'The Screen Actors Guild has endorsed your bid, citing job protection.',
            effects: { reputation: 25, influence: 15 },
            type: 'positive',
            probability: 0.06
        },
        {
            id: 'dga_opposition',
            title: 'Directors Guild Opposition',
            description: 'The Directors Guild has come out against your acquisition.',
            effects: { reputation: -25, influence: -10 },
            type: 'negative',
            probability: 0.08
        },
        {
            id: 'wga_concerns',
            title: 'Writers Guild Concerns',
            description: 'The Writers Guild has expressed concerns about content consolidation.',
            effects: { reputation: -15 },
            type: 'negative',
            probability: 0.1
        }
    ];

    // Shareholder events
    shareholderEvents = [
        {
            id: 'vanguard_support',
            title: 'Vanguard Backs Your Bid',
            description: 'Vanguard Group has announced support for your acquisition.',
            effects: { shareholder_vanguard: 20, reputation: 15 },
            type: 'positive',
            probability: 0.05
        },
        {
            id: 'activist_investor',
            title: 'Activist Investor Enters',
            description: 'An activist investor has taken a stake and is pushing for highest bid.',
            effects: { pressure: 15 },
            type: 'neutral',
            probability: 0.07
        },
        {
            id: 'proxy_fight',
            title: 'Proxy Fight Brewing',
            description: 'Some shareholders are threatening a proxy fight over the deal.',
            effects: { delay: 30, reputation: -10 },
            type: 'negative',
            probability: 0.04
        }
    ];

    // Generate random event from appropriate pool
    getRandomEvent(state) {
        const eventPools = [
            ...GAME_DATA.events.positive,
            ...GAME_DATA.events.negative,
            this.mediaEvents,
            this.industryEvents,
            this.shareholderEvents
        ].flat();

        const roll = Math.random();

        for (let event of eventPools) {
            if (event.probability && roll < event.probability) {
                return event;
            }
        }

        return null;
    }

    // Process special conditions
    checkSpecialConditions(state) {
        // Check if player is doing very well - trigger negative event
        if (state.currentBid > state.competitorBids.netflix + 3 &&
            state.relationships.zaslav > 70 &&
            !this.triggeredEvents.has('too_good')) {

            this.triggerEvent({
                id: 'too_good',
                title: 'Too Good To Be True?',
                description: 'Your strong position has attracted regulatory attention. The FTC wants to review your financing sources.',
                effects: { antitrust_pressure: 15, delay: 20 },
                type: 'negative'
            });
        }

        // Check if player is struggling - offer help
        if (state.currentBid < state.competitorBids.netflix - 2 &&
            state.cash < 20 &&
            !this.triggeredEvents.has('friendly_investor')) {

            this.triggerEvent({
                id: 'friendly_investor',
                title: 'Friendly Investor Offers Help',
                description: 'A friendly investor has offered to inject capital into your bid.',
                effects: { cash: 5 },
                type: 'positive'
            });
        }
    }
}

// Create global events instance
if (typeof window !== 'undefined') {
    window.Events = new EventsSystem();
}
