#!/usr/bin/env python3
"""
THIS IS THE PRESIDENT - Exact Copy
Complete recreation of the original game

Pass the 28th Amendment. By any means necessary.
"""

from src.core.game_titp import GameTITP


def main():
    """Start This Is the President"""
    print("=" * 70)
    print("THIS IS THE PRESIDENT - Exact Game Copy")
    print("=" * 70)
    print()
    print("You are the President of the United States.")
    print("You committed crimes before taking office.")
    print("Law enforcement is closing in.")
    print()
    print("Your only way out: Pass the 28th Amendment.")
    print("It will grant you presidential immunity - forever.")
    print()
    print("You have 4 years. You need 67 votes in Congress.")
    print()
    print("=" * 70)
    print("STARTING GAME...")
    print("=" * 70)
    print()

    game = GameTITP()
    game.run()


if __name__ == "__main__":
    main()
