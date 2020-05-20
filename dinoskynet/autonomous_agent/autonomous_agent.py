import logging
import time
from typing import Tuple, List, Union

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

    def _handle_gameover(self, game: DinoGame):
        # the game is over, we report the event with the session's score
        _LOGGER.info("The game is over with the score of {}".format(game.score))

        # waits a moment
        time.sleep(self._death_delay)

        # we restart the game
        game.reset()
        game.start_running()

    def _handle_loop(self, game: DinoGame):
        # logging if the load value is too high
        if game.load > 1.0:
            _LOGGER.warning("The load has exceeded the limit, with {}".format(game.load))
        elif game.load > 0.85:
            _LOGGER.warning("The load is close to the limit, with {}".format(game.load))

        # Let's retrieve the current frame
        frame = game.frame

        # process the frame
        player, obstacles = self._process_frame(frame)

        # do the decisions
        self._do_something(game, obstacles, player)

    def _process_frame(self, frame: "np.array") -> \
            Tuple[Union[None, Tuple[float, float, float, float]], List[Tuple[float, float, float, float]]]:
        # pygame uses notation W,H, opencv2 uses notation H,W
        # so we need to transpose the frame matrix
        original_frame = cv.transpose(frame)

        # the game is in grayscale so it is easier work with a grayscale image
        frame = cv.cvtColor(original_frame, cv.COLOR_RGB2GRAY)

        # There are many small objects on screen
        # apply a blur filter to reduce the image complexity
        frame = cv.medianBlur(frame, 5)

        # create a bitmap on the basis of threshold
        _, frame = cv.threshold(frame, 127, 255, 0)

        # for convention in a mask the positive value (255) is used to mark the useful area
        # in our case we have the opposite, so we need to invert the mask
        frame = cv.bitwise_not(frame)

        # find the blobs' contours
        contours, _ = cv.findContours(frame,
                                      cv.RETR_CCOMP,
                                      cv.CHAIN_APPROX_SIMPLE)

        # remove the smallest blobs (false positives)
        contours = filter(lambda c: cv.contourArea(c) > 50, contours)

        # enclose each blob in a rectangle
        entities = map(lambda c: cv.boundingRect(c), contours)

        # remap entities like x_min, x_max, y_min, y_max
        entities = list(map(lambda e: (e[0], e[0] + e[2], e[1], e[1] + e[3]), entities))

        # try to find the player
        player_candidates = list(filter(lambda e: 10 < e[0] and e[1] < 100, entities))

        # check if only one player is found
        player = None
        if len(player_candidates) == 1:
            player = player_candidates[0]

            # remove player from entities list
            entities = list(filter(lambda e: e is not player, entities))

        # show the processed frame only if it is required
        if self._show_processed_frame:
            output_frame = original_frame

            # draw the bounding rectangle of the player
            if player is not None:
                x1, x2, y1, y2 = player
                cv.rectangle(output_frame, (x1, y1), (x2, y2), (255, 0, 0), 2)

            # draw the bounding rectangle of the found blobs
            for x1, x2, y1, y2 in entities:
                cv.rectangle(output_frame, (x1, y1), (x2, y2), (0, 255, 0), 2)

            # show the the processed frame and the frame with output
            cv.imshow("processed_frame", frame)
            cv.imshow("output_frame", output_frame)
            cv.waitKey(1)

        # return player and entities discovered
        return player, entities

    def _do_something(self,
                      game: DinoGame,
                      obstacles: List[Tuple[float, float, float, float]],
                      player: Tuple[float, float, float, float] = None
                      ) -> None:
        # some variables to know how we need in order to not die
        need_jump = False
        need_crouch = False

        # do something only if the player is identified
        if player is not None:
            _, p_x, _, _ = player

            for x, _, _, _ in obstacles:
                # if obstacle is close -> jump
                if x - p_x < 30:
                    need_jump = True

            # do the action with priorities
            if need_jump:
                game.jump()
            elif need_crouch:
                game.crouch()
            else:
                game.stand_up()
