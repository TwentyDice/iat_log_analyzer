# import pandas
from decimal import Decimal
import os
from typing import OrderedDict
import csv
import pprint
import re

import pandas

import iat_config_manager
import gui_manager

FILES_NAME_PROCESS_ERROR = "Some files could not be identified.\nCorrect the filename or remove them"


def get_info_from_filename(file_name):

    # Aggr-Impl35_t0-IATaggr_Block4_Version3&4.log

    s = str(file_name)
    if not s.endswith(".log"):
        raise ValueError("Wronge file format, must be .log")

    # Aggr-Impl35_t0-IATaggr_Block4_Version3&4.log
    #          ^^
    id = s.partition("Aggr-Impl")[2].partition("_t")[0]
    if not id.isnumeric:
        raise ValueError("participant id could not be determined")

    # Aggr-Impl35_t0-IATaggr_Block4_Version3&4.log
    #              ^
    t_id = s.partition("_t")[2].partition("-IATaggr")[0]
    if t_id not in ("0", "1"):
        raise ValueError("before/after incdicator could not be determined")

    # Aggr-Impl35_t0-IATaggr_Block4_Version3&4.log
    #                             ^
    block = s.partition("_Block")[2].partition("_Version")[0]
    if block not in ("1", "2", "3", "4", "5"):
        raise ValueError("Block number could not be determined")

    # Aggr-Impl35_t0-IATaggr_Block4_Version3&4.log
    #                                      ^^^
    version = s.partition("_Version")[2].partition(".log")[0]
    if version.find("&"):
        version = version.partition("&")[0]

    return (id, t_id, block, version)


def proc_single_file(file_path, cfg):

    table = pandas.read_csv(file_path,
                            sep='\t',
                            engine='python',
                            header=(2))

    aggregated_respones = {}

    errored_on_trial = []

    # iterate over table by index
    # did not find out how i can access columns in a row by column name
    for row_idx in table.index:
        print(table.loc[row_idx])

        # Leaving this in might be needed later, only process line if 1 cell starts with following value
        # if ("Aggr" in str(table.loc[row_idx, "Subject"])

        # Only process the row if the
        if not str(table.loc[row_idx, "Event Type"]) in cfg.event_type:
            continue

        # if trial number comes up more than 2 times means they answered wrong
        if not str(table.loc[row_idx, "Code"]) in cfg.code:
            continue

        # start on configured trial number
        if (trial_number := int(table.loc[row_idx, "Trial"])) < int(cfg.inclusive_minimum_trial_number):
            continue

        # consider min and max response times
        _response_time = int(str(table.loc[row_idx, "TTime"]))
        if not cfg.inclusive_minimum_response_time <= _response_time <= cfg.inclusive_maximum_response_time:
            continue

        # if trial number comes up more than 2 times means they answered wrong
        if ((len((table.loc[table["Trial"] == table.loc[row_idx, "Trial"]]).index)) != 2):
            if trial_number not in errored_on_trial:
                errored_on_trial.append(trial_number)
            if cfg.skip_errored_on_trial:
                continue

        pressed_direction = cfg.pressed_code_to_direction.get(
            str(table.loc[row_idx, "Code"]))

        if pressed_direction not in aggregated_respones:
            aggregated_respones[pressed_direction] = []

        aggregated_respones[pressed_direction].append({
            "Trial": trial_number,
            "TTime": _response_time})

    aggregated_respones["failed on trial"] = errored_on_trial

    return aggregated_respones


def verify_files_are_good(path):
    failed_files = {}
    with os.scandir(path) as dir:
        for entry in dir:
            try:
                # get participant id, before/after water, blocknumber, version from the single teststep
                id, t_id, block, version = get_info_from_filename(
                    str(entry.name))
            except Exception as e:
                failed_files[entry.name] = str(e)
                continue

    # Empty dictionaries evaluate to false
    if failed_files:
        gui_manager.show_key_value_list(failed_files)
        return False

    return True


def process_files(cfg=None):

    path = os.path.abspath(cfg.path_input_directory)

    if not verify_files_are_good(path=path):
        raise RuntimeError(
            "Not all Files were following the naming convention")

    participants = {}

    with os.scandir(path) as dir:
        for entry in dir:
            try:
                # get participant id, before/after water, blocknumber, version from the single teststep
                id, t_id, block, version = get_info_from_filename(
                    str(entry.name))
            except Exception as e:
                raise RuntimeError(
                    "Files were modified during runtime {} {}".format(str(entry.name), str(e)))

            # skip block if not wanted
            if not block in cfg.include_blocks:
                continue

            test_step_results = proc_single_file(entry.path, cfg)

            if id not in participants:
                participants[id] = {}
            if t_id not in participants[id]:
                participants[id][t_id] = {}
            if block not in participants[id][t_id]:
                participants[id][t_id][block] = {}

            person_root = {}

            for direction, trials_and_times_for_direction in test_step_results.items():
                if not direction in cfg.allowed_directions:
                    continue

                # this converts what the participant pressed (left or right) into the
                question_option = str(cfg.version_and_block_keypress_to_option_conversion_table.get(
                    version).get(block).get(direction))
                all_response_times = 0

                trials_per_direction = len(trials_and_times_for_direction)

                for trial in trials_and_times_for_direction:
                    all_response_times += Decimal(trial.get("TTime"))
                    person_root[question_option] = str(round(
                        Decimal(all_response_times/trials_per_direction/10), 3))

            # Important: if an option that can be pressed would occure multiple times PER block
            # per t_id (before/after water) this must be changed
            # TODO: I think the block can be aggregated away somehow
            # Or the option value which is assigned to the direction, in the big shitty version table can be de-tupled
            # to show direction association to aggresion / peace
            for pressable_option, average_reaction_for_option in person_root.items():
                participants[id][t_id][block][pressable_option] = average_reaction_for_option

        header_row = ["person_id",
                      "before_after_water",
                      "block",
                      ]

        pp = pprint.PrettyPrinter(depth=4)
        pp.pprint(participants)

        # add all possible option to header row aka line 1 of the table
        for person_id, before_after_water_subset in participants.items():
            for block_number, before_val in before_after_water_subset.items():
                for block_key, pressable_options in before_val.items():
                    for question_option in pressable_options.keys():
                        if (question_option not in header_row) and (question_option not in cfg.prohibit_output_options):
                            header_row.append(question_option)

        # You will need 'wb' mode in Python 2.x
        with open(cfg.path_output_file, 'w',  newline='', encoding='utf-8') as f:
            w = csv.DictWriter(f, fieldnames=OrderedDict(
                dict.fromkeys(header_row)), dialect=cfg.csv_dialect)
            w.writeheader()

            for person_id, before_after_water_subset in participants.items():
                out_line = OrderedDict(dict.fromkeys(header_row))
                for block_number, before_val in before_after_water_subset.items():
                    for block_key, pressable_options in before_val.items():
                        out_line = dict.fromkeys(header_row)
                        out_line["person_id"] = person_id
                        out_line["before_after_water"] = block_number
                        out_line["block"] = block_key

                        print_line = False
                        for option, average_reaction_time in pressable_options.items():
                            if option in cfg.prohibit_output_options:
                                continue
                            if average_reaction_time:
                                print_line = True
                                if option in out_line.keys():
                                    # Get a list of all non number in the calculated response
                                    # Replace all 
                                    seperators_list = re.findall(r'\D', average_reaction_time)
                                    for to_remove in  [' ', cfg.decimal_delimiter]:
                                        if to_remove in seperators_list:
                                            seperators_list.remove(to_remove)
                                    if seperators_list:
                                        for sep in seperators_list:
                                            average_reaction_time = average_reaction_time.replace(sep, cfg.decimal_delimiter)
                                    out_line[option] = average_reaction_time
                        if print_line:
                            w.writerow(out_line)

    return


if __name__ == "__main__":
    try:
        with iat_config_manager.IAT_config() as cfg:
            process_files(cfg)
    except Exception as e:
        gui_manager.show_error_msgbox(str(e))
        import sys
        print(sys.exc_info()[0])
        import traceback
        print(traceback.format_exc()) 
    finally:
        print("Execution finished.\nThis shows some data relevant to the Developer.\nPress Enter to close this Window.")
        input()
