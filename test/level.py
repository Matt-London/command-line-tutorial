from modules.levels.Level import Level
import modules.levels.levels as Levels
import modules.resources.functions as function
import modules.resources.variables as var


var.bash_history = ("Check")
test = Level("Instruct", "Help", ("Check"))

test.instruct()
test.help()
print(test.check())