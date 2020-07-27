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

# Check if colors should be disabled
print("Is the following text readable?")
print(var.ps1)
readable = str(input("Type y for yes and n for no:"))
if readable != "y":
    var.colorPrompt = False



while True:
    try:
        interpreter.prompt()
        
    except KeyboardInterrupt:
        print()
        var.exit_code = 130
        continue