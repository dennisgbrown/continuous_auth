# -*- coding: utf-8 -*-
import sys

sys.path.append('code')
from gameState import GameState


class GameScenarioInfo:
    """
    Class to hold a game scenario. Initialize from a scenario file.
    """
    def __init__(self, scenario_file_path):
        self.game_scenario = None
        self.width = 0
        self.height = 0
        self.num_walls = 0

        with open(scenario_file_path, 'r') as reader:
            curr_line = reader.readline()

            # Get scenario dimensions
            dims = list(curr_line.split(' '))
            self.width = int(dims[0])
            self.height = int(dims[1])

            # Fill internal representation of scenario
            self.game_scenario = [[] for _ in range(self.height)]
            for curr_row_idx in range(self.height):
                row_string = reader.readline()
                self.game_scenario[self.height - curr_row_idx - 1] = \
                    self.convert_row_string_to_list(row_string)

        # Calculate number of walls
        self.num_walls = sum([curr_row.count(GameState.WALL) \
                              for curr_row in self.game_scenario])


    @staticmethod
    def convert_row_string_to_list(row_string):
        """
        Given a row from a scenario file, return a matrix row for internal representation.
        """
        row = []
        for curr_char in row_string:
            if (curr_char == '#'):
                row.append(GameState.WALL)
            if (curr_char == '~'):
                row.append(GameState.OPEN)
        return row
