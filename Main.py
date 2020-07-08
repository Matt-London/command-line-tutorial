from packages.levels.Level import Level
import packages.levels.levels as Levels
import packages.resources.functions as function
import packages.resources.variables as var
from packages.filesystem.Directory import Directory
from packages.filesystem.File import File


di = Directory("Test")
di.mkdir("ls")
di.mkdir("lsg")

sub = di.contents[0]
sub.mkdir("Test2")

di.ls()
