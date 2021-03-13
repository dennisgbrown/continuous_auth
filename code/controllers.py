# -*- coding: utf-8 -*-
import sys

sys.path.append('code')


class AttackerController():
    """
    Attacker controller
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

        # print('------------------\n', self.tree.root)

        # Set the next move
        treeval = self.tree.root.calc([game_state.T(),
                                       game_state.S(),
                                       game_state.W()])
        if (treeval <= -0.33):
            self.next_move = 'wait'
        elif (treeval <= 0.33):
            self.next_move = 'listen'
        else:
            self.next_move = 'attack'


class DefenderController():
    """
    Defender controller
    """
    def __init__(self, defender_id, tree):
        """
        Initialization requires the expression tree asociated with this controller.
        """
        self.defender_id = defender_id
        self.tree = tree
        self.next_move = None


    def decide_move(self, game_state):
        """
        To device next move... TBD
        """
        # Set the next move
        treeval = self.tree.root.calc([game_state.T(),
                                       game_state.S(),
                                       game_state.W()])
        if (treeval >= 0):
            self.next_move = 'block'
        else:
            self.next_move = 'unblock'
