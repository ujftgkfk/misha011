#!/usr/bin/env python3
"""
This Is the President - Political Survival Game
Main entry point for presidential version
"""

from src.core.game_president import Game


def main():
    """Start the presidential game"""
    print("=" * 60)
    print("THIS IS THE PRESIDENT")
    print("Do whatever it takes to survive")
    print("=" * 60)
    print()
    print("GOAL: Pass immunity amendment OR survive 4 years")
    print("Avoid: Impeachment, scandals, investigations")
    print()
    print("Starting game...")
    print()

    game = Game()
    game.run()


if __name__ == "__main__":
    main()
