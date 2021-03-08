# -*- coding: utf-8 -*-
import random


class GameState:
    """
    Class to hold game state for each eval/game
    """

    def __init__(self):
        """
        Set up the game state given initialization parameters as listed.
        """

        # Did the Defender win?
        self.defender_won = False



    def G(self, pos, defender_id = -1):
        """
        """
        return random.randint(0, 100)


    def P(self, pos):
        """
        """
        return random.randint(0, 100)


    def W(self, pos):
        """
        """
        return random.randint(0, 100)


    def F(self, pos):
        """
        """
        return random.randint(0, 100)


    def M(self, pos, attacker_id = -1):
        """
        """
        return random.randint(0, 100)


    def play_turn(self, world_data, attacker_controllers, defender_controllers):
        """
        Play a turn of a game given world_data to log world updates
        and controllers for Attacker and Defenders.
        """
        game_over = False

        # Decide next moves
        for attacker_controller in attacker_controllers:
            attacker_controller.decide_move(self)
        for defender_controller in defender_controllers:
            defender_controller.decide_move(self)

        # Execute next moves
        for attacker_controller in attacker_controllers:
            attacker_controller.execute_move(self)
        for defender_controller in defender_controllers:
            defender_controller.execute_move(self)

        # Decrement time (yeah this is obvious but adding comment here is consistent)
        self.time -= 1

        # Out of time? Game over.
        if (self.time == 0):
            game_over = True

        return game_over

