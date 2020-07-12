from packages.levels.Level import Level
import packages.levels.levels as Levels
import packages.resources.functions as function
import packages.resources.variables as var
from packages.filesystem.Directory import Directory
from packages.filesystem.File import File
from packages.parser.interpreter import Interpreter

dir = Directory("test")

dir.mkdir("gg")

dir.mkdir("gg/test")

dir.ls("gg")
dir.ls("ggg")