import sys

from ..resources import variables as var
from ..resources import functions as function
from ..levels.Level import Level
from ..levels.levels import levels
from ..filesystem.Directory import Directory
from ..filesystem.File import File

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
    token = command.split(" ")

    if not command:
        return False
    
    # Grab current level reference
    currLevel = Level()
    if len(levels) >= var.currentLevel + 1:
        currLevel = levels[var.currentLevel]
    else:
        print("ERROR:\n var.currentLevel references a level that doesn't exist")
        return False

    # Check if it's a level command
    if len(token) > 0 and token[0] == "level":
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
            
            return True
        
        # Not a valid entered command
        print("USAGE:\nlevel [OPTION]\n\ninstruct\tGet current level instructions\nhelp\t\tProvides help if the answer can't be found\ncheck\t\tChecks if the level is complete")
        return True
    
    
    
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

    # clear command
    elif command == "clear":
        function.clear()
        var.exit_code = 0
        return True

    # Makes user root
    elif command == "sudo su":
        var.isRoot = True
        var.username = "root"
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
        if var.isRoot:
            var.isRoot = False
            var.username = var.user
            return True
        else:
            sys.exit(0)
            return True # Never ever will run. Ever.
    
    # # Wants last return code
    # elif command == "$?":
    #     print()
    

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
def filesystem(command=""):
    verbose = False

    # Save vars locally
    token = var.token
    headDir = var.headDir
    workingDir = var.workingDir

    # mkdir command
    if token[0] == "mkdir":
        token.pop(0)
        if "-v" in token:
            verbose = True
            token.remove("-v")

        if "--verbose" in token:
            verbose = True
            token.remove("--verbose")

        if len(token) == 0:
            print("mkdir: missing operand")
            var.exit_code = 1
            return True

        if len(token) > 0:
            for arg in token:
                success = None
                try:
                    success = var.workingDir.mkdir(arg)
                except:
                    print("mkdir: cannot create directory ‘{}’: No such file or directory".format(arg))

                if verbose and success:
                    print("mkdir: created directory '{}'".format(arg))
            var.exit_code = 0
            return True
    
        return False

    # ls command
    elif token[0] == "ls":
        token.pop(0)
        if len(token) == 0:
            var.workingDir.ls()
            var.exit_code = 0
            return True

        elif len(token) == 1:
            var.workingDir.ls(token[0])
            var.exit_code = 0
            return True
        
        elif len(token) > 1:
            first = token.pop(0)
            print("{}:".format(first))
            var.workingDir.ls(first)
            for path in token:
                print("\n{}:".format(path))
                var.workingDir.ls(path)
            
            var.exit_code = 0
            return True
        
        else:
            return False
        return False
    
    # touch command
    elif token[0] == "touch":
        token.pop(0)
        
        if len(token) == 0:
            print("touch: missing file operand")
            var.exit_code = 1
            return True
        
        for path in token:
            var.workingDir.touch(path)
        var.exit_code = 0
        return True
    
    # rm command
    elif token[0] == "rm":
        token.pop(0)
        
        # Check if recursive
        recurse = False
        if "-r" in token:
            recurse = True
            token.remove("-r")

        elif "-rf" in token:
            recurse = True
            token.remove("-rf")
        
        # Make sure args are present
        if len(token) == 0:
            print("rm: missing operand")
            var.exit_code = 1
            return True

        # Run the command
        for x in token:
            workingDir.rm(x, recurse)
        var.exit_code = 0
        return True
        
    # rmdir command
    elif token[0] == "rmdir":
        token.pop(0)

        # Check if no args
        if len(token) == 0:
            print("rmdir: missing operand")
            var.exit_code = 1
            return True
        
        # Run command
        for x in token:
            var.workingDir.rmdir(x)
        
        var.exit_code = 0
        return True
    
    # cd command
    elif token[0] == "cd":
        token.pop(0)
        if len(token) == 0:
            workingDir = headDir
            var.wd = ""
            var.exit_code = 0
            var.token = token
            var.headDir = headDir
            var.workingDir = workingDir
            return True
        
        # Check for too many args
        if len(token) > 1:
            print("{}: cd: too many arguments".format(var.shell))
            var.exit_code = 1
            return True

        # Set path to only arg
        path = token[0]

        # Check if dir exists
        if workingDir.get_sub(path):
            # Check if it's a dir
            if type(workingDir.get_sub(path)) == Directory:
                var.workingDir = workingDir.get_sub(path)
                var.wd = var.workingDir.get_path()
                
                var.exit_code = 0
                var.token = token
                var.headDir = headDir
                return True

            else:
                print("{}: cd: {}: Not a directory".format(var.shell, path))
                var.exit_code = 1
                return True
            
        else:
            print("{}: cd: {}: No such file or directory".format(var.shell, path))
            var.exit_code = 1
            return True
    
    # pwd command
    elif token[0] == "pwd":
        print("/home/{}{}".format(var.user, var.workingDir.get_path()[1:]))
        var.exit_code = 0
        var.token = token
        var.headDir = headDir
        var.workingDir = workingDir
        return True

    # Kind of vim
    elif token[0] == "vim" or token[0] == "nano":
        base = token.pop(0)

        overwrite = "-o" in token
        append = "-a" in token

        if overwrite and append:
            print("Either '-o' or '-a', not both")
            var.exit_code = 1
            return True

        # Clean up args
        if overwrite:
            token.remove("-o")

        if append:
            token.remove("-a")
        
        if len(token) > 1:
            print("Give only one path")
            var.exit_code = 1
            return True
        elif len(token) < 1:
            print("USAGE:\nvim (or nano)\t[OPTIONS]\tPath/to/file")
            print("-o\tOverwrite any existing text")
            print("-a\tAppend to existing text (default)")
            print("-h\tDisplay this help message")
            var.exit_code = 1
            return True
        
        path = token.pop(0)

        # Create/save reference file
        f = None
        # Check if given path of file that exists
        if type(var.workingDir.get_sub(path)) == File:
            f = var.workingDir.get_sub(path)
        # Check if given path of dir
        elif type(var.workingDir.get_sub(path)) == Directory:
            print("{}: {}: cannot write to '{}': Is a directory".format(var.shell, base, path))
        # Check if top dir exists
        elif var.workingDir.get_sub("/".join(path.split("/")[:-1])):
            var.workingDir.touch(path)
            f = var.workingDir.get_sub(path)
        else:
            var.exit_code = 1
            return False

        print("Type contents (press ctrl-d to end):")
        fileContents = sys.stdin.read()

        if append:
            f.append(fileContents)
        else:
            f.write(fileContents)

        var.exit_code = 0
        return True
    
    # Cat command
    elif token[0] == "cat":
        token.pop(0)
        if len(token) == 0:
            try:
                while True:
                    repeat = input()
                    print(repeat)
            except KeyboardInterrupt:
                print()
                var.exit_code = 130
                return True

        for arg in token:
            # Check if it's a file
            if type(var.workingDir.get_sub(arg)) == File:
                print(var.workingDir.get_sub(arg).read())
            elif type(var.workingDir.get_sub(arg)) == Directory:
                print("cat: {}: Is a directory".format(arg))
        return True

    # mv command
    elif token[0] == "mv":
        token.pop(0)

        verbose = False

        if "-v" in token:
            verbose = True
            token.remove("-v")

        if "--verbose" in token:
            verbose = True
            token.remove("--verbose")

        # Make sure correct args
        if len(token) == 0:
            print("mv: missing file operand")
            var.exit_code = 1
            return True
        elif len(token) == 1:
            print("mv: missing destination file operand after '{}'".format(token[0]))
            var.exit_code = 1
            return True

        # If it has a dir at the end
        if type(var.workingDir.get_sub(token[-1])) == Directory:
            dest = token.pop(-1)
            for arg in token:
                # Make sure they're not the same
                if var.workingDir.get_sub(dest) == var.workingDir.get_sub(arg):
                    print("mv: cannot move '{0}' to a subdirectory of itself, '{0}/{1}'".format(dest, dest.split("/")[-1]))
                    continue

                if var.workingDir.mv(arg, dest):
                    if verbose:
                        print("renamed '{}' -> '{}'".format(arg, dest))
            var.exit_code = 0
            return True
        
        else:
            # Make sure there's just two args
            if len(token) == 2:
                if var.workingDir.mv(token[0], token[1]):
                    if verbose:
                        print("renamed '{}' -> '{}'".format(token[0], token[1]))
                    var.exit_code = 0
                    return True
        
        return True

    # cp command
    elif token[0] == "cp":
        token.pop(0)

        verbose = False
        recurse = False

        if "-v" in token:
            verbose = True
            token.remove("-v")

        if "--verbose" in token:
            verbose = True
            token.remove("--verbose")
        
        if "-r" in token:
            recurse = True
            token.remove("-r")

        
        # Make sure correct args
        if len(token) == 0:
            print("cp: missing file operand")
            var.exit_code = 1
            return True
        elif len(token) == 1:
            print("cp: missing destination file operand after '{}'".format(token[0]))
            var.exit_code = 1
            return True

        # If it has a dir at the end
        if type(var.workingDir.get_sub(token[-1])) == Directory:
            dest = token.pop(-1)
            for arg in token:
                # Check if recurse if its a dir
                if type(var.workingDir.get_sub(arg)) == Directory:
                    if not recurse:
                        print("cp: -r not specified; omitting directory '{}'".format(arg))
                        var.exit_code = 1
                        continue

                # Make sure they're not the same
                if var.workingDir.get_sub(dest) == var.workingDir.get_sub(arg):
                    print("cp: cannot copy '{0}' to a subdirectory of itself, '{0}/{1}'".format(dest, dest.split("/")[-1]))
                    continue

                if var.workingDir.cp(arg, dest, recurse):
                    if verbose:
                        print("'{}' -> '{}'".format(arg, dest))
            var.exit_code = 0
            return True
        
        else:
            # Make sure there's just two args
            if len(token) == 2:
                if not recurse and type(var.workingDir.get_sub(token[0])) == Directory:
                    print("cp: -r not specified; omitting directory '{}'".format(token[0]))
                    var.exit_code = 1
                    return True

                if var.workingDir.cp(token[0], token[1], recurse):
                    if verbose:
                        print("'{}' -> '{}'".format(token[0], token[1]))
                    var.exit_code = 0
                    return True
        
        return True


    # Save tokens and workingDir and head
    var.token = token
    var.headDir = headDir
    var.workingDir = workingDir
