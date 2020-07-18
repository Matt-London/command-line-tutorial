class File:
    # Constructor
    def __init__(self, name="", contents=""):
        self.name = name
        self.contents = contents # Contains a string of the file

    # Append to file's text
    def append(self, text=""):
        self.contents += text
    
    # Overwrites the files's text
    def write(self, text=""):
        self.contents = text

    # Returns the text
    def read(self):
        return self.contents
    
    # Copies everything to here
    def copy_from(self, dir, name=""):
        if not name:
            self.name = dir.name
        else:
            self.name = name
        self.contents = dir.contents

