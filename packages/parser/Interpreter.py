from ..resources.colors import colors
from ..resources import functions as function
from ..resources import variables as var
from ..filesystem.Directory import Directory
from ..filesystem.File import File
from . import commands

class Interpreter:
    def __init__(self):
        # Contains the head of the filesystem
        self.headDir = Directory("/")
        # Contains reference to current workingDir
        self.workingDir = self.headDir
        # List that contains a tree of dirs, 0 being head [-1] being current
        self.dirTree = [self.headDir]
        # Contains current command that is being processed
        self.command = ""
        # Contains a list of token of commands
        self.token = []
        # Set reference from workingDir
        var.workingDir = self.workingDir

    # Prompts and takes input, returns exit code
    def prompt(self):
        print(var.ps1, end=" ")
        self.command = input()
        return self.process(self.command)

    # Processes given input and runs command, returns exit code
    def process(self, command=""):
        self.command = command
        if not command:
            var.exit_code = 127
            return 127

        # Save command to var
        var.command = command

        # Process command into token
        token = command.split(" ")
        self.token = command.split(" ")


        # Add command to history
        if len(var.bash_history) == 0 or command != var.bash_history[-1]:
            var.bash_history.append(command)
        
        if len(var.lev_bash_history) == 0 or command != var.lev_bash_history[-1]:
            var.lev_bash_history.append(command)

        # Interchange certain token
        commands.interchange(command)
        command = var.command
        token = command.split(" ")
        self.token = command.split(" ")

        # Check if it is a level command
        if commands.game_process(command):
            var.exit_code = 137
            return 137

        # Check if it's a special command
        if commands.special(command):
            var.exit_code = 20
            return 20

        # Check if it's a banned command
        if commands.is_banned(command):
            var.exit_code = 110
            return 110

        # Run filesystem command
        if self.filesystem(command):
            return var.exit_code

        # Command not found
        var.exit_code = 127
        print("{}: {}: command not found...".format(var.shell, token[0]))
        return 127



    # Contains commands run on Directory
    # Needs to be here to avoid circular import that 'technically' works
    def filesystem(self, command=""):
        verbose = False
        token = self.token

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
                    success = self.workingDir.mkdir(arg)
                    if verbose and success:
                        print("mkdir: created directory '{}'".format(arg))
                var.exit_code = 0
                return True
        
            return False

        # ls command
        elif token[0] == "ls":
            token.pop(0)
            if len(token) == 0:
                self.workingDir.ls()
                var.exit_code = 0
                return True

            elif len(token) == 1:
                self.workingDir.ls(token[0])
                var.exit_code = 0
                return True
            
            elif len(token) > 1:
                first = token.pop(0)
                print("{}:".format(first))
                self.workingDir.ls(first)
                for path in token:
                    print("\n{}:".format(path))
                    self.workingDir.ls(path)
                
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
                self.workingDir.touch(path)
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
                self.workingDir.rm(x, recurse)
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
                self.workingDir.rmdir(x)
            
            var.exit_code = 0
            return True


                
                    

