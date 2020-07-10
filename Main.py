from packages.levels.Level import Level
import packages.levels.levels as Levels
import packages.resources.functions as function
import packages.resources.variables as var
from packages.filesystem.Directory import Directory
from packages.filesystem.File import File


di = Directory("Test")

di.mkdir("one")
di.mkdir("one/three")
di.touch("one/three/four")

di.ls("one/three")

di.rm("one/three/four")

di.ls("one/three")

di.ls()