# import pandas
import os
import json

CONFIG_FILE_NAME = "IAT_config.json"

t_code_trans = {
    "0": "before",
    "1": "after"
}

LEFT = "links"
RIGHT = "rechts"

ME = "Ich"
OTHERS = "Andere"
AGGRO = "Aggression"
PEACE = "Friedlichkeit"


# todo make a setting that auto gens this directory
_default_config = {
    'version_and_block_keypress_to_option_conversion_table' : {
        "1": {
            # blocks
            "1": {LEFT: ME,
                  RIGHT: OTHERS},
            "2": {LEFT: AGGRO,
                  RIGHT: PEACE},
            "3": {LEFT: (ME, AGGRO),
                  RIGHT: (OTHERS, PEACE)},
            "4": {LEFT: PEACE,
                  RIGHT: AGGRO},
            "5": {LEFT: (ME, PEACE),
                  RIGHT: (OTHERS, AGGRO)}
        },
        "2": {
            "1": {LEFT: OTHERS,
                  RIGHT: ME},
            "2": {LEFT: AGGRO,
                  RIGHT: PEACE},
            "3": {LEFT: (OTHERS, AGGRO),
                  RIGHT: (ME, PEACE)},
            "4": {LEFT: PEACE,
                  RIGHT: AGGRO},
            "5": {LEFT: (OTHERS, PEACE),
                  RIGHT: (ME, AGGRO)}
        },
        "3": {
            "1": {LEFT: ME,
                  RIGHT: OTHERS},
            "2": {LEFT: PEACE,
                  RIGHT: AGGRO},
            "3": {LEFT: (ME, PEACE),
                  RIGHT: (OTHERS, AGGRO)},
            "4": {LEFT: AGGRO,
                  RIGHT: PEACE},
            "5": {LEFT: (ME, AGGRO),
                  RIGHT: (OTHERS, PEACE)}
        },
        "4": {
            "1": {LEFT: OTHERS,
                  RIGHT: ME},
            "2": {LEFT: PEACE,
                  RIGHT: AGGRO},
            "3": {LEFT: (OTHERS, PEACE),
                  RIGHT: (ME, AGGRO)},
            "4": {LEFT: AGGRO,
                  RIGHT: PEACE},
            "5": {LEFT: (OTHERS, AGGRO),
                  RIGHT: (ME, PEACE)}
        }
    },
    't_code_translation': {
        "0": "before",
        "1": "after"
    },
    'pressed_code_to_direction': {
        "1": LEFT,
        "2": RIGHT
    },
    'allowed_directions': [LEFT, RIGHT],
    'csv_dialect' : "excel-tab",
    'input_directory': 'input',
    'output_directory': 'output',
    'output_filename': 'results.tsv',
    'include_blocks': ["3", "5"],
    'inclusive_min_trial_number': 0,
    'inclusive_minimum_response_time': 4000,
    'inclusive_maximum_response_time': 100000,
    'event_type': ["Response"],
    'code': ["1", "2"],
    'skip_errored_on_trial': True
}


class IAT_config:
    # directory wher this file currently is, so the config.json must always be in the same one
    _exec_dirname = os.path.dirname(os.path.abspath(__file__))
    _config_location = (os.path.join(_exec_dirname, CONFIG_FILE_NAME))

    def __init__(self):
        if os.path.exists(self._config_location):
            try:
                self.__dict__ = json.load(open(self._config_location))
                self.create_full_paths()
            except Exception:
                print("Failed to open config (File open?)")
        else:
            print("no config file found, creating default config")
            self.__dict__ = _default_config
            self.save_config_to_file()

    def __enter__(self):
        return self

    def create_full_paths(self):
        self.path_input_directory = os.path.join(
            self._exec_dirname, self.input_directory)
        self.path_output_file = os.path.join(
            self._exec_dirname, self.output_directory, self.output_filename)

    def save_config_to_file(self):
        self.create_full_paths()
        try:
            json.dump(self.__dict__,
                      open(self._config_location, 'w'),
                      indent=4,
                      separators=(',', ': '))
        except Exception:
            print("Failed to save config (File open?)")

    def __exit__(self, exc_type, exc_value, traceback):
        self.save_config_to_file()
