from packages.levels.Level import Level
import packages.levels.levels as Levels
import packages.resources.functions as function
import packages.resources.variables as var
from packages.filesystem.Directory import Directory
from packages.filesystem.File import File


di = Directory("Test")
di.add(Directory("Banana"))
di.add(File("Test"))
di.get("Test").append("Hello World!")

print(di.get("Test").read())

di.ls()
