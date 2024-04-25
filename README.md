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

naming scheme
walkthrough
settings

# Configuration
You dont have to create the configuration manually. The configuration manager has a hardcoded default configuration with everything you need, that.\
Deleting the configuration file will reset it to default. If you mess up your configuration\
Determine where your "IAT_config.json" file is, see above \
