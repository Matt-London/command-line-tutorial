from packages.levels.Level import Level
import packages.levels.levels as Levels
import packages.resources.functions as function
import packages.resources.variables as var
from packages.filesystem.Directory import Directory
from packages.filesystem.File import File
from packages.parser.Interpreter import Interpreter

interpreter = Interpreter()

while True:
    try:
        interpreter.prompt()
        
    except KeyboardInterrupt:
        print()
        var.exit_code = 130
        continue