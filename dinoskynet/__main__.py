#!/usr/bin/env python3
import logging

from dinogame import DinoGame
from .autonomous_agent import AutonomousAgent

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

    game = DinoGame(fps=60)

    agent = AutonomousAgent(game, True, 0.5)

    game.start()
