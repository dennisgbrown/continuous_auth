# -*- coding: utf-8 -*-
import sys
import configparser
import random
import time
import traceback

from ccegpStrategy import CCEGPStrategy


class Experiment:
    """
    Provide capabilities to run an experiment within given
    configuration parameters.
    """

    def __init__(self, config_file_path):
        """
        Set up an experiment given a configuration file path and
        problem file path.
        """
        self.config_parser = None

        self.random_seed = None
        self.strategy = 'ccegp'
        self.num_runs_per_experiment = 1
        self.num_fitness_evals_per_run = 100
        self.log_file_path = 'logs/defaultLog.txt'
        self.log_file = None
        self.attacker_solution_file_path = 'solutions/defaultAttackerSolution.txt'
        self.defender_solution_file_path = 'solutions/defaultDefenderSolution.txt'
        self.high_score_world_file_path = 'worlds/defaultWorld.txt'
        self.world_data = None  # Array of strings that will be written to world data file

        self.num_attackers = 1
        self.num_defenders = 1

        self.attacker_exp_high_fitness = float('-inf')
        self.attacker_exp_best_solution = None
        self.defender_exp_high_fitness = float('-inf')
        self.defender_exp_best_solution = None

        # Which strategy does the defender use? (ccegp or saritas)
        self.defender_strategy = 'ccegp'

        # Time limit for game
        self.game_time_limit = 1000


        try:
            self.config_parser = configparser.ConfigParser()
            self.config_parser.read(config_file_path)

            try:
                self.random_seed = self.config_parser.getint('basic_options', 'random_seed')
                print('config: random_seed =', self.random_seed)
            except:
                print('config: random_seed not specified; using system time')
                self.random_seed = int(time.time() * 1000.0)
            random.seed(self.random_seed)

            try:
                self.strategy = self.config_parser.get('basic_options', 'strategy')
                print('config: strategy =', self.strategy)
            except:
                print('config: strategy not properly specified; using', self.strategy)

            try:
                self.num_runs_per_experiment = self.config_parser.getint('basic_options', 'num_runs_per_experiment')
                print('config: num_runs_per_experiment =', self.num_runs_per_experiment)
            except:
                print('config: num_runs_per_experiment not properly specified; using', self.num_runs_per_experiment)

            try:
                self.num_fitness_evals_per_run = self.config_parser.getint('basic_options',
                                                                           'num_fitness_evals_per_run')
                print('config: num_fitness_evals_per_run =', self.num_fitness_evals_per_run)
            except:
                print('config: num_fitness_evals_per_run not properly specified; using',
                      self.num_fitness_evals_per_run)

            try:
                self.log_file_path = self.config_parser.get('basic_options', 'log_file_path')
                print('config: log_file_path =', self.log_file_path)
            except:
                print('config: log_file_path not properly specified; using', self.log_file_path)

            try:
                self.attacker_solution_file_path = self.config_parser.get('basic_options', 'attacker_solution_file_path')
                print('config: attacker_solution_file_path =', self.attacker_solution_file_path)
            except:
                print('config: attacker_solution_file_path not properly specified; using', self.attacker_solution_file_path)

            try:
                self.defender_solution_file_path = self.config_parser.get('basic_options', 'defender_solution_file_path')
                print('config: defender_solution_file_path =', self.defender_solution_file_path)
            except:
                print('config: defender_solution_file_path not properly specified; using', self.defender_solution_file_path)

            try:
                self.defender_strategy = self.config_parser.get('basic_options', 'defender_strategy')
                print('config: defender_strategy =', self.defender_strategy)
            except:
                print('config: defender_strategy not specified; using', self.defender_strategy)

            try:
                self.game_time_limit = self.config_parser.getfloat('basic_options', 'game_time_limit')
                print('config: game_time_limit =', self.game_time_limit)
            except:
                print('config: game_time_limit not specified; using', self.game_time_limit)

            # Dump parms to log file
            try:
                self.log_file = open(self.log_file_path, 'w')

                self.log_file.write('Result Log\n\n')
                self.log_file.write('random seed: '
                                    + str(self.random_seed) + '\n')
                self.log_file.write('strategy: '
                                    + self.strategy + '\n')
                self.log_file.write('number of runs per experiment: '
                                    + str(self.num_runs_per_experiment) + '\n')
                self.log_file.write('number of fitness evals per run: '
                                    + str(self.num_fitness_evals_per_run) + '\n')
                self.log_file.write('attacker solution file path: '
                                    + self.attacker_solution_file_path + '\n')
                self.log_file.write('defender solution file path: '
                                    + self.defender_solution_file_path + '\n')
                self.log_file.write('defender_strategy: '
                                    + self.defender_strategy + '\n')
                self.log_file.write('game_time_limit: '
                                    + str(self.game_time_limit) + '\n')
            except:
                print('config: problem with log file', self.log_file_path)
                traceback.print_exc()
                return None

        except:
            traceback.print_exc()
            return None


    def run_experiment(self):
        """
        Run the experiment defined by the member variables contained in this
        experiment instance on the provided puzzle state.
        """

        start_time = time.time()

        strategy_instance = None
        if (self.strategy == 'ccegp'):
            strategy_instance = CCEGPStrategy(self)
        else:
            print('strategy unknown:', self.strategy)
            sys.exit(1)

        # For each run...
        for curr_run in range(1, self.num_runs_per_experiment + 1):

            # Update log
            self.curr_run = curr_run
            print('\nRun', curr_run)
            self.log_file.write('\nRun ' + str(curr_run) + '\n')

            # Execute one run and get best values.
            attacker_run_high_fitness, attacker_run_best_world_data, attacker_run_best_solution, \
                defender_run_high_fitness, defender_run_best_solution \
                = strategy_instance.execute_one_run()

            print('Best attacker tree of run:\n' + attacker_run_best_solution)
            print('Best defender tree of run:\n' + defender_run_best_solution)

            # If best of run is best overall, update appropriate values
            if (self.strategy != 'ccegp'):
                if (attacker_run_high_fitness > self.attacker_exp_high_fitness):
                    self.attacker_exp_high_fitness = attacker_run_high_fitness
                    print('New exp Attacker high fitness: ', self.attacker_exp_high_fitness)
                    self.attacker_exp_best_world_data = attacker_run_best_world_data
                    self.attacker_exp_best_solution = attacker_run_best_solution
            # If Competitive Co-evolution, add fitnesses (use Attacker to store most data)
            else:
                if ((attacker_run_high_fitness + defender_run_high_fitness) > self.attacker_exp_high_fitness):
                    self.attacker_exp_high_fitness = (attacker_run_high_fitness + defender_run_high_fitness)
                    print('New exp Attacker+Defender high fitness: ', self.attacker_exp_high_fitness)
                    self.attacker_exp_best_world_data = attacker_run_best_world_data
                    self.attacker_exp_best_solution = attacker_run_best_solution
                    self.defender_exp_best_solution = defender_run_best_solution


        # Dump best world to file
        the_file = open(self.high_score_world_file_path, 'w')
        for line in self.attacker_exp_best_world_data:
            the_file.write(line)
        the_file.close()

        # Dump best Attacker solution to file
        the_file = open(self.attacker_solution_file_path, 'w')
        the_file.write(self.attacker_exp_best_solution)
        the_file.close()

        # Dump best Defender solution to file
        if (self.strategy == 'ccegp'):
            the_file = open(self.defender_solution_file_path, 'w')
            the_file.write(self.defender_exp_best_solution)
            the_file.close()

        # Close out the log file
        if (not(self.log_file is None)):
            self.log_file.close()

        print(time.time() - start_time, 'seconds')
