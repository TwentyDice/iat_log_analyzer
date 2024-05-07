# iat_log_analyzer

# How to Install
All of this was only tested on Windows 10, but should work on Windows 11 and Linux / MacOs. \
Create a folder on your system where the program files can be stored, make sure you have read and write acces on your user. 
## Using the Installer 
Download #Todo:\
Move the Executable to the new folder and run it. This installs everything and runs the program. \
The Configuration file will be in the newly created folder, its called "IAT_config.json" \
You can create a Shortcut to the Executeable and move the shortcut to your desktop. 

## Without the installer (Linux / MacOS / I know what I'm doing):
This Software is made with Python and uses the Data Analysis Library Pandas.\
You need to Install Python on your System, Version 3.9 or higher and Pandas.\
Go to https://www.python.org/downloads/ download and run the Python installer.\
Include the package installer pip in in the installation, this is the default option.\
If Python installed without pip, you can install it manually. See here: https://pip.pypa.io/en/stable/installation/ \
Open the command prompt and install pandas. 
```
pip install pandas
```
Downlaod this repository and unpack the Zipfile to the new folder 
```
https://github.com/TwentyDice/iat_log_analyzer/archive/refs/heads/main.zip
```
Or if you have git installed clone this repository. 
```
git clone https://github.com/TwentyDice/iat_log_analyzer.git
```
Right click "main.py" open with Python. \
If you dont see that option manually execute it over the command prompt. 
```
python your-directory\main.py
```

# User Guide
## Naming scheme of Log files
Each log file must follow the naming scheme, because the program takes Data from the filename, that is not present elsewhere:


## Walkthrough


# Configuration
You dont have to create the configuration manually. The configuration manager has a hardcoded default configuration with everything you need, that is created on first execution.\
If you mess up your configuration beyond repair you can delete it, to get the defaults back. \
Determine where your "IAT_config.json" file is, see above. For now the config is determined by filename in the same directory as the  \
If for whatever reason you want to work with multiple configs, you can just save them and switch configurations by changing the file names \
Create a Backup of the file, before making any changes!.  \

## How to configure
The analyzer uses a single json file for configuration. \
This includes statitc data needed to process data and configuration values that can be changed \
If the value is not mentioned in the following list, DO NOT CHANGE IT YOU WILL BREAK STUFF
### output_filename
File name prefix, of the output file. Full file name is this + timestamp + output_filename_format. \
Change to your liking, but must be a valid file name on your operation System. 
### csv_dialect
Determines the Output format of the File. The output is a Table that will be produced. \
`excel-tab` (Default) Creates a Tab seperated values file. This can easily be imported into excel. \
`excel` Creates a comma seperated values file. This can easily be imported into excel, make sure `floating_decimal_delimiter` is not a `,` \
`unix` See here: https://docs.python.org/3/library/csv.html#csv.unix_dialect
### output_filename_format
File format of the output file, this direcly relates to csv_dialect setting. Include the `.` in the format. \
For `excel-tab` use `.tsv` (Default) \
For `excel` use `.csv`
### decimal_delimiter
Delimiter symbol used for decimal numbers, free text. default is `.` \
If you want to import into Excel on a computer with german settings, change to `,`
### include_blocks
List of Blocks that should be processed. List of ["1", "2", "3", "4", "5"] \
If the block number is not include, it will not be processed. \
Default `["3", "5"]`
## inclusive_minimum_trial_number
Starting point on which trial number (Column Tiral) the calculation will be done. \
Default `0`
## inclusive_minimum_response_time & inclusive_maximum_response_time
Minimum and Maximum response time that will be processed. \
This is to exclude people pressing the button on accident, or outside a reasonable amount of time. \
Default `4000 - 100000`
## skip_errored_on_trial
What to do with the result if the participant makes a mistake `true` will not include it `false` \
You should probably leave this on skip, because there is only 2 options in this trial, so if you press 1 and 1 is wrong, you press 2 without thinking.  \
Default `true`