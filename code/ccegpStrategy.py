# -*- coding: utf-8 -*-
import random
import copy
import traceback
import numpy
import sys

from strategy import Strategy
from gameState import GameState
from controllers import AttackerController, DefenderController
from exprTree import Node, ExprTree
from population import Population
from ciaoPlotter import CIAOPlotter


class CCEGPStrategy(Strategy):
    """
    Competitive Co-Evolutionary Genetic Programming search strategy.
    """
    def __init__(self, experiment):
        self.experiment = experiment

        # Information for setting up and controlling the Attacker population
        self.attacker_controllers = [None for _ in range(experiment.num_attackers)]
        self.attacker_mu = 10
        self.attacker_lambda = 5
        self.attacker_dmax_init = 5
        self.attacker_dmax_overall = 5
        self.attacker_parent_selection = 'fitness_proportional_selection'
        self.attacker_overselection_top = 0.32
        self.attacker_p_m = 0.05
        self.attacker_survival_selection = 'truncation'
        self.attacker_tournament_size_for_survival_selection = 4
        self.attacker_parsimony_technique = 'size'
        self.attacker_pppc = 0.05  # parsimony pressure penalty coefficient

        # Information for setting up and controlling the Defender population
        self.defender_controllers = [None for _ in range(experiment.num_defenders)]
        self.defender_mu = 10
        self.defender_lambda = 5
        self.defender_dmax_init = 5
        self.defender_dmax_overall = 5
        self.defender_parent_selection = 'fitness_proportional_selection'
        self.defender_overselection_top = 0.32
        self.defender_p_m = 0.05
        self.defender_survival_selection = 'truncation'
        self.defender_tournament_size_for_survival_selection = 4
        self.defender_parsimony_technique = 'size'
        self.defender_pppc = 0.05  # parsimony pressure penalty coefficient

        # Logging and termination information
        self.ciao_file_path_root = 'data/defaultCIAOData'
        self.parsimony_log_file_path = 'data/defaultParsimonyLog.txt'
        self.parsimony_log = None
        self.termination = 'number_of_evals'
        self.n_for_convergence = 10

        # Parse config properties
        try:
            self.attacker_mu = experiment.config_parser.getint('ccegp_options', 'attacker_mu')
            print('config: attacker_mu =', self.attacker_mu)
        except:
            print('config: attacker_mu not specified; using', self.attacker_mu)

        try:
            self.attacker_lambda = experiment.config_parser.getint('ccegp_options', 'attacker_lambda')
            print('config: attacker_lambda =', self.attacker_lambda)
        except:
            print('config: attacker_lambda not specified; using', self.attacker_lambda)

        try:
            self.attacker_dmax_init = experiment.config_parser.getint('ccegp_options', 'attacker_dmax_init')
            print('config: attacker_dmax_init =', self.attacker_dmax_init)
        except:
            print('config: attacker_dmax_init not specified; using', self.attacker_dmax_init)

        try:
            self.attacker_dmax_overall = experiment.config_parser.getint('ccegp_options', 'attacker_dmax_overall')
            print('config: attacker_dmax_overall =', self.attacker_dmax_overall)
        except:
            print('config: attacker_dmax_overall not specified; using', self.attacker_dmax_overall)

        try:
            self.attacker_parent_selection = experiment.config_parser.get('ccegp_options',
                                                                     'attacker_parent_selection').lower()
            print('config: attacker_parent_selection =', self.attacker_parent_selection)
        except:
            print('config: attacker_parent_selection not specified; using', self.attacker_parent_selection)

        if (self.attacker_parent_selection == 'overselection'):
            try:
                self.attacker_overselection_top = experiment.config_parser.getfloat('ccegp_options',
                                                                               'attacker_overselection_top')
                print('config: attacker_overselection_top =',
                      self.attacker_overselection_top)
            except:
                print('config: attacker_overselection_top not specified; using',
                      self.attacker_overselection_top)

        try:
            self.attacker_p_m = experiment.config_parser.getfloat('ccegp_options', 'attacker_p_m')
            print('config: attacker_p_m =', self.attacker_p_m)
        except:
            print('config: attacker_p_m not specified; using', self.attacker_p_m)

        try:
            self.attacker_survival_selection = experiment.config_parser.get('ccegp_options',
                                                                       'attacker_survival_selection').lower()
            print('config: attacker_survival_selection =', self.attacker_survival_selection)
        except:
            print('config: attacker_survival_selection not specified; using', self.attacker_survival_selection)

        if (self.attacker_survival_selection == 'k_tournament_without_replacement'):
            try:
                self.attacker_tournament_size_for_survival_selection = experiment.config_parser.getint(
                    'ccegp_options', 'attacker_tournament_size_for_survival_selection')
                print('config: attacker_tournament_size_for_survival_selection =',
                      self.attacker_tournament_size_for_survival_selection)
            except:
                print('config: attacker_tournament_size_for_survival_selection not specified; using',
                      self.attacker_tournament_size_for_survival_selection)

        try:
            self.attacker_parsimony_technique = experiment.config_parser.get('ccegp_options',
                                                                        'attacker_parsimony_technique').lower()
            print('config: attacker_parsimony_technique =', self.attacker_parsimony_technique)
        except:
            print('config: attacker_parsimony_technique not specified; using', self.attacker_parsimony_technique)

        try:
            self.attacker_pppc = experiment.config_parser.getfloat('ccegp_options', 'attacker_pppc')
            print('config: attacker_pppc =', self.attacker_pppc)
        except:
            print('config: attacker_pppc not specified; using', self.attacker_pppc)

        try:
            self.defender_mu = experiment.config_parser.getint('ccegp_options', 'defender_mu')
            print('config: defender_mu =', self.defender_mu)
        except:
            print('config: defender_mu not specified; using', self.defender_mu)

        try:
            self.defender_lambda = experiment.config_parser.getint('ccegp_options', 'defender_lambda')
            print('config: defender_lambda =', self.defender_lambda)
        except:
            print('config: defender_lambda not specified; using', self.defender_lambda)

        try:
            self.defender_dmax_init = experiment.config_parser.getint('ccegp_options', 'defender_dmax_init')
            print('config: defender_dmax_init =', self.defender_dmax_init)
        except:
            print('config: defender_dmax_init not specified; using', self.defender_dmax_init)

        try:
            self.defender_dmax_overall = experiment.config_parser.getint('ccegp_options', 'defender_dmax_overall')
            print('config: defender_dmax_overall =', self.defender_dmax_overall)
        except:
            print('config: defender_dmax_overall not specified; using', self.defender_dmax_overall)

        try:
            self.defender_parent_selection = experiment.config_parser.get('ccegp_options',
                                                                       'defender_parent_selection').lower()
            print('config: defender_parent_selection =', self.defender_parent_selection)
        except:
            print('config: defender_parent_selection not specified; using', self.defender_parent_selection)

        if (self.defender_parent_selection == 'overselection'):
            try:
                self.defender_overselection_top = experiment.config_parser.getfloat('ccegp_options',
                                                                               'defender_overselection_top')
                print('config: defender_overselection_top =',
                      self.defender_overselection_top)
            except:
                print('config: defender_overselection_top not specified; using',
                      self.defender_overselection_top)

        try:
            self.defender_p_m = experiment.config_parser.getfloat('ccegp_options', 'defender_p_m')
            print('config: defender_p_m =', self.defender_p_m)
        except:
            print('config: defender_p_m not specified; using', self.defender_p_m)

        try:
            self.defender_survival_selection = experiment.config_parser.get('ccegp_options',
                                                                       'defender_survival_selection').lower()
            print('config: defender_survival_selection =', self.defender_survival_selection)
        except:
            print('config: defender_survival_selection not specified; using', self.defender_survival_selection)

        if (self.defender_survival_selection == 'k_tournament_without_replacement'):
            try:
                self.defender_tournament_size_for_survival_selection = experiment.config_parser.getint(
                    'ccegp_options', 'defender_tournament_size_for_survival_selection')
                print('config: defender_tournament_size_for_survival_selection =',
                      self.defender_tournament_size_for_survival_selection)
            except:
                print('config: defender_tournament_size_for_survival_selection not specified; using',
                      self.defender_tournament_size_for_survival_selection)

        try:
            self.defender_parsimony_technique = experiment.config_parser.get('ccegp_options',
                                                                          'defender_parsimony_technique').lower()
            print('config: defender_parsimony_technique =', self.defender_parsimony_technique)
        except:
            print('config: defender_parsimony_technique not specified; using', self.defender_parsimony_technique)

        try:
            self.defender_pppc = experiment.config_parser.getfloat('ccegp_options', 'defender_pppc')
            print('config: defender_pppc =', self.defender_pppc)
        except:
            print('config: defender_pppc not specified; using', self.defender_pppc)

        try:
            self.termination = experiment.config_parser.get('ccegp_options',
                                                            'termination').lower()
            print('config: termination =', self.termination)
        except:
            print('config: termination not specified; using', self.termination)

        if (self.termination == 'convergence'):
            try:
                self.n_for_convergence = experiment.config_parser.getint('ccegp_options',
                                                                         'n_for_convergence')
                print('config: n_for_convergence =', self.n_for_convergence)
            except:
                print('config: n_for_convergence not specified; using', self.n_for_convergence)

        try:
            self.ciao_file_path_root = experiment.config_parser.get('ccegp_options',
                                                                         'ciao_file_path_root')
            print('config: ciao_file_path_root =', self.ciao_file_path_root)
        except:
            print('config: ciao_file_path_root not properly specified; using', self.ciao_file_path_root)

        try:
            self.parsimony_log_file_path = experiment.config_parser.get('ccegp_options',
                                                                        'parsimony_log_file_path')
            print('config: parsimony_log_file_path =', self.parsimony_log_file_path)
        except:
            print('config: parsimony_log_file_path not properly specified; using', self.parsimony_log_file_path)

        # Set up populations
        self.attacker_pop = Population('Attacker', self.attacker_mu, self.attacker_lambda,
                                  self.attacker_dmax_init, self.attacker_dmax_overall,
                                  self.attacker_parent_selection, self.attacker_overselection_top,
                                  self.attacker_p_m, self.attacker_survival_selection,
                                  self.attacker_tournament_size_for_survival_selection,
                                  self.attacker_parsimony_technique, self.attacker_pppc,
                                  AttackerController.functions, AttackerController.terminals)
        self.defender_pop = Population('Defender', self.defender_mu, self.defender_lambda,
                                    self.defender_dmax_init, self.defender_dmax_overall,
                                    self.defender_parent_selection, self.defender_overselection_top,
                                    self.defender_p_m, self.defender_survival_selection,
                                    self.defender_tournament_size_for_survival_selection,
                                    self.defender_parsimony_technique, self.defender_pppc,
                                    DefenderController.functions, DefenderController.terminals)

        # Write configuration items to log file
        experiment.log_file.write('attacker_mu: ' + str(self.attacker_mu) + '\n')
        experiment.log_file.write('attacker_lambda: ' + str(self.attacker_lambda) + '\n')
        experiment.log_file.write('attacker_dmax_init: ' + str(self.attacker_dmax_init) + '\n')
        experiment.log_file.write('attacker_dmax_overall: ' + str(self.attacker_dmax_overall) + '\n')
        experiment.log_file.write('attacker_parent selection method: ' + self.attacker_parent_selection + '\n')
        if (self.attacker_parent_selection == 'overselection'):
            experiment.log_file.write('attacker_overselection top for parent selection: '
                                      + str(self.attacker_overselection_top) + '\n')
        experiment.log_file.write('attacker_probability of mutation p_m: ' + str(self.attacker_p_m) + '\n')
        experiment.log_file.write('attacker_survival selection method: ' + self.attacker_survival_selection + '\n')
        if (self.attacker_survival_selection == 'k_tournament_without_replacement'):
            experiment.log_file.write('attacker_tournament size for survival selection: '
                                      + str(self.attacker_tournament_size_for_survival_selection) + '\n')
        experiment.log_file.write('attacker_parsimony technique: ' + self.attacker_parsimony_technique + '\n')
        experiment.log_file.write('attacker_parsimony pressure penalty coefficient: ' + str(self.attacker_pppc) + '\n')
        experiment.log_file.write('defender_mu: ' + str(self.defender_mu) + '\n')
        experiment.log_file.write('defender_lambda: ' + str(self.defender_lambda) + '\n')
        experiment.log_file.write('defender_dmax_init: ' + str(self.defender_dmax_init) + '\n')
        experiment.log_file.write('defender_dmax_overall: ' + str(self.defender_dmax_overall) + '\n')
        experiment.log_file.write('defender_parent selection method: ' + self.defender_parent_selection + '\n')
        if (self.defender_parent_selection == 'overselection'):
            experiment.log_file.write('defender_overselection top for parent selection: '
                                      + str(self.defender_overselection_top) + '\n')
        experiment.log_file.write('defender_probability of mutation p_m: ' + str(self.defender_p_m) + '\n')
        experiment.log_file.write('defender_survival selection method: ' + self.defender_survival_selection + '\n')
        if (self.defender_survival_selection == 'k_tournament_without_replacement'):
            experiment.log_file.write('defender_tournament size for survival selection: '
                                      + str(self.defender_tournament_size_for_survival_selection) + '\n')
        experiment.log_file.write('defender_parsimony technique: ' + self.defender_parsimony_technique + '\n')
        experiment.log_file.write('defender_parsimony pressure penalty coefficient: ' + str(self.defender_pppc) + '\n')
        experiment.log_file.write('termination method: ' + self.termination + '\n')
        if (self.termination == 'convergence'):
            experiment.log_file.write('n evals for convergence: '
                                      + str(self.n_for_convergence) + '\n')
        experiment.log_file.write('CIAO data file path root: ' + self.ciao_file_path_root + '\n')
        experiment.log_file.write('parsimony log file path: ' + self.parsimony_log_file_path + '\n')

        # Open parsimony log
        try:
            self.parsimony_log = open(self.parsimony_log_file_path, 'w')
        except:
            print('config: problem with parsimony log file', self.parsimony_log_file_path)
            traceback.print_exc()
            return None


    def initialize_population(self, pop):
        """
        Given an empty population, generate and return an initial population
        of expression trees using Ramped Half-and-Half
        """
        pop.individuals = [None for _ in range(pop.ea_mu)]

        for i in range(pop.ea_mu):
            root = Node()
            pop.individuals[i] = ExprTree(root)

            # Full method
            if (random.random() < 0.5):
                pop.individuals[i].build_tree(pop, root, 0, pop.dmax_init, 'full')

            # Grow method
            else:
                pop.individuals[i].build_tree(pop, root, 0, pop.dmax_init, 'grow')
                
            pop.individuals[i].clean_tree()
            pop.individuals[i].root.reset_metrics()


    def random_selection_without_replacement(self, pop, num_to_select):
        """
        Given a population, return a selection made up of num_to_select randomly-
        selected individuals from the given population
        """
        if (len(pop.individuals) < num_to_select):
            print('Stuck in random selection without replacement because',
                  len(pop.individuals), 'insufficient to choose', num_to_select)

        random.shuffle(pop.individuals)
        selection = pop.individuals[0:num_to_select]
        return selection


    def fitness_proportional_selection(self, pop, num_to_select):
        """
        Given a population, return a selection using Fitness Proportional Selection
        """
        selection = []
        probabilities = []

        # Find total fitness of population. Account for negative fitnesses
        # with an offset.
        min_fitness = pop.individuals[0].fitness
        for individual in pop.individuals:
            if (individual.fitness < min_fitness):
                min_fitness = individual.fitness
        offset = 0
        if (min_fitness < 0):
            offset = abs(min_fitness)
        total_fitness = 0
        for individual in pop.individuals:
            total_fitness += (individual.fitness + offset)

        # If total fitness is nonzero, good to go.
        if (total_fitness != 0):
            # Calculate probability distribution
            accumulation = 0.0
            for individual in pop.individuals:
                accumulation += ((individual.fitness + offset) / total_fitness)
                probabilities.append(accumulation)

            # Build new population using roulette wheel algorithm
            while (len(selection) < num_to_select):
                randval = random.random()
                curr_member = 0
                while (probabilities[curr_member] < randval):
                    curr_member += 1
                if (curr_member > (len(pop.individuals) - 1)):
                    curr_member = len(pop.individuals) - 1
                selection.append(pop.individuals[curr_member])

        # Edge case: If total_fitness == 0, then just pick from population
        # with uniform probability, because the roulette wheel can't
        # handle having an infinite number of 0-width wedges.
        else:
            selection = self.random_selection_without_replacement(pop, num_to_select)

        return selection


    def overselection(self, pop, num_to_select):
        """
        Given a population, select 80% from the top x% of the population
        ranked by fitness, and 20% from the rest of the population,
        where x% is specified in the configuration file.
        """
        # Sort the population by decreasing fitness
        pop.individuals = sorted(pop.individuals, key = lambda item: item.fitness,
                                 reverse = True)

        # Find the split point and identify top and bottom populations
        split = int(len(pop.individuals) * pop.overselection_top)
        top = pop.individuals[0:split]
        bottom = pop.individuals[split:len(pop.individuals) - 1]

        # Randomly build the new population with 80% chance of choosing
        # from top and 20% chance of choosing from bottom
        selection = []
        while (len(selection) < num_to_select):
            if (random.random() < 0.8):
                if (len(top) > 0):
                    selection.append(top[random.randint(0, len(top) - 1)])
            else:
                if (len(bottom) > 0):
                    selection.append(bottom[random.randint(0, len(bottom) - 1)])

        return selection


    def k_tournament_selection_without_replacement(self, pop, num_to_select):
        """
        Given a population, return a selection using k-tournament Selection
        without replacement.

        Updated to be less dumb by keeping a list of eligible tournament members
        instead of allowing choosing ineligible members.
        """
        if (len(pop.individuals) < num_to_select):
            print('Stuck in k-tournament selection without replacement because',
                  len(pop.individuals), 'insufficient to choose', num_to_select)

        selection = []
        selected_indices = set()

        while (len(selection) < num_to_select):
            # Identify those eligible to be contestants (not already selected)
            k_eligible = {x for x in range(len(pop.individuals))}
            k_eligible = k_eligible - selected_indices

            # If we can't fill a tournament with unselected individuals,
            # reduce tournament size to what's left
            tournament_size = pop.tournament_size_for_survival_selection
            if ((len(pop.individuals) - len(selection)) < tournament_size):
                tournament_size = len(pop.individuals) - len(selection)

            # Pick tournament contestants from those eligible to be contestants
            k_contestants = []
            while (len(k_contestants) < tournament_size):
                contestant_index = list(k_eligible)[random.randint(0, len(k_eligible) - 1)]
                k_eligible.remove(contestant_index)
                k_contestants.append(contestant_index)

            # Choose the best-rated contestant
            k_contestants = sorted(k_contestants,
                                   key=lambda item: pop.individuals[item].fitness,
                                   reverse = True)
            best_index = k_contestants[0]
            selected_indices.add(best_index)
            selection.append(pop.individuals[best_index])

        return selection


    def truncation_selection(self, pop, num_to_select):
        """
        Truncation selection. Given a population, sort the population and
        select the top individuals.
        """
        sorted_population = sorted(pop.individuals, key=lambda item: item.fitness, reverse = True)
        selection = []
        for curr_individual in range(pop.ea_mu):
            selection.append(sorted_population[curr_individual])
        return selection


    def select_parents(self, pop):
        """
        Given a population, return a mating pool using the configured method.
        """
        if (pop.parent_selection == "fitness_proportional_selection"):
            return self.fitness_proportional_selection(pop, pop.ea_lambda)
        elif (pop.parent_selection == "overselection"):
            return self.overselection(pop, pop.ea_lambda)
        else:
            print("Unknown parent selection method:", pop.parent_selection)
            sys.exit(1)


    def mutate(self, pop, parent):
        """
        Given a population and a parent, return a mutated offspring
        """
        # Start with a copy of the parent
        offspring = copy.deepcopy(parent)

        # Randomly pick a node in the expression tree
        selected_node = offspring.root.find_nth_node(random.randint(1, offspring.root.size))

        # Build a new (sub)tree there. Arbitrarily choose 'grow' method and limit depth to dmax_overall.
        offspring.build_tree(pop, selected_node, selected_node.depth, pop.dmax_overall, 'grow')

        # clean the tree to remove non-branches
        offspring.clean_tree()
        # Reset the tree metrics we just screwed up
        offspring.root.reset_metrics()

        return offspring


    def recombine(self, pop, parent1, parent2):
        """
        Given a population and two parents, return two recombined offspring.
        """
        # Start with copies of the parents
        offspring1 = copy.deepcopy(parent1)
        offspring2 = copy.deepcopy(parent2)

        # Randomly pick nodes from each tree and swap them.
        match_found = False
        while (not(match_found)):
            # Pick a node in each tree
            selected_node1 = offspring1.root.find_nth_node(random.randint(1, offspring1.root.size))
            selected_node2 = offspring2.root.find_nth_node(random.randint(1, offspring2.root.size))

            # If the swap would cause either offspring to exceed Dmax,
            # try again.
            if (((selected_node1.depth + selected_node2.height) > pop.dmax_overall)
                or ((selected_node2.depth + selected_node1.height) > pop.dmax_overall)):
                continue

            # Match found -- make swap
            temp_node = Node()
            temp_node.copy(selected_node1)
            selected_node1.copy(selected_node2)
            selected_node2.copy(temp_node)
            match_found = True

        offspring1.clean_tree()
        offspring2.clean_tree()
        # Reset the tree metrics we just screwed up
        offspring1.root.reset_metrics()
        offspring2.root.reset_metrics()

        return [offspring1, offspring2]


    def recombine_mutate(self, pop, parents):
        """
        Given a population and a set of parents, return a set of offspring
        of equal size created through stochastic choice of mutation or
        recombination.
        """
        offspring = []

        # Walk through parents list either mutating or pair-wise recombining
        # to create offspring
        parent_counter = 0
        while (len(offspring) < len(parents)):
            # Mutate if random value within probability of mutation
            # OR if we only have 1 parent left
            if ((random.random() < pop.p_m)
                or (parent_counter == (len(parents) - 1))):
                offspring.append(self.mutate(pop, parents[parent_counter]))
                parent_counter += 1
            # Otherwise, recombine
            else:
                offspring += self.recombine(pop, parents[parent_counter],
                                            parents[parent_counter + 1])
                parent_counter += 2

        return offspring


    def select_survivors(self, pop):
        """
        Given a population, return a selection of survivors using the
        configured method.
        """
        if (pop.survival_selection == 'truncation'):
            return self.truncation_selection(pop, pop.ea_mu)
        elif (pop.survival_selection == 'k_tournament_without_replacement'):
            return self.k_tournament_selection_without_replacement(pop,
                                                                   pop.ea_mu)
        else:
            print('Unknown parent selection method:', pop.survival_selection)
            exit(1)


    def execute_one_game(self, attacker_individual, defender_individual):
        """
        Execute one game / eval of a run given a Attacker individual and
        Defender individual selected from their respective populations.
        """
        # Pick a new scenario and set up a new game state.
        self.experiment.world_data = []
        game_state = GameState(self.experiment)

        # Create new Attacker and Defender controllers
        for curr_attacker_id in range(self.experiment.num_attackers):
            self.attacker_controllers[curr_attacker_id] = AttackerController(curr_attacker_id, attacker_individual)
        for curr_defender_id in range(self.experiment.num_defenders):
            self.defender_controllers[curr_defender_id] = DefenderController(curr_defender_id,
                                                                    defender_individual)

        # While the game isn't over, play game turns.
        game_over = False
        while (not game_over):
            game_over = game_state.play_turn(self.experiment.world_data,
                                             self.attacker_controllers,
                                             self.defender_controllers)

        # Set Attacker fitness and implement parsimony pressure
        attacker_individual.fitness = game_state.calculate_attacker_fitness()
        if (self.attacker_pop.parsimony_technique == 'size'):
            attacker_individual.fitness -= (self.attacker_pop.pppc * attacker_individual.root.size)
        else:
            attacker_individual.fitness -= (self.attacker_pop.pppc * attacker_individual.root.height)

        # Set Defender fitness and implement parsimony pressure
        defender_individual.fitness = game_state.calculate_defender_fitness()
        if (self.defender_pop.parsimony_technique == 'size'):
            defender_individual.fitness -= (self.defender_pop.pppc * defender_individual.root.size)
        else:
            defender_individual.fitness -= (self.defender_pop.pppc * defender_individual.root.height)

        # Set Attacker and Defender scores
        # Score is raw game score without parsimony pressure for Attacker
        attacker_individual.score = game_state.calculate_attacker_fitness()
        defender_individual.score = game_state.calculate_defender_fitness()

        # print('Game over: Attacker', game_state.attacker_score, '/ Defender', game_state.defender_score)


    def generation_evals(self, attackers, defenders, eval_count, evals_with_no_change, attacker_gen_high_fitness):
        """
        Run evaluations of the Attacker vs Defender populations given Attacker and Defender
        populations. Also takes current eval count, evals with no change, and
        attacker generation high fitness in order to do bookkeeping related to
        termination conditions. Returns updated eval count and evals with no change.

        Run games with Attacker vs Defender from the provided populations.
        Average fitnesses of multiple evaluations of the same individual.
        """

        # METHOD 1: Evaluate each attacker once.
        # USES O(N) EVALUATIONS

        # Set up matrices to hold per-game fitness values for Attacker and Defender
        attacker_fitnesses = [[] for _ in range(len(attackers))]
        defender_fitnesses = [[] for _ in range(len(defenders))]

        # Shuffle the attackers and defenders, then play each Attacker against one Defender
        random.shuffle(attackers)
        random.shuffle(defenders)
        num_games = max(len(attackers), len(defenders))
        for curr_game in range(num_games):
            # If num attackers < num defenders, some attackers will go multiple times
            attacker_index = curr_game % len(attackers)
            # If num defenders < num attackers, some defenders will go multiple times
            defender_index = curr_game % len(defenders)
            attacker_individual = attackers[attacker_index]
            defender_individual = defenders[defender_index]
            self.execute_one_game(attacker_individual, defender_individual)
            # Save the fitness in a list so we can average the results later
            attacker_fitnesses[attacker_index].append(attacker_individual.fitness)
            defender_fitnesses[defender_index].append(defender_individual.fitness)

            # Bookkeeping
            eval_count += 1
            if (attacker_individual.fitness <= attacker_gen_high_fitness):
                evals_with_no_change += 1
            else:
                evals_with_no_change = 0

            # # Provide status message every nth evaluation.
            # if ((eval_count % 10) == 0):
            #     print('\r', eval_count, 'evals', end =" ")

        # Set the fitness of each Attacker and Defender to the average of its list of fitnesses
        for attacker_index in range(len(attackers)):
            attackers[attacker_index].fitness = numpy.mean(attacker_fitnesses[attacker_index])
        for defender_index in range(len(defenders)):
            defenders[defender_index].fitness = numpy.mean(defender_fitnesses[defender_index])

        # # METHOD 2: Play every Attacker against every Defender and average fitnesses
        # # USES O(N^2) EVALUATIONS

        # # Set up matrices to hold per-game fitness values for Attacker and Defender
        # attacker_fitnesses = numpy.zeros((len(self.attacker_pop.individuals),
        #                               len(self.defender_pop.individuals)))
        # defender_fitnesses = numpy.zeros((len(self.defender_pop.individuals),
        #                                 len(self.attacker_pop.individuals)))
        # # Play every Attacker against every Defender and perform bookkeeping
        # for attacker_index in range(len(self.attacker_pop.individuals)):
        #     attacker_individual = self.attacker_pop.individuals[attacker_index]
        #     for defender_index in range(len(self.defender_pop.individuals)):
        #         defender_individual = self.defender_pop.individuals[defender_index]
        #         self.execute_one_game(attacker_individual, defender_individual)
        #         attacker_fitnesses[attacker_index][defender_index] = attacker_individual.fitness
        #         defender_fitnesses[defender_index][attacker_index] = defender_individual.fitness
        #         # Bookkeeping
        #         eval_count += 1
        #         if (attacker_individual.fitness <= attacker_gen_high_fitness):
        #             evals_with_no_change += 1
        #         else:
        #             evals_with_no_change = 0
        #         # Provide status message every nth evaluation.
        #         if ((eval_count % 10) == 0):
        #             print('\r', eval_count, 'evals', end =" ")
        # # Set the fitness of each Attacker to the mean of its fitnesses against every Defender
        # # and vice-versa for the Defenders.
        # for attacker_index in range(len(self.attacker_pop.individuals)):
        #     attacker_individual = self.attacker_pop.individuals[attacker_index]
        #     attacker_individual.fitness = numpy.mean(attacker_fitnesses[attacker_index])
        # for defender_index in range(len(self.defender_pop.individuals)):
        #     defender_individual = self.defender_pop.individuals[defender_index]
        #     defender_individual.fitness = numpy.mean(defender_fitnesses[defender_index])

        return eval_count, evals_with_no_change


    def ciao_plot(self):
        """
        Play the best Attacker and Defender of every generation against each other
        to create CIAO plot.

        Attacker = Attacker = Y axis (rows)
        Defender = Defender = X axis (columns)
        """
        num_gens = len(self.attacker_pop.best_individuals)

        fitnesses = numpy.zeros((num_gens, num_gens))
        eval_count = 0
        print('CIAO: play', num_gens, 'generations of bests')
        for defender in range(num_gens):
            for attacker in range(defender, num_gens):
                self.execute_one_game(self.attacker_pop.best_individuals[attacker],
                                      self.defender_pop.best_individuals[defender])
                eval_count += 1
                # 0,0 is lower left, so adjust the row index
                fitnesses[num_gens - attacker - 1][defender] = self.attacker_pop.best_individuals[attacker].fitness

                # # Provide status message every nth evaluation.
                # if ((eval_count % 10) == 0):
                #     print('\r', eval_count, 'evals', end = ' ')

        # Normalize fitnesses to [0.0 - 1.0] where 1.0 is best
        min_fitness = numpy.min(fitnesses)
        if (min_fitness < 0):
            fitnesses = fitnesses + numpy.abs(min_fitness)
        else:
            fitnesses = fitnesses - min_fitness
        max_fitness = numpy.max(fitnesses)
        if (max_fitness != 0):
            fitnesses = (fitnesses / max_fitness)

        # Reset the matrix below the anti-diagonal. We should just be able to
        # ignore these values but if we set them to 1.0 (max luminance)
        # it can make plotting them simpler since 1.0 will show up as white
        # and disappear into the background (assuming white background).
        for i in range(1, num_gens):
            for j in range(i, num_gens):
                fitnesses[num_gens - i][j] = 1.0

        # Write out CIAO data to file for separate tool to plot it
        numpy.savetxt('data/' + self.ciao_file_path_root + '_Run' \
                      + str(self.experiment.curr_run) + '_CIAO_Data.txt',
                      fitnesses)
        CIAOPlotter.plot(self.ciao_file_path_root + '_Run' + str(self.experiment.curr_run),
                         fitnesses)


    def execute_one_run(self):
        """
        Execute one run of an experiment.

        Return highest score and its associated world and solution data.
        """
        # Initialize run values of populations
        self.attacker_pop.reset_run_values()
        self.defender_pop.reset_run_values()

        self.parsimony_log.write('\nRun ' + str(self.experiment.curr_run) + '\n')

        generation = 1
        print('\rGeneration', generation, end = ' ')

        # Initialize the populations and starting fitnesses
        self.initialize_population(self.attacker_pop)
        self.initialize_population(self.defender_pop)
        eval_count, self.attacker_pop.evals_with_no_change = \
            self.generation_evals(self.attacker_pop.individuals,
                                  self.defender_pop.individuals,
                                  0, 0, float('-inf'))

        # Run generation after generation until we hit termination condition
        # and break out of the loop
        while (True):

            # Update generation bookkeeping
            self.attacker_pop.generation_bookkeeping()
            self.attacker_pop.update_logs(eval_count, self.experiment.log_file, self.parsimony_log)
            self.defender_pop.generation_bookkeeping()

            # Update run bookkeeping
            self.attacker_pop.calc_run_stats()
            self.defender_pop.calc_run_stats()

            # Check for termination
            if (self.termination == 'number_of_evals'):
                if (eval_count >= self.experiment.num_fitness_evals_per_run):
                    break
            elif (self.termination == 'convergence'):
                if (self.attacker_pop.evals_with_no_change >= self.n_for_convergence):
                    print('CONVERGED at', eval_count, 'evals')
                    break
            else:
                print('Unknown termination method:', self.termination)
                sys.exit(1)

            # Not terminating? Let's proceed!

            generation += 1
            print('\rGeneration', generation, end = ' ')

            # Select parents
            attacker_parents = self.select_parents(self.attacker_pop)
            defender_parents = self.select_parents(self.defender_pop)

            # Recombine and/or mutate
            attacker_offspring = self.recombine_mutate(self.attacker_pop, attacker_parents)
            self.attacker_pop.individuals += attacker_offspring
            defender_offspring = self.recombine_mutate(self.defender_pop, defender_parents)
            self.defender_pop.individuals += defender_offspring

            # Evaluate offspring within the total population
            eval_count, self.attacker_pop.evals_with_no_change = \
                self.generation_evals(self.attacker_pop.individuals,
                                      self.defender_pop.individuals,
                                      eval_count, self.attacker_pop.evals_with_no_change,
                                      self.attacker_pop.gen_high_fitness)

            # Survival selection
            self.attacker_pop.individuals = self.select_survivors(self.attacker_pop)
            self.defender_pop.individuals = self.select_survivors(self.defender_pop)


        # Do CIAO plot here
        self.ciao_plot()

        # Play "exhibition game" to get best world data (does not count against Eval total).
        # This has a side effect of setting self.experiment.world_data
        print('Exhibition game: Attacker', self.attacker_pop.run_best_individual.fitness,
              'vs Defender', self.defender_pop.run_best_individual.fitness)
        self.execute_one_game(self.attacker_pop.run_best_individual,
                              self.defender_pop.run_best_individual)

        return self.attacker_pop.run_high_fitness, self.experiment.world_data, \
            str(self.attacker_pop.run_best_individual.root), \
            self.defender_pop.run_high_fitness, str(self.defender_pop.run_best_individual.root), \
            self.attacker_pop.run_best_individual.dot_viz(), \
            self.defender_pop.run_best_individual.dot_viz()

