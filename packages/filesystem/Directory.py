from ..resources.colors import colors
from ..resources import variables as var
from .File import File

class Directory:
    # Basic constructor
    def __init__(self, name="", container=None):
        self.name = name
        self.contents = []
        self.container = container
    
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

        # Check if it's ../
        if pathSplit[0] == "..":
            pathSplit.pop(0)
            path = "/".join(pathSplit)
            if self.container == None:
                return self.get_sub(path)
            else:
                return self.container.get_sub(path)
        
        # Check if it's ./
        if pathSplit[0] == ".":
            pathSplit.pop(0)
            path = "/".join(pathSplit)
            return self.get_sub(path)

        if nextDir < 0:
            return False
        
        pathSplit.pop(0)
        path = "/".join(pathSplit)

        if nextDir >= 0:
            if type(self.contents[nextDir]) == File:
                return self.contents[nextDir]
            return self.contents[nextDir].get_sub(path)
        
        # print("get_sub error")
    
    # Returns a string which is the path from this directory to the top
    def get_path(self):
        if self.container == None:
            return self.name
        
        return self.container.get_path() + "/" + self.name

    # Like get_sub but it gives container
    def get_container(self, path=""):
        toR = self.get_sub("/".join(path.split("/")[:-1]))
        if toR == False:
            return self
        return toR

        

    # Delete file/dir by name:
    def delete(self, path=""):
        ind = -1
        if path:
            pathSplit = path.split("/")
            if len(pathSplit) == 1:
                ind = self.index(pathSplit[0])
                if ind >= 0:
                    self.contents.pop(ind)
                    return True


            name = pathSplit.pop()
            path = "/".join(pathSplit)
            ind = self.get_sub(path).index(name)
            if ind >= 0:
                self.get_sub(path).contents.pop(ind)
                return True
        return False
    
    # Copies everything to here
    def copy_from(self, dir, name=""):
        if not name:
            self.name = dir.name
        else:
            self.name = name
        self.contents = dir.contents

        


    # ============== Shell Commands ==============

    # List all contents in directory
    def ls(self, path=""):
        if not self.get_sub(path):
            print("ls: cannot access '{}': No such file or directory".format(path))
            return False
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
            # Check if the name already exists
            if self.get_sub(path):
                print("mkdir: cannot create directory '{}': File exists".format(path))
                return False
            pathSplit = path.split("/")
            if len(pathSplit) == 1:
                self.add(Directory(pathSplit[0], self))
                return True

            name = pathSplit.pop()
            path = "/".join(pathSplit)
            self.get_sub(path).add(Directory(name, self.get_sub(path)))
            return True
        return False
    
    # Rename/move anything
    def mv(self, orig="", final=""):
        # Print error for no operands
        if not orig and not final:
            print("mv: missing file operand")
            var.exit_code = 1
            return False
        # Print error for one arg
        if not final:
            print("mv: missing destination file operand after '{}'".format(orig))
            var.exit_code = 1
            return False
        
        if not self.get_sub(orig):
            print("mv: cannot stat '{}': No such file or directory".format(orig))
            var.exit_code = 1
            return False

        # Check if we're moving a file or dir
        if self.get_sub(final):
            # Save from and to objects
            fromf = self.get_sub(orig)
            tof = self.get_sub(final)

            if type(tof) == File:
                print("mv: destination '{}' exists".format(final))
                var.exit_code = 1
                return False
            elif type(tof) == Directory:
                # Move if dir
                if type(fromf) == Directory:
                    tof.mkdir(fromf.name)
                    tof.copy_from(fromf, "temp")
                    newName = fromf.name
                    self.delete(orig)
                    self.get_sub(final + "/temp").name = newName
                    var.exit_code = 0
                    return True
                # Move if file
                elif type(self.get_sub(orig)) == File:
                    tof.touch("temp")
                    self.get_sub(final + "/temp").copy_from(fromf, "temp")
                    newName = self.get_sub(orig).name
                    self.delete(orig)
                    self.get_sub(final + "/temp").name = newName
                    var.exit_code = 0
                    return True
        # Check if looking for a move and a rename
        elif type(self.get_container(final)) == Directory:
            finalS = final.split("/")
            name = finalS.pop(-1)

            # Move if dir
            if type(self.get_sub(orig)) == Directory:
                self.get_container(final).mkdir(name)
                self.get_container(final).copy_from(self.get_sub(orig), "temp")
                self.delete(orig)
                if len(finalS) >= 1:
                    self.get_sub("/".join(finalS) + "/temp").name = name
                else:
                    self.get_sub("temp").name = name
                var.exit_code = 0
                return True
            # Move if file
            elif type(self.get_sub(orig)) == File:
                self.get_sub(final).touch(name)
                self.get_sub(final).copy_from(self.get_sub(orig), "temp")
                self.delete(orig)
                self.get_sub(final + "/temp").name = name
                var.exit_code = 0
                return True
                
        if type(self.get_sub(orig)) == Directory:
            self.mkdir(final)
            self.get_sub(final).copy_from(self.get_sub(orig), final.split("/")[len(final.split("/")) - 1])
            self.delete(orig)
            var.exit_code = 0
            return True
        
        elif type(self.get_sub(orig)) == File:
            self.touch(final)
            self.get_sub(final).copy_from(self.get_sub(orig), final.split("/")[len(final.split("/")) - 1])
            self.delete(orig)
            var.exit_code = 0
            return True
        
        else:
            print("MV ERROR")
            var.exit_code = 1
            return False
        return False
    
    # Make new file
    def touch(self, path=""):
        if path:
            pathSplit = path.split("/")
            if len(pathSplit) == 1:
                if self.index(pathSplit[0]) >= 0:
                    return True
                else:
                    self.add(File(pathSplit[0]))
                    return True

            name = pathSplit.pop()
            path = "/".join(pathSplit)
            self.get_sub(path).add(File(name))
    
    # Deletes a file
    def rm(self, path="", recurse=False):
        if path:
            if type(self.get_sub(path)) == File:
                self.delete(path)
                return True
            elif type(self.get_sub(path)) == Directory:
                if recurse:
                    self.delete(path)
                    return True
                print("rm: cannot remove '{}': Is a directory".format(path))
                return False
            else:
                print("rm: cannot remove '{}': No such file or directory".format(path))
                return False

    # Deletes a directory
    def rmdir(self, path=""):
        if path:
            if type(self.get_sub(path)) == Directory:
                # Exit if empty
                if self.get_sub(path).contents:
                    print("rmdir: failed to remove '{}': Directory not empty".format(path))
                    return False
                self.delete(path)
                return True

            elif type(self.get_sub(path)) == File:
                print("rmdir: failed to remove '{}': Not a directory".format(path))
                return False
            else:
                print("rmdir: failed to remove '{}': No such file or directory".format(path))
                return False
        return False
