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
        var.wd = self.workingDir.get_path()[1::]
        ps1 = ""

        if var.colorPrompt:
            ps1 = colors.fg.lightblue + var.username + colors.fg.darkgrey + "@" + colors.fg.red + var.hostname + colors.fg.lightcyan + ":" + colors.fg.cyan + "[~" + var.wd + "] " + colors.fg.black + "> " + colors.fg.pink + "$#  "[var.isRoot] + colors.reset # Sets PS1
        else:
            ps1 = var.username + "@" + var.hostname + ":" + "[~" + var.wd + "] " + "> " + "$#  "[var.isRoot] # Sets PS1

        print(ps1, end=" ")
        self.command = str(input())
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

        # Save vars to var
        var.token = self.token
        var.headDir = self.headDir
        var.workingDir = self.workingDir

        # Check if it is a level command
        if commands.game_process(command):
            var.exit_code = 137
            return 137

        # Check if it's a special command
        if commands.special(command):
            return var.exit_code

        # Check if it's a banned command
        if commands.is_banned(command):
            var.exit_code = 110
            return 110

        # Run filesystem command
        if commands.filesystem(command):
            # Save var to current vars
            self.token = var.token
            self.headDir = var.headDir
            self.workingDir = var.workingDir
            return var.exit_code

        # Save var to current vars
        self.token = var.token
        self.headDir = var.headDir
        self.workingDir = var.workingDir

        # Command not found
        var.exit_code = 127
        print("{}: {}: command not found...".format(var.shell, token[0]))
        return 127


    


                
                    

