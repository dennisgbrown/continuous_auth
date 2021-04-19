# -*- coding: utf-8 -*-

class Controller():
    """
    Base class for controllers.
    """

    def __init__(self, id, tree):
        """
        Initialization requires the expression tree asociated with this controller.
        """
        self.id = id
        self.tree = tree
        self.next_move = None


    @staticmethod
    def fill_precalcs(functions, game_state):
        """
        Precalculate the game state values before evaluating the tree
        so we don't recalculate "static" values repeatedly (static within
        the scope of a single tree evalution)
        """
        precalcs = {}
        for function in functions:
            if (function[0] != 'constant'):
                precalcs[function[0]] = getattr(game_state, function[0])()
        return precalcs


    def decide_move(self, game_state):
        pass


class AttackerController(Controller):
    """
    Attacker controller
    """
    # Canonical list of functions for Attacker supported by the Expression Tree class
    functions = [['B', 'boolean'],
                 ['T', 'real', [['AO', 'constant'], [0, 1000]]],
                 ['AO', 'real', [['T', 'AR', 'constant'], [0, 1000]]],
                 ['AR', 'real', [['T', 'AO', 'constant'], [0, 1000]]]]

    # Canonical list of terminals for Attacker supported by the Expression Tree class
    terminals = [['attack', 'terminal'],
                 ['listen', 'terminal'],
                 ['wait', 'terminal']]


    def decide_move(self, game_state):
        """
        To decide next move, just evaluate the tree, which should spit out
        the action with the expected best payoff
        """
        # print('------------------\n' + str(self.tree.root))
        # Set the next move
        self.next_move = self.tree.root.calc(Controller.fill_precalcs(self.functions,
                                                                      game_state))


class DefenderController(Controller):
    """
    Defender controller
    """
    # Canonical list of functions for Defender supported by the Expression Tree class
    functions = [['BM', 'boolean'],
                 ['BH', 'real', [['constant'], [-100,300]]],
                 ['T', 'real', [['constant'], [0, 1000]]]]

    # Canonical list of terminals for Defender supported by the Expression Tree class
    terminals = [['block', 'terminal'],
                 ['unblock', 'terminal']]


    def decide_move(self, game_state):
        """
        To decide next move, just evaluate the tree, which should spit out
        the action with the expected best payoff
        """
        # Set the next move
        self.next_move = self.tree.root.calc(Controller.fill_precalcs(self.functions,
                                                                      game_state))


