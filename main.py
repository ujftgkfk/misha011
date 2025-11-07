#!/usr/bin/env python3
"""
Political Strategy Game
Main entry point
"""

from src.core.game import Game


def main():
    """Start the game"""
    game = Game()
    game.run()


if __name__ == "__main__":
    main()
