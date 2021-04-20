# -*- coding: utf-8 -*-
import sys
import configparser
import random
import time
import traceback
import ast

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
        self.attacker_solution_dot_path = 'solutions/defaultAttackerSolution.dot'
        self.attacker_solution_png_path = 'solutions/defaultAttackerSolution.png'
        self.defender_solution_file_path = 'solutions/defaultDefenderSolution.txt'
        self.defender_solution_dot_path = 'solutions/defaultDefenderSolution.dot'
        self.defender_solution_png_path = 'solutions/defaultDefenderSolution.png'
        self.high_score_world_file_path = 'worlds/defaultWorld.txt'
        self.world_data = None  # Array of strings that will be written to world data file

        self.render_solutions = False
        self.print_dots = False
        self.attacker_open_png = False
        self.defender_open_png = False

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

        # List of CA classifiers to use
        self.ca_classifiers = []

        # game parameters
        self.lambda_u = 1
        self.beta_u = 100
        self.sigma_u = 3
        self.eta_u = 0.01
        self.nu_r = 0.1
        self.delta_l = 0.1
        self.delta_a = 0.2
        self.q = 0.7
        self.gamma = 0.1
        self.rho = 0.98
        self.user_bonus = 1
        self.attacker_penalty = 1
        self.IDLess = False

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
                self.attacker_solution_dot_path = self.config_parser.get('basic_options', 'attacker_solution_dot_path')
                print('config: attacker_solution_dot_path =', self.attacker_solution_dot_path)
            except:
                print('config: attacker_solution_dot_path not properly specified; using', self.attacker_solution_dot_path)

            try:
                self.attacker_solution_png_path = self.config_parser.get('basic_options', 'attacker_solution_png_path')
                print('config: attacker_solution_png_path =', self.attacker_solution_png_path)
            except:
                print('config: attacker_solution_png_path not properly specified; using', self.attacker_solution_png_path)

            try:
                self.defender_solution_file_path = self.config_parser.get('basic_options', 'defender_solution_file_path')
                print('config: defender_solution_file_path =', self.defender_solution_file_path)
            except:
                print('config: defender_solution_file_path not properly specified; using', self.defender_solution_file_path)

            try:
                self.defender_solution_dot_path = self.config_parser.get('basic_options', 'defender_solution_dot_path')
                print('config: defender_solution_dot_path =', self.defender_solution_dot_path)
            except:
                print('config: defender_solution_dot_path not properly specified; using', self.defender_solution_dot_path)

            try:
                self.defender_solution_png_path = self.config_parser.get('basic_options', 'defender_solution_png_path')
                print('config: defender_solution_png_path =', self.defender_solution_png_path)
            except:
                print('config: defender_solution_png_path not properly specified; using', self.defender_solution_png_path)

            try:
                self.high_score_world_file_path = self.config_parser.get('basic_options', 'high_score_world_file_path')
                print('config: high_score_world_file_path =', self.high_score_world_file_path)
            except:
                print('config: high_score_world_file_path not properly specified; using', self.high_score_world_file_path)

            try:
                self.render_solutions = self.config_parser.getboolean('basic_options', 'render_solutions')
                print('config: render_solutions =', self.render_solutions)
            except:
                print('config: render_solutions not properly specified; using', self.render_solutions)

            try:
                self.print_dots = self.config_parser.getboolean('basic_options', 'print_dots')
                print('config: print_dots =', self.print_dots)
            except:
                print('config: print_dots not properly specified; using', self.print_dots)

            try:
                self.attacker_open_png = self.config_parser.getboolean('basic_options', 'attacker_open_png')
                print('config: attacker_open_png =', self.attacker_open_png)
            except:
                print('config: attacker_open_png not properly specified; using', self.attacker_open_png)

            try:
                self.defender_open_png = self.config_parser.getboolean('basic_options', 'defender_open_png')
                print('config: defender_open_png =', self.defender_open_png)
            except:
                print('config: defender_open_png not properly specified; using', self.defender_open_png)

            # Parse gamestate config properties
            try:
                self.defender_strategy = self.config_parser.get('game_options', 'defender_strategy')
                print('config: defender_strategy =', self.defender_strategy)
            except:
                print('config: defender_strategy not specified; using', self.defender_strategy)

            try:
                self.game_time_limit = self.config_parser.getfloat('game_options', 'game_time_limit')
                print('config: game_time_limit =', self.game_time_limit)
            except:
                print('config: game_time_limit not specified; using', self.game_time_limit)

            try:
                self.ca_classifiers = ast.literal_eval(self.config_parser.get('game_options', 'ca_classifiers'))
                print('config: ca_classifiers =', self.ca_classifiers)
            except:
                print('config: ca_classifiers not specified; using', self.ca_classifiers)

            try:
                self.lambda_u = self.config_parser.getfloat('game_options', 'lambda_u')
                print('config: lambda_u =', self.lambda_u)
            except:
                print('config: lambda_u not specified; using', self.lambda_u)

            try:
                self.beta_u = self.config_parser.getfloat('game_options', 'beta_u')
                print('config: beta_u =', self.beta_u)
            except:
                print('config: beta_u not specified; using', self.beta_u)

            try:
                self.sigma_u = self.config_parser.getfloat('game_options', 'sigma_u')
                print('config: sigma_u =', self.sigma_u)
            except:
                print('config: sigma_u not specified; using', self.sigma_u)

            try:
                self.eta_u = self.config_parser.getfloat('game_options', 'eta_u')
                print('config: eta_u =', self.eta_u)
            except:
                print('config: eta_u not specified; using', self.eta_u)

            try:
                self.nu_r = self.config_parser.getfloat('game_options', 'nu_r')
                print('config: nu_r =', self.nu_r)
            except:
                print('config: nu_r not specified; using', self.nu_r)

            try:
                self.delta_l = self.config_parser.getfloat('game_options', 'delta_l')
                print('config: delta_l =', self.delta_l)
            except:
                print('config: delta_l not specified; using', self.delta_l)

            try:
                self.delta_a = self.config_parser.getfloat('game_options', 'delta_a')
                print('config: delta_a =', self.delta_a)
            except:
                print('config: delta_a not specified; using', self.delta_a)

            try:
                self.q = self.config_parser.getfloat('game_options', 'q')
                print('config: q =', self.q)
            except:
                print('config: q not specified; using', self.q)

            try:
                self.gamma = self.config_parser.getfloat('game_options', 'gamma')
                print('config: gamma =', self.gamma)
            except:
                print('config: gamma not specified; using', self.gamma)

            try:
                self.rho = self.config_parser.getfloat('game_options', 'rho')
                print('config: rho =', self.rho)
            except:
                print('config: rho not specified; using', self.rho)

            try:
                self.user_bonus = self.config_parser.getfloat('game_options', 'user_bonus')
                print('config: user_bonus =', self.user_bonus)
            except:
                print('config: user_bonus not specified; using', self.user_bonus)

            try:
                self.attacker_penalty = self.config_parser.getfloat('game_options', 'attacker_penalty')
                print('config: attacker_penalty =', self.attacker_penalty)
            except:
                print('config: attacker_penalty not specified; using', self.attacker_penalty)

            try:
                self.IDLess = self.config_parser.getboolean('game_options', 'IDLess')
                print('config: IDLess =', self.IDLess)
            except:
                print('config: IDLess not specified; using', self.IDLess)

            # Dump parms to log file
            try:
                self.log_file = open(self.log_file_path, 'w')

                self.log_file.write('Result Log\n\n')
                self.log_file.write('random seed: ' + str(self.random_seed) + '\n')
                self.log_file.write('strategy: ' + self.strategy + '\n')
                self.log_file.write('number of runs per experiment: '
                                    + str(self.num_runs_per_experiment) + '\n')
                self.log_file.write('number of fitness evals per run: '
                                    + str(self.num_fitness_evals_per_run) + '\n')
                self.log_file.write('attacker solution file path: '
                                    + self.attacker_solution_file_path + '\n')
                self.log_file.write('attacker solution dot path: '
                                    + self.attacker_solution_dot_path + '\n')
                self.log_file.write('attacker solution png path: '
                                    + self.attacker_solution_png_path + '\n')
                self.log_file.write('defender solution file path: '
                                    + self.defender_solution_file_path + '\n')
                self.log_file.write('defender solution dot path: '
                                    + self.defender_solution_dot_path + '\n')
                self.log_file.write('defender solution png path: '
                                    + self.defender_solution_png_path + '\n')
                self.log_file.write('high score world file path: '
                                    + self.high_score_world_file_path + '\n')
                self.log_file.write('defender_strategy: ' + self.defender_strategy + '\n')
                self.log_file.write('game_time_limit: ' + str(self.game_time_limit) + '\n')
                self.log_file.write('ca_classifiers: ' + str(self.ca_classifiers) + '\n')
                self.log_file.write('lambda_u: ' + str(self.lambda_u) + '\n')
                self.log_file.write('beta_u: ' + str(self.beta_u) + '\n')
                self.log_file.write('sigma_u: ' + str(self.sigma_u) + '\n')
                self.log_file.write('eta_u: ' + str(self.eta_u) + '\n')
                self.log_file.write('nu_r: ' + str(self.nu_r) + '\n')
                self.log_file.write('delta_l: ' + str(self.delta_l) + '\n')
                self.log_file.write('delta_a: ' + str(self.delta_a) + '\n')
                self.log_file.write('q: ' + str(self.q) + '\n')
                self.log_file.write('gamma: ' + str(self.gamma) + '\n')
                self.log_file.write('rho: ' + str(self.rho) + '\n')
                self.log_file.write('user_bonus: ' + str(self.user_bonus) + '\n')
                self.log_file.write('attacker_penalty: ' \
                                    + str(self.attacker_penalty) + '\n')
                self.log_file.write('IDLess: ' + str(self.IDLess) + '\n')

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
                defender_run_high_fitness, defender_run_best_solution, attacker_dot, defender_dot \
                = strategy_instance.execute_one_run()

            print('\nBest attacker tree of run:\n' + attacker_run_best_solution)
            if (self.print_dots):
                print('\nBest attacker dot of run:\n' + str(attacker_dot))
            print('\nBest defender tree of run:\n' + defender_run_best_solution)
            if (self.print_dots):
                print('\nBest defender dot of run:\n' + str(defender_dot))

            # If best of run is best overall, update appropriate values
            if (self.strategy != 'ccegp'):
                if (attacker_run_high_fitness > self.attacker_exp_high_fitness):
                    self.attacker_exp_high_fitness = attacker_run_high_fitness
                    print('New exp Attacker high fitness: ', self.attacker_exp_high_fitness)
                    self.attacker_exp_best_world_data = attacker_run_best_world_data
                    self.attacker_exp_best_solution = attacker_run_best_solution
                    self.attacker_exp_best_dot = attacker_dot
            # If Competitive Co-evolution, add fitnesses (use Attacker to store most data)
            else:
                if ((attacker_run_high_fitness + defender_run_high_fitness) > self.attacker_exp_high_fitness):
                    self.attacker_exp_high_fitness = (attacker_run_high_fitness + defender_run_high_fitness)
                    print('New exp Attacker+Defender high fitness: ', self.attacker_exp_high_fitness)
                    self.attacker_exp_best_world_data = attacker_run_best_world_data
                    self.attacker_exp_best_solution = attacker_run_best_solution
                    self.defender_exp_best_solution = defender_run_best_solution
                    self.attacker_exp_best_dot = attacker_dot
                    self.defender_exp_best_dot = defender_dot

        # Dump best world to file
        the_file = open(self.high_score_world_file_path, 'w')
        for line in self.attacker_exp_best_world_data:
            the_file.write(line)
        the_file.close()

        # Dump best Attacker solution (text) to file
        the_file = open(self.attacker_solution_file_path, 'w')
        the_file.write(self.attacker_exp_best_solution)
        the_file.close()

        # Dump best Defender solution (text) to file
        if (self.strategy == 'ccegp'):
            the_file = open(self.defender_solution_file_path, 'w')
            the_file.write(self.defender_exp_best_solution)
            the_file.close()

        # Dump best Attacker solution (dot) to file
        the_file = open(self.attacker_solution_dot_path, 'w')
        the_file.write(str(self.attacker_exp_best_dot))
        the_file.close()

        # Dump best Defender solution (dot) to file
        if (self.strategy == 'ccegp'):
            the_file = open(self.defender_solution_dot_path, 'w')
            the_file.write(str(self.defender_exp_best_dot))
            the_file.close()

        # Dump and display best Attacker solution
        if (self.render_solutions):
            self.attacker_exp_best_dot.render(filename=self.attacker_solution_png_path,
                                              view=self.attacker_open_png,
                                              format='png')

        # Dump and display best Defender solution
        if (self.render_solutions and self.strategy == 'ccegp'):
            self.defender_exp_best_dot.render(filename=self.defender_solution_png_path,
                                              view=self.defender_open_png,
                                              format='png')

        # Close out the log file
        if (not(self.log_file is None)):
            self.log_file.close()

        print(time.time() - start_time, 'seconds')
