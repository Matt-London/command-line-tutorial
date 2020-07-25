from packages.levels.Level import Level
import packages.levels.levels as Levels
import packages.resources.functions as function
import packages.resources.variables as var
from packages.filesystem.Directory import Directory
from packages.filesystem.File import File
from packages.parser.Interpreter import Interpreter

interpreter = Interpreter()

# Put test dir in interpreter
interpreter.process("mkdir cdTest")
interpreter.process("touch cdTest/greatWork")
interpreter.process("mkdir mvTest")
interpreter.process("touch mvTest/from")


# Clear out these entered commands
var.lev_bash_history.clear()
var.bash_history.clear()


while True:
    try:
        interpreter.prompt()
        
    except KeyboardInterrupt:
        print()
        var.exit_code = 130
        continue