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
        To device next move, calculate the value of each possible move
        and pick the highest.
        """
        # Get all possible moves
        valid_pos = game_state.get_valid_positions(game_state.attackers_pos[self.attacker_id], 'attacker')
        # Get the value of the expression tree for each possible move.
        # Feed the calculator the values of G, P, W, F, M instead of
        # recalculating those values each time we hit them in the tree.
        valid_pos_vals = [ self.tree.root.calc([game_state.G(pos),
                                                game_state.P(pos),
                                                game_state.W(pos),
                                                game_state.F(pos),
                                                game_state.M(pos, attacker_id = self.attacker_id)]) \
                          for pos in valid_pos ]
        # Find the index of the highest-valued move
        new_pos_idx = valid_pos_vals.index(max(valid_pos_vals))
        # Set the next move
        self.next_move = valid_pos[new_pos_idx]


    def execute_move(self, game_state):
        """
        Actually execute the stored move
        """
        game_state.attackers_pos[self.attacker_id] = self.next_move


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
        Decide next move for a defender: Randomly pick a valid move.
        """
        # Get all possible moves
        valid_pos = game_state.get_valid_positions(game_state.defenders_pos[self.defender_id],
                                                   'defender')
        # Get the value of the expression tree for each possible move.
        # Feed the calculator the values of G, P, W, F, M instead of
        # recalculating those values each time we hit them in the tree.
        valid_pos_vals = [ self.tree.root.calc([game_state.G(pos, defender_id = self.defender_id),
                                                game_state.P(pos),
                                                game_state.W(pos),
                                                game_state.F(pos),
                                                game_state.M(pos)]) \
                          for pos in valid_pos ]
        # Find the index of the highest-valued move
        new_pos_idx = valid_pos_vals.index(max(valid_pos_vals))
        # Set the next move
        self.next_move = valid_pos[new_pos_idx]


    def execute_move(self, game_state):
        """
        Actually execute the stored move
        """
        # Set new location based on which defender this is
        game_state.defenders_pos[self.defender_id] = self.next_move


class RandomDefenderController():
    """
    Random Defender controller (as used by assignments 2a and 2b)
    """
    def __init__(self, defender_id):
        """
        Use instances of the same class for each defender -- need to know
        which defender this class instance is for.
        """
        self.defender_id = defender_id
        self.next_move = None


    def decide_move(self, game_state):
        """
        Decide next move for a defender: Randomly pick a valid move.
        """
        # Get starting position based on which defender this is
        pos = game_state.defenders_pos[self.defender_id]

        # Get a list of valid new positions and pick one randomly
        valid_pos = game_state.get_valid_positions(pos, 'defender')
        new_pos_idx = random.randint(0, len(valid_pos) - 1)
        self.next_move = valid_pos[new_pos_idx]


    def execute_move(self, game_state):
        """
        Actually execute the stored move
        """
        # Set new location based on which defender this is
        game_state.defenders_pos[self.defender_id] = self.next_move

