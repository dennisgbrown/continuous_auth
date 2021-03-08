# -*- coding: utf-8 -*-
import random
import sys

sys.path.append('code')


class AttackerController():
    """
    Attacker-Man controller
    """
    def __init__(self, attacker_id, tree):
        """
        Initialization requires the expression tree asociated with this controller.
        """
        self.attacker_id = attacker_id
        self.tree = tree
        self.next_move = None


    def decide_move(self, game_state):
        """
        To device next move... TBD
        """
        # Set the next move
        self.next_move = random.randint(0, 1)


    def execute_move(self, game_state):
        """
        Actually execute the stored move
        """
        if (self.next_move == 0):
            pass


class DefenderController():
    """
    Defender controller
    """
    def __init__(self, defender_id, tree):
        """
        Use instances of the same class for each defender -- need to know
        which defender this class instance is for.
        """
        self.defender_id = defender_id
        self.tree = tree
        self.next_move = None


    def decide_move(self, game_state):
        """
        To device next move... TBD
        """
        # Set the next move
        self.next_move = random.randint(0, 1)


    def execute_move(self, game_state):
        """
        Actually execute the stored move
        """
        if (self.next_move == 0):
            pass
