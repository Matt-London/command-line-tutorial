from .colors import colors
DEBUG = True # Defines if should run debug utilities

isRoot = False # If the user is root
wd = "" # Current working directory
username = "user" # Defines username
hostname = "computer" # Defines hostname
shell = "splash" # Name of shell

ps1 = colors.fg.lightblue + username + colors.fg.darkgrey + "@" + colors.fg.red + hostname + colors.fg.lightcyan + ":" + colors.fg.cyan + "[~/" + wd + "] " + colors.fg.black + "> " + colors.fg.pink + "$#  "[isRoot] + colors.reset # Sets PS1

bash_history = [] # Saves all ran commands
currentLevel = 1 # contains current levels

args = [] # Contains current args for current command