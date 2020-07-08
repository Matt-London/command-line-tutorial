from . import variables as var
# This will check if something lives in the list of ran commands
# Takes a tuple which is strings that the history must contain
def check(needed=()):
    # Loop through needed param
    for command in needed:
        if command not in var.bash_history:
            # If this isn't in it, it must return false
            return False

    # If everything is in it, it can return true
    return True