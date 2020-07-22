import sys

from ..resources import variables as var
from ..levels.Level import Level
from ..levels.levels import levels

# Returns true if it's a banned command
def is_banned(command=""):
    if not command:
        return False

    if command in var.banned_commands:
        print("Let's not do that")
        return True
    
    for token in command.split(" "):
        if token in var.banned_tokens:
            print("Let's not do that")
            return True
    
    return False

# Runs the entire game and processes levels, returns if there is a level change
def game_process(command=""):
    if not command:
        return False
    
    # Grab current level reference
    currLevel = Level()
    if len(levels) >= var.currentLevel + 1:
        currLevel = levels[var.currentLevel]
    else:
        print("ERROR:\n var.currentLevel references a level that doesn't exist")
        return False
    
    # Check if user wants instruction
    if command.lower() == "level instruct":
        currLevel.instruct()
        return True
    
    # Check if user wants help
    if command.lower() == "level help":
        currLevel.help()
        return True
    
    # Check if user wants to check
    if command.lower() == "level check":
        # If check is successful
        if currLevel.check():
            # Increment currnet Level
            var.currentLevel += 1
            # If all levels are complete
            if len(levels) < var.currentLevel + 1:
                print("All levels completed!\nGreat job!")
                sys.exit(0)
            var.lev_bash_history.clear()
            print("\nLevel complete!")
            print("Level #{} instructions:".format(var.currentLevel))
            currLevel.instruct()
        else:
            print("Not quite complete yet. Keep trying!")
    
    # Return false otherwise
    return False

# Define special commands (Like not super important stuff)
def special(command=""):
    if not command:
        return False

    # Yes command
    if command == "yes":
        while True:
            print("y")
        return True

    # Makes user root
    elif command == "sudo su":
        var.isRoot = True
        return True
    
    # Returns username
    elif command == "whoami":
        if var.isRoot:
            print("root")
        else:
            print(var.username)

        return True
    
    # Prints out history
    elif command == "history":
        i = 1
        for x in var.bash_history:
            print("{}  {}".format(i, x))
            i += 1
        return True
    
    # Exit program
    elif command == "exit":
        sys.exit(0)
        return True # Never ever will run. Ever.
    
    # Wants last return code
    elif command == "$?":
        print()
    

    # Return false
    else:
        return False

    return False

# Interchanges certain tokens that should not be there
def interchange(command=""):
    if not command:
        return False
    
    # Replace $? with last exit code
    command = command.replace("$?", str(var.exit_code))

    # Replace * with all contents
    if "*" in command:
        contentNames = []
        for x in var.workingDir.contents:
            contentNames.append(x.name)
        if len(contentNames) == 0:
            command = command.replace("*", "")
        else:
            command = command.replace("*", " ".join(contentNames))

    # Update
    var.command = command

# Runs filesystem commands
# FIND FILESYSTEM COMMANDS IN INTERPRETER.PY
