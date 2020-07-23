from . import variables as var
from os import system, name 
from ..filesystem.Directory import Directory
from ..filesystem.File import File

# This will check if something lives in the list of ran commands
# Takes a tuple which is strings that the history must contain
def check(needed=()):
    # Loop through needed param
    for command in needed:
        if command not in var.lev_bash_history:
            # If this isn't in it, it must return false
            return False

    # If everything is in it, it can return true
    return True

# Clears screen
# CREDIT: https://www.geeksforgeeks.org/clear-screen-python/
# By: mohit_negi
def clear(): 
    # for windows 
    if name == 'nt': 
        _ = system('cls') 
  
    # for mac and linux(here, os.name is 'posix') 
    else: 
        _ = system('clear') 