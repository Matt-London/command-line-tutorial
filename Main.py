from packages.levels.Level import Level
import packages.levels.levels as Levels
import packages.resources.functions as function
import packages.resources.variables as var
from packages.filesystem.Directory import Directory
from packages.filesystem.File import File
# from packages.parser.interpreter import Interpreter

folder = Directory("/")
# interpreter = Interpreter(folder)

while True:
    try:
        print(var.ps1, end=" ")
        command = str(input()).split(" ")
        base = command.pop(0)
        if base == "ls":
            command.append("")
            folder.ls(command[0])
        elif base == "touch":
            folder.touch(command[0])
        elif base == "mkdir":
            folder.mkdir(command[0])
        elif base == "mv":
            command.append("")
            folder.mv(command[0], command[1])
        elif base == "rm":
            recurser = "-r" in command
            recurserf = "-rf" in command
            recurse = recurser or recurserf

            # Remove the -r or -rf flag
            if recurse:
                if recurser:
                    command.remove("-r")
                if recurserf:
                    command.remove("-rf")


            folder.rm(command[0], recurse)
        elif base == "rmdir":
            folder.rmdir(command[0])
        # elif base == "cd":


        elif base == "exit":
            break
        
    except KeyboardInterrupt:
        print()
        continue