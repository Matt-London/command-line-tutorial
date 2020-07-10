from ..resources.colors import colors
from ..resources import variables as var
from .File import File

class Directory:
    # Basic constructor
    def __init__(self, name=""):
        self.name = name
        self.contents = []
    
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
        if path == "":
            return self
        
        pathSplit = path.split("/")
        nextDir = self.index(pathSplit[0])
        
        pathSplit.pop(0)
        path = "/".join(pathSplit)

        if nextDir >= 0:
            if type(self.contents[nextDir]) == File:
                return self.contents[nextDir]
            return self.contents[nextDir].get_sub(path)
        
        print("get_sub error")

    # Delete file/dir by name:
    def delete(self, path=""):
        ind = -1
        if path:
            pathSplit = path.split("/")
            if len(pathSplit) == 1:
                ind = self.index(pathSplit[0])
                if ind >= 0:
                    self.contents.pop(ind)

            name = pathSplit.pop()
            path = "/".join(pathSplit)
            ind = self.get_sub(path).index(name)
            if ind >= 0:
                self.get_sub(path).contents.pop(ind)


    # ============== Shell Commands ==============

    # List all contents in directory
    def ls(self, path=""):
        destContents = self.get_sub(path).contents
        lenContent = len(self.get_sub(path).contents)

        for content in destContents:
            if type(content) == Directory:
                print(colors.fg.blue + content.name + colors.reset + "\t", end="")
            else:
                print(content.name + "\t", end="")
        if lenContent != 0:
            print()
    
    # Make new dir
    def mkdir(self, path=""):
        if path:
            pathSplit = path.split("/")
            if len(pathSplit) == 1:
                self.add(Directory(pathSplit[0]))

            name = pathSplit.pop()
            path = "/".join(pathSplit)
            self.get_sub(path).add(Directory(name))
    
    # Make new file
    def touch(self, path=""):
        if path:
            pathSplit = path.split("/")
            if len(pathSplit) == 1:
                self.add(File(pathSplit[0]))

            name = pathSplit.pop()
            path = "/".join(pathSplit)
            self.get_sub(path).add(File(name))
    
    # Deletes a file
    def rm(self, path=""):
        if path:
            if type(self.get_sub(path)) == File:
                self.delete(path)
            elif type(self.get_sub(path)) == Directory:
                print("rm error, fed directory")
            else:
                print("rm error, Thing doesn't exist")

    # Deletes a directory
    def rmdir(self, path=""):
        if path:
            if type(self.get_sub(path)) == Directory:
                self.delete(path)
            elif type(self.get_sub(path)) == File:
                print("rm error, fed File")
            else:
                print("rm error, Thing doesn't exist")