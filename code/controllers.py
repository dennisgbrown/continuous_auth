# -*- coding: utf-8 -*-


def fill_precalcs(function_names, game_state):
    """
    Precalculate the game state values before evaluating the tree
    so we don't recalculate "static" values repeatedly (static within
    the scope of a single tree evalution)
    """
    precalcs = {}
    for function_name in function_names:
        if (function_name != 'constant'):
            precalcs[function_name] = getattr(game_state, function_name)()
    return precalcs


class AttackerController():
    """
    Attacker controller
    """
    # Canonical list of functions for Attacker supported by the Expression Tree class
    functions = ['T', 'S', 'W', 'constant']

    # Canonical list of terminals for Attacker supported by the Expression Tree class
    terminals = ['attack', 'listen', 'wait']


    def __init__(self, attacker_id, tree):
        """
        Initialization requires the expression tree asociated with this controller.
        """
        self.attacker_id = attacker_id
        self.tree = tree
        self.next_move = None


    def decide_move(self, game_state):
        """
        To decide next move, just evaluate the tree, which should spit out
        the action with the expected best payoff
        """
        print('------------------\n' + str(self.tree.root))
        # Set the next move
        self.next_move = self.tree.root.calc(fill_precalcs(self.functions, game_state))


class DefenderController():
    """
    Defender controller
    """
    # Canonical list of functions for Defender supported by the Expression Tree class
    functions = ['T', 'S', 'constant']

    # Canonical list of terminals for Defender supported by the Expression Tree class
    terminals = ['block', 'unblock']


    def __init__(self, defender_id, tree):
        """
        Initialization requires the expression tree asociated with this controller.
        """
        self.defender_id = defender_id
        self.tree = tree
        self.next_move = None


    def decide_move(self, game_state):
        """
        To decide next move, just evaluate the tree, which should spit out
        the action with the expected best payoff
        """
        # Set the next move
        self.next_move = self.tree.root.calc(fill_precalcs(self.functions, game_state))
