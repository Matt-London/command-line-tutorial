from .colors import colors

DEBUG = True # Defines if should run debug utilities

isRoot = False # If the user is root
wd = "" # Current working directory
username = "user" # Defines username
hostname = "computer" # Defines hostname
shell = "splash" # Name of shell

ps1 = colors.fg.lightblue + username + colors.fg.darkgrey + "@" + colors.fg.red + hostname + colors.fg.lightcyan + ":" + colors.fg.cyan + "[~/" + wd + "] " + colors.fg.black + "> " + colors.fg.pink + "$#  "[isRoot] + colors.reset # Sets PS1

bash_history = [] # Saves all ran commands
lev_bash_history = [] # All ran commands, cleared after each level
currentLevel = 0 # contains current level index in levels

banned_commands = [] # List of banned commands
banned_tokens = [] # List of banned tokens

exit_code = 0 # Contains last exit code

command = "" # Contains current command
token = [] # Contains current args for current command

workingDir = None # Contains reference to working dir in Interpreter
