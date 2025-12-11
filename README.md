# 🎬 Media Mogul: The Warner Bros. War

> A strategic business simulation game based on the real-life bidding war for Warner Bros. Discovery

![Game Version](https://img.shields.io/badge/version-1.0.0-gold)
![Status](https://img.shields.io/badge/status-Alpha-orange)
![Platform](https://img.shields.io/badge/platform-Web%20Browser-blue)

## 🎮 About

**Media Mogul** is a browser-based strategy game where you compete to acquire Warner Bros. Discovery in a high-stakes bidding war. Navigate corporate negotiations, political lobbying, shareholder relations, and regulatory approval to close the deal of the century.

**Key Features:**
- 💰 Resource management (cash, influence, reputation)
- 🤝 Dynamic negotiations with CEOs and politicians
- 📊 Competitive bidding rounds
- 🏛️ Political lobbying system
- 📰 Random events and market dynamics
- ⚖️ Antitrust regulatory challenges

## 🚀 Quick Start

### Play Instantly

Simply open `index.html` in any modern web browser (Chrome, Firefox, Edge, Safari).

### Local Server (Recommended)

For better performance:

```bash
# Python 3
python -m http.server 8000

# Node.js
npx http-server -p 8000
```

Then visit `http://localhost:8000`

## 📖 How to Play

1. **Start as Paramount Skydance** (more factions coming soon)
2. **Manage your resources**: Cash, Political Influence, Reputation
3. **Build relationships** with David Zaslav (WBD CEO) and Donald Trump
4. **Make competitive bids** in 3 bidding rounds
5. **Win approval** from board, shareholders, and regulators

### Win Conditions

- Bid ≥ $35/share
- Zaslav relationship ≥ 70/100
- Shareholder support > 50%
- Antitrust pressure < 50

**Deadline: 120 days**

## 🎯 Game Mechanics

### Actions

- **Negotiate** - Meet with CEOs, politicians, regulators
- **Finance** - Raise bids, secure funding
- **Politics** - Lobby DOJ/FTC, work with Trump
- **Shareholders** - Win institutional investor support

### Resources

- 💰 **Cash** ($40.7B starting)
- 🏛️ **Political Influence** (0-100)
- ⭐ **Reputation** (0-100)

### Key NPCs

- **David Zaslav** - CEO of WBD (most important!)
- **Donald Trump** - US President (political support)
- **Jonathan Kanter** - DOJ Antitrust Chief
- **Lina Khan** - FTC Chair
- **Larry Ellison** - Your father (financial backing)

## ⌨️ Keyboard Shortcuts

- `Space/Enter` - Next day
- `1` - Negotiate
- `2` - Finance
- `3` - Politics
- `4` - Shareholders
- `Esc` - Close modal
- `Ctrl+S` - Manual save

## 🛠️ Debug Commands

Open browser console (F12):

```javascript
DEBUG.showState()           // View game state
DEBUG.addCash(10)           // Add $10B cash
DEBUG.addInfluence(20)      // Add 20 influence
DEBUG.setRelationship('zaslav', 80)  // Set relationship
DEBUG.jumpToDay(80)         // Jump to day
DEBUG.win()                 // Instant win
DEBUG.listEvents()          // Show all events
```

## 📁 Project Structure

```
misha011/
├── index.html              # Main game page
├── css/
│   ├── main.css           # Core styles
│   └── ui.css             # UI components
├── js/
│   ├── data.js            # Game data
│   ├── game.js            # Game engine
│   ├── ui.js              # UI controller
│   ├── negotiations.js    # Dialogue system
│   ├── events.js          # Events system
│   └── main.js            # Entry point
├── GAME_README.md         # Detailed game guide (Russian)
└── README.md              # This file
```

## 🎯 Strategies

### Diplomatic Strategy
- Focus on building relationships
- Patient bidding approach
- Lower risk, slower progress

### Aggressive Strategy
- High bids early
- Active lobbying
- High risk, fast results

### Political Strategy
- Leverage Trump connections
- Work with regulators early
- Requires high influence

### Hostile Takeover
- Bypass the board
- Go directly to shareholders
- Damages reputation, high risk

## 🚧 Roadmap

### Version 1.1
- More dialogues and meetings
- Detailed financing system
- Sound effects and music
- Animations

### Version 1.2
- Multiplayer (2-3 players)
- Sandbox mode
- Historical scenarios
- Achievements system

### Version 2.0
- 3D office visualization
- Voice acting
- Mobile app
- Steam release

## 🐛 Known Issues

- Saves are browser-specific (use same browser)
- Mobile UI needs optimization
- Some dialogues not yet implemented

## 🤝 Contributing

This is a personal project, but suggestions and bug reports are welcome!

## 📜 License

© 2025 Media Mogul Game. All rights reserved.

**Disclaimer:** This is a fictional game based on public news. All characters and events are used for entertainment purposes only.

## 🎮 Easter Egg

Try the Konami Code: ⬆️⬆️⬇️⬇️⬅️➡️⬅️➡️BA

---

**Made with ❤️ using vanilla JavaScript**

*No frameworks. No dependencies. Just pure gaming fun!*
