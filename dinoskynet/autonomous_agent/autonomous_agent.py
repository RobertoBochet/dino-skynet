import logging
import time

from cv2 import cv2 as cv

from dinogame import DinoGame

# we prepare the logger
_LOGGER = logging.getLogger(__package__)


class AutonomousAgent:
    def __init__(self, game: DinoGame, show_processed_frame: bool = False, death_delay: float = 0):
        # the flag that controls if the processed frame must will be shown
        self._show_processed_frame = show_processed_frame

        # the amount of time must will be waited after a death
        self._death_delay = death_delay

        # we attach the callbacks
        self._attach_callback(game)

    def _attach_callback(self, game: DinoGame):
        # we use methods of instance as callbacks
        # so we have to use a lambda to give the instance parameter to the callback methods
        game.loop_callback.set(self._handle_loop)
        game.gameover_callback.set(self._handle_gameover)

    def _handle_loop(self, game: DinoGame):
        # we log if the load value is too high
        if game.load > 1.0:
            _LOGGER.warning("The load has exceeded the limit, with {}".format(game.load))
        elif game.load > 0.85:
            _LOGGER.warning("The load is close to the limit, with {}".format(game.load))

        # Let's retrieve the current frame
        frame = game.frame

        # pygame uses notation W,H, opencv2 uses notation H,W
        # so we need to transpose the frame matrix
        frame = cv.transpose(frame)

        # the game is in grayscale so it is easier work with a grayscale image
        frame = cv.cvtColor(frame, cv.COLOR_RGB2GRAY)

        # There are many small objects on screen
        # we apply a blur filter to reduce the image complexity
        frame = cv.medianBlur(frame, 5)

        # we show the processed frame only if it is required
        if self._show_processed_frame:
            cv.imshow("screen", frame)
            cv.waitKey(1)

    def _handle_gameover(self, game: DinoGame):
        # the game is over, we report the event with the session's score
        _LOGGER.info("The game is over with the score of {}".format(game.score))

        # waits a moment
        time.sleep(self._death_delay)

        # we restart the game
        game.reset()
        game.start_running()
