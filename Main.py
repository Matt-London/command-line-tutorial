from packages.levels.Level import Level
import packages.levels.levels as Levels
import packages.resources.functions as function
import packages.resources.variables as var
from packages.filesystem.Directory import Directory
from packages.filesystem.File import File
from packages.parser.interpreter import Interpreter

folder = Directory("/")
interpreter = Interpreter(folder)

for i in range(10):
    folder.add(File("file_" + str(i)))

cmds = ["ls", "ls -a 'a b ca' \"banana bread'\"", "ls -a '", "ls -a '", "rgoajgiuehgetyhgiuethgyu"]

for cmd in cmds:
    if interpreter.interpret(cmd):
        print("Returned with exit code " + str(interpreter.get_return_code()))