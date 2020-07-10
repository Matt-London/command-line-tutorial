from packages.levels.Level import Level
import packages.levels.levels as Levels
import packages.resources.functions as function
import packages.resources.variables as var
from packages.filesystem.Directory import Directory
from packages.filesystem.File import File


di = Directory("Test")

di.mkdir("one")
di.mkdir("two")

di.get_sub("one").mkdir("three")

di.get_sub("one/three").mkdir("four")

di.ls()
di.get_sub("one").ls()
di.get_sub("one/three").ls()