// Media Mogul: Game Data

const GAME_DATA = {
    // Player Factions
    factions: {
        paramount: {
            id: 'paramount',
            name: 'Paramount Skydance',
            color: '#003087',
            ceo: 'David Ellison',
            resources: {
                cash: 40.7, // in billions
                stock: 0,
                debt_capacity: 54,
                influence: 75,
                reputation: 60
            },
            advantages: ['Trump connections', 'More cash available', 'Ellison family backing'],
            disadvantages: ['Smaller company size', 'Less market cap']
        },
        netflix: {
            id: 'netflix',
            name: 'Netflix',
            color: '#E50914',
            ceo: 'Ted Sarandos & Greg Peters',
            resources: {
                cash: 7,
                stock: 50,
                debt_capacity: 59,
                influence: 60,
                reputation: 75
            },
            advantages: ['Market cap', 'Global reach', 'Content library'],
            disadvantages: ['Antitrust risks', 'Zaslav\'s bias against them']
        },
        comcast: {
            id: 'comcast',
            name: 'Comcast',
            color: '#7F3F98',
            ceo: 'Brian Roberts',
            resources: {
                cash: 15,
                stock: 30,
                debt_capacity: 70,
                influence: 70,
                reputation: 65
            },
            advantages: ['M&A experience', 'Vertical integration', 'NBC Universal'],
            disadvantages: ['Regulatory problems', 'Already owns NBCUniversal']
        }
    },

    // NPCs (Non-Player Characters)
    npcs: {
        zaslav: {
            id: 'zaslav',
            name: 'David Zaslav',
            title: 'CEO, Warner Bros. Discovery',
            portrait: 'DZ',
            mood: 'neutral',
            relationship: 45,
            bias: {
                paramount: 0,
                netflix: -15, // Biased against Netflix
                comcast: 5
            },
            motivations: ['Maximize personal compensation ($660M)', 'Quick deal', 'Cash preferred'],
            influence: 10
        },
        trump: {
            id: 'trump',
            name: 'Donald Trump',
            title: 'President of the United States',
            portrait: 'DT',
            mood: 'watching',
            relationship: 60,
            bias: {
                paramount: 15, // Likes Ellison
                netflix: -10, // Dislikes "liberal media"
                comcast: 0
            },
            motivations: ['Political loyalty', 'Business success stories', 'Personal relationships'],
            influence: 10
        },
        kanter: {
            id: 'kanter',
            name: 'Jonathan Kanter',
            title: 'DOJ Antitrust Chief',
            portrait: 'JK',
            mood: 'skeptical',
            relationship: 30,
            bias: {
                paramount: 5,
                netflix: -20, // Antitrust concerns
                comcast: -15
            },
            motivations: ['Prevent monopolies', 'Protect competition', 'Content diversity'],
            influence: 9
        },
        khan: {
            id: 'khan',
            name: 'Lina Khan',
            title: 'FTC Chair',
            portrait: 'LK',
            mood: 'concerned',
            relationship: 25,
            bias: {
                paramount: 0,
                netflix: -25,
                comcast: -20
            },
            motivations: ['Block big mergers', 'Protect consumers', 'Market competition'],
            influence: 9
        },
        ellison_larry: {
            id: 'ellison_larry',
            name: 'Larry Ellison',
            title: 'Founder, Oracle (David\'s father)',
            portrait: 'LE',
            mood: 'supportive',
            relationship: 95,
            bias: {
                paramount: 50
            },
            motivations: ['Support his son', 'Good investment', 'Tech empire'],
            influence: 8
        }
    },

    // Major Shareholders
    shareholders: {
        vanguard: {
            id: 'vanguard',
            name: 'Vanguard Group',
            ownership: 10.2,
            stance: 'neutral',
            priorities: ['Shareholder value', 'Long-term growth', 'Governance']
        },
        blackrock: {
            id: 'blackrock',
            name: 'BlackRock',
            ownership: 7.8,
            stance: 'neutral',
            priorities: ['ESG concerns', 'Financial returns', 'Market stability']
        },
        statestreet: {
            id: 'statestreet',
            name: 'State Street',
            ownership: 4.9,
            stance: 'neutral',
            priorities: ['Shareholder returns', 'Deal certainty', 'Management quality']
        },
        oakmark: {
            id: 'oakmark',
            name: 'Harris Oakmark',
            ownership: 3.5,
            stance: 'activist',
            priorities: ['Maximize price', 'Quick close', 'Competitive bidding']
        }
    },

    // Random Events
    events: {
        positive: [
            {
                id: 'trump_dinner',
                title: 'Mar-a-Lago Invitation',
                description: 'Trump has invited you to dinner at Mar-a-Lago. This is a huge opportunity!',
                effects: { influence: 50, reputation: 10 },
                probability: 0.05
            },
            {
                id: 'wsj_article',
                title: 'Positive WSJ Coverage',
                description: 'The Wall Street Journal published a glowing article about your bid.',
                effects: { reputation: 20, shareholder_support: 10 },
                probability: 0.1
            },
            {
                id: 'shareholder_endorsement',
                title: 'Major Shareholder Support',
                description: 'A large institutional investor has publicly endorsed your offer.',
                effects: { shareholder_support: 15, reputation: 10 },
                probability: 0.08
            },
            {
                id: 'competitor_stumble',
                title: 'Competitor Makes Mistake',
                description: 'Your competitor made a public relations blunder.',
                effects: { reputation: 15 },
                probability: 0.12
            },
            {
                id: 'financing_secured',
                title: 'Easy Financing',
                description: 'Banks are offering better terms than expected for your debt financing.',
                effects: { debt_capacity: 5 },
                probability: 0.1
            }
        ],
        negative: [
            {
                id: 'guild_opposition',
                title: 'Directors Guild Opposes Deal',
                description: 'The Directors Guild of America has come out against your acquisition.',
                effects: { reputation: -30, influence: -10 },
                probability: 0.08
            },
            {
                id: 'info_leak',
                title: 'Confidential Information Leaked',
                description: 'Internal negotiations have been leaked to the press.',
                effects: { reputation: -25, relationship_loss: 15 },
                probability: 0.1
            },
            {
                id: 'antitrust_suit',
                title: 'State Antitrust Lawsuit',
                description: 'California has filed a preemptive antitrust lawsuit.',
                effects: { delay: 90, influence: -20 },
                probability: 0.05
            },
            {
                id: 'trump_criticism',
                title: 'Trump Criticizes on Truth Social',
                description: 'Trump posted criticism about your company on Truth Social.',
                effects: { influence: -40, reputation: -15 },
                probability: 0.06
            },
            {
                id: 'stock_drop',
                title: 'Stock Market Volatility',
                description: 'Market downturn has affected your stock-based financing.',
                effects: { stock_value: -15 },
                probability: 0.15
            },
            {
                id: 'competitor_raises',
                title: 'Competitor Raises Bid',
                description: 'Your main competitor has increased their offer significantly.',
                effects: { pressure: 20 },
                probability: 0.12
            }
        ],
        neutral: [
            {
                id: 'media_attention',
                title: 'Media Coverage Increases',
                description: 'The media is paying more attention to the bidding war.',
                effects: {},
                probability: 0.2
            },
            {
                id: 'analyst_report',
                title: 'Analyst Report Published',
                description: 'Industry analysts have published their take on the deal.',
                effects: {},
                probability: 0.15
            }
        ]
    },

    // Bidding Rounds
    bidding_rounds: [
        {
            round: 1,
            date: 'November 20, 2025',
            day: 80,
            description: 'First round of formal bids',
            min_bid: 25.00
        },
        {
            round: 2,
            date: 'December 1, 2025',
            day: 91,
            description: 'Second round - best and final',
            min_bid: 28.00
        },
        {
            round: 3,
            date: 'December 4, 2025',
            day: 94,
            description: 'Final round',
            min_bid: 30.00
        }
    ],

    // Dialogue Options
    dialogues: {
        zaslav_meeting_1: {
            npc: 'zaslav',
            text: "Your offer is interesting, but Netflix has the scale we need. They can close faster and with less regulatory scrutiny. What makes your bid better?",
            choices: [
                {
                    id: 'offer_ceo_role',
                    text: 'Offer him co-CEO role in the combined company',
                    cost: { reputation: -10 },
                    risk: 0.4,
                    success_effects: { relationship: 30 },
                    failure_effects: { relationship: -15, reputation: -20 }
                },
                {
                    id: 'raise_bid',
                    text: 'Raise offer to $32/share',
                    cost: { cash: 6 },
                    risk: 0,
                    success_effects: { relationship: 20, bid_increase: 2 },
                    failure_effects: {}
                },
                {
                    id: 'mention_trump',
                    text: 'Mention your connections with Trump and regulatory advantages',
                    cost: { influence: 10 },
                    risk: 0.2,
                    success_effects: { relationship: 15, influence: 10 },
                    failure_effects: { relationship: -5 }
                },
                {
                    id: 'criticize_netflix',
                    text: 'Point out Netflix\'s antitrust problems',
                    cost: {},
                    risk: 0.3,
                    success_effects: { relationship: 10 },
                    failure_effects: { reputation: -15, relationship: -10 }
                }
            ]
        },
        trump_call: {
            npc: 'trump',
            text: "David! I heard you're going after Warner Bros. Good move. What do you need from me?",
            choices: [
                {
                    id: 'ask_endorsement',
                    text: 'Ask for a public endorsement',
                    cost: { influence: 30 },
                    risk: 0.3,
                    success_effects: { relationship: 20, reputation: 25, influence: 50 },
                    failure_effects: { relationship: -10, influence: -20 }
                },
                {
                    id: 'ask_regulatory',
                    text: 'Request help with DOJ/FTC approval',
                    cost: { influence: 40 },
                    risk: 0.4,
                    success_effects: { antitrust_pressure: -30 },
                    failure_effects: { relationship: -15 }
                },
                {
                    id: 'just_update',
                    text: 'Just update him and maintain relationship',
                    cost: { influence: 10 },
                    risk: 0,
                    success_effects: { relationship: 10 },
                    failure_effects: {}
                }
            ]
        }
    },

    // Finance Options
    finance_sources: {
        ellison_family: {
            id: 'ellison_family',
            name: 'Ellison Family Capital',
            available: 40.7,
            cost: 'No interest (family)',
            type: 'equity',
            available_to: ['paramount']
        },
        saudi_pif: {
            id: 'saudi_pif',
            name: 'Saudi PIF',
            available: 8,
            cost: '5% + board seat',
            type: 'equity',
            available_to: ['paramount']
        },
        debt_financing: {
            id: 'debt_financing',
            name: 'Bank Debt',
            available: 54,
            cost: '6.5% interest rate',
            type: 'debt',
            available_to: ['all']
        },
        bridge_loan: {
            id: 'bridge_loan',
            name: 'Bridge Loan',
            available: 20,
            cost: '8% interest rate',
            type: 'debt',
            available_to: ['all']
        }
    },

    // Political Actions
    political_actions: [
        {
            id: 'lobby_doj',
            name: 'Lobby Department of Justice',
            description: 'Hire top lawyers and lobbyists to make your case to the DOJ Antitrust Division.',
            cost: { influence: 20, cash: 0.1 },
            effects: { antitrust_pressure: -15 },
            cooldown: 14
        },
        {
            id: 'lobby_ftc',
            name: 'Lobby FTC',
            description: 'Present your case to the Federal Trade Commission.',
            cost: { influence: 20, cash: 0.1 },
            effects: { antitrust_pressure: -15 },
            cooldown: 14
        },
        {
            id: 'call_trump',
            name: 'Call Trump',
            description: 'Reach out to President Trump for support.',
            cost: { influence: 30 },
            effects: 'dialogue',
            cooldown: 30
        },
        {
            id: 'media_campaign',
            name: 'Public Media Campaign',
            description: 'Launch a PR campaign to build public support.',
            cost: { cash: 0.5, influence: 10 },
            effects: { reputation: 15, shareholder_support: 10 },
            cooldown: 7
        },
        {
            id: 'shareholder_presentation',
            name: 'Investor Roadshow',
            description: 'Present your vision to major institutional shareholders.',
            cost: { cash: 0.2 },
            effects: { shareholder_support: 20 },
            cooldown: 14
        }
    ],

    // Game Configuration
    config: {
        starting_day: 1,
        deadline_day: 120,
        starting_date: new Date('2025-09-01'),
        max_influence: 100,
        max_reputation: 100,
        wbd_valuation: 82.7, // billion
        wbd_shares: 2.45, // billion shares
        min_winning_bid: 35.00, // per share
        antitrust_threshold: 50, // if pressure exceeds this, deal blocked
        shareholder_threshold: 50 // % needed for hostile takeover
    }
};

// Export for use in other files
if (typeof module !== 'undefined' && module.exports) {
    module.exports = GAME_DATA;
}
