from levels.Level import Level
import levels.levels as Levels
import resources.functions as function
import resources.variables as var
from filesystem.Directory import Directory
from filesystem.File import File


di = Directory("Test")
di.add(Directory("Banana"))
di.add(File("Test"))
di.get("Test").append("Hello World!")

print(di.get("Test").read())

di.ls()
