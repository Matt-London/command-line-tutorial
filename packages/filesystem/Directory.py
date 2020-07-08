from ..resources.colors import colors
from ..resources import variables as var

class Directory:
    # Basic constructor
    def __init__(self, name="", container=None, contents=[]):
        self.name = name
        self.container = container
        self.contents = contents
    
    # grabs index of contents by name
    def index(self, find):
        for i in range(len(self.contents)):
            if self.contents[i].name == find:
                return i
        return -1
    
    # Add something to the container
    def add(self, dirFile):
        # Check for duplicate names
        if self.index(dirFile.name) != -1:
            return False

        self.contents.append(dirFile)
        return True

    # Retrieve something that's in contents
    def get(self, neededName):
        ind = self.index(neededName)
        if ind >= 0:
            return self.contents[ind]

    # Returns true if it has at least one sub directory
    def has_sub(self):
        for content in self.contents:
            if type(content) == Directory:
                return True
        return False
    
    # Iterates through, looks for slashes and goes to subs (recursion, ooooh!)
    def get_sub(self, path=""):
        if not self.has_sub() or path == "":
            return self
        
        pathSplit = path.split("/")
        nextDir = self.index(pathSplit[0])
        
        if nextDir >= 0:
            return self.contents[nextDir]
        
        pathSplit.pop(0)
        path = "/".join(pathSplit)
        return self.get_sub(path)


        
            

    # ============== Shell Commands ==============

    # List all contents in directory
    def ls(self):
        for content in self.contents:
            if type(content) == Directory:
                print(colors.fg.blue + content.name + colors.reset + "\t", end="")
            else:
                print(content.name + "\t", end="")
        print()

    # Delete file by name:
    def rm(self, toDelete):
        ind = self.index(toDelete)
        if ind >= 0:
            self.contents.pop(ind)
            return True
        else:
            return False
    
    # Make new dir
    def mkdir(self, name=""):
        if name:
            self.add(Directory(name))
            
        
