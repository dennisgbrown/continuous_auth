# -*- coding: utf-8 -*-
import random


class GameState:
    """
    Class to hold game state for each eval/game.
    """

    def __init__(self):
        """
        Set up the game state given initialization parameters as listed.
        """
        
        self.time = 100  
        
        self.attacker_score = 0
        self.defender_score = 0

        # Did the Defender win?
        self.defender_won = False


    def G(self):
        """
        Random stand-in for something we can measure in the simulation
        """
        return random.randint(-100, 100)


    def P(self):
        """
        Random stand-in for something we can measure in the simulation
        """
        return random.randint(-100, 100)


    def W(self):
        """
        Random stand-in for something we can measure in the simulation
        """
        return random.randint(-100, 100)


    def F(self):
        """
        Random stand-in for something we can measure in the simulation
        """
        return random.randint(-100, 100)


    def M(self):
        """
        Random stand-in for something we can measure in the simulation
        """
        return random.randint(-100, 100)


    def play_turn(self, world_data, attacker_controllers, defender_controllers):
        """
        Play a turn of a game given world_data to log world updates
        and controllers for Attacker and Defenders.
        """
        game_over = False
    
        # Assume there is a single attacker and single defender,
        # even though the EA supports sets of attackers and defenders.
        attacker = attacker_controllers[0]
        defender = defender_controllers[0]

        # Decide next moves
        attacker.decide_move(self)
        defender.decide_move(self)

        world_data.append('attacker: ' + attacker.next_move + ' vs. defender: ' 
                          + defender.next_move + '\n')

        # Execute next moves
        if ((attacker.next_move == 'attack') and (defender.next_move == 'unblock')):
            self.attacker_score += 1
        if ((attacker.next_move == 'attack') and (defender.next_move == 'block')):
            self.defender_score += 1
        
        # Decrement time (yeah this is obvious but adding comment here is consistent)
        self.time -= 1

        # Out of time? Game over.
        if (self.time == 0):
            game_over = True

        return game_over

