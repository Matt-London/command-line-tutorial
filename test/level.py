from packages.levels.Level import Level
import packages.levels.levels as Levels
import packages.resources.functions as function
import packages.resources.variables as var
from packages.filesystem.Directory import Directory
from packages.filesystem.File import File


var.bash_history = ("Check")
test = Level("Instruct", "Help", ("Check"))

test.instruct()
test.help()
print(test.check())