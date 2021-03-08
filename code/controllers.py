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

        # print(self.tree.root)

        # Set the next move
        treeval = self.tree.root.calc([game_state.G(),
                                       game_state.P(),
                                       game_state.W(),
                                       game_state.F(),
                                       game_state.M()])
        if (treeval >= 0):
            self.next_move = 'wait'
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
        treeval = self.tree.root.calc([game_state.G(),
                                       game_state.P(),
                                       game_state.W(),
                                       game_state.F(),
                                       game_state.M()])
        if (treeval >= 0):
            self.next_move = 'block'
        else:
            self.next_move = 'unblock'
