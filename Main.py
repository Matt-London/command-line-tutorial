from packages.levels.Level import Level
import packages.levels.levels as Levels
import packages.resources.functions as function
import packages.resources.variables as var
from packages.filesystem.Directory import Directory
from packages.filesystem.File import File
from packages.parser.interpreter import Interpreter

globals()["callable"] = None

folder = Directory("/")
interpreter = Interpreter(folder)

for i in range(10):
    folder.add(File("file_" + str(i)))
    folder.add(Directory("directory_" + str(i)))

while True:
    print(var.ps1, end=" ")
    while not interpreter.interpret(input()):
        print(">", end=" ")

    print("Exit code " + str(interpreter.get_return_code()))
