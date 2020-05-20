#!/usr/bin/env python3
import logging

from dinogame import DinoGame
from .autonomous_agent import AutonomousAgent

if __name__ == "__main__":
    # set the log level to INFO
    logging.basicConfig(level=logging.INFO)

    # create a new instance of the game
    game = DinoGame()

    # create a new autonomous agent to play the game
    agent = AutonomousAgent(game, True, 0.5)

    # start the game
    game.start()
