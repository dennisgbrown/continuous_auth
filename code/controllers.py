# -*- coding: utf-8 -*-


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

        COMMENTARY: 
        During each turn in the game in which the user generates traffic, the defender is basically
        trying to learn confidence intervals on the mean and variance of the traffic generator
        (intervals that should shrink over time as more traffic is generated). If behavior deviates
        from normal suddenly, and continues deviating over a sequence of turns, that should be more
        alarming than if one round of behavior comes in outside of normal. Incorporating recent
        behavior into the decision made by the defender would give the system "outlier" resistence,
        and is something lacking from the Saritas model. I'm not sure how that would translate into
        CCEGP, we'd be sort of evolving confidence bounds over each turn.

        Also, regarding the output of the defender. I'm not sure how best to accomplish it, but if
        we were to change the output from block/unblock into a number from 0 to 1 (basically by
        feeding the evolved treeval output into a logistic function I guess) we could treat such a
        value as the defender's confidence in whether or not the user is authentic.

        Not sure how that fits into CCEGP and how fitness is derived, but having output like that
        rather than binary output might make fitness more meaningful (if the defender is almost
        certain that the user is authentic rather than on-the-fence when the user actually is
        authentic, that should be rewarded with more fitness)

        Further, we could also evolve alongside the cutoff point of the confidence interval at which
        the defender blocks, with fitness for that based on how often the real user is prevented
        from accessing the resource.
        """
        # Set the next move
        #treeval = self.tree.root.calc([game_state.T(),
        #                               game_state.S(),
        #                               game_state.W()])
        #if (treeval >= 0):

        # First check if the game is currently blocked, then there's nothing for the defender to do.
        # This could probably be moved into the game state logic and the defender's turn here skipped.
        if (game_state.state == game_state.BLOCKED):
            self.next_move = 'block'
            return
        # Adding a static check (if behavior > false positive cut-off) for now
        if (game_state.behavior_mask[-1] and game_state.behavior_history[-1] > game_state.c_r):
            self.next_move = 'block'
        else:
            self.next_move = 'unblock'
