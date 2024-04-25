# import pandas
import os
import json
import gui_manager
from datetime import datetime as dt

CONFIG_FILE_NAME = "IAT_config.json"

INPUT_DIR_SELECT_MESSAGE = "Select folder with all files to be processed"
OUTPUT_DIR_SELECT_MESSAGE = "Select where the Results file will be saved.\n"\
    "The results file has a timestamp, to distinguish when doing multiple runs.\n"\
    "Do not use the same directory, used for the input data!"
CONFIG_MODIFY_FAILED = "Could not modify config file (File open?)"
CREATING_DEFAULT_CONFIG = "no config file found, creating default config"

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

ME_AGGRO = (ME, AGGRO)
ME_AGGRO = "Ich Aggression"

_default_config = {
    'version_and_block_keypress_to_option_conversion_table': {
        "1": {
            # blocks
            "1": {LEFT: ME,
                  RIGHT: OTHERS},
            "2": {LEFT: AGGRO,
                  RIGHT: PEACE},
            "3": {LEFT: ME_AGGRO,
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
                  RIGHT: ME_AGGRO}
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
            "5": {LEFT: ME_AGGRO,
                  RIGHT: (OTHERS, PEACE)}
        },
        "4": {
            "1": {LEFT: OTHERS,
                  RIGHT: ME},
            "2": {LEFT: PEACE,
                  RIGHT: AGGRO},
            "3": {LEFT: (OTHERS, PEACE),
                  RIGHT: ME_AGGRO},
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
    'output_filename': 'results-',    
    'csv_dialect': "excel-tab",
    'output_filename_format': '.tsv',
    'include_blocks': ["3", "5"],
    'inclusive_minimum_trial_number': 0,
    'inclusive_minimum_response_time': 4000,
    'inclusive_maximum_response_time': 100000,
    'event_type': ["Response"],
    'code': ["1", "2"],
    'skip_errored_on_trial': True,
    'prohibit_output_options': []
}


class IAT_config:
    # directory wher this file currently is, so the config.json must always be in the same one
    _exec_dirname = os.path.dirname(os.path.abspath(__file__))
    _config_location = (os.path.join(_exec_dirname, CONFIG_FILE_NAME))

    def __init__(self):
        if os.path.exists(self._config_location):
            try:
                self.__dict__ = json.load(open(self._config_location))
            except Exception:
                gui_manager.show_error_msgbox(CONFIG_MODIFY_FAILED)
        else:
            gui_manager.show_info_msgbox(CREATING_DEFAULT_CONFIG)
            self.__dict__ = _default_config
            self.save_config_to_file()
        self.create_input_output_paths()

    def __enter__(self):
        return self

    def create_input_output_paths(self):
        # Show an info window with what folder user should select
        # then open dialog for directory selection
        self.path_input_directory = gui_manager.get_dir_with_info_msgbox(
            msg=INPUT_DIR_SELECT_MESSAGE)

        output_filename = "".join([self.output_filename,
                                    dt.now().strftime("%Y-%m-%d_%H-%M-%S"),
                                      self.output_filename_format])

        self.path_output_file = os.path.join(
            gui_manager.get_dir_with_info_msgbox(
                msg=OUTPUT_DIR_SELECT_MESSAGE),output_filename)

    def save_config_to_file(self):
        try:
            json.dump(self.__dict__,
                      open(self._config_location, 'w'),
                      indent=4,
                      separators=(',', ': '))
        except Exception:
            gui_manager.show_error_msgbox(CONFIG_MODIFY_FAILED)

    def __exit__(self, exc_type, exc_value, traceback):
        self.save_config_to_file()
