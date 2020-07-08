from .Directory import Directory
# Working directory
class Working:
    def __init__(self, dir=Directory()):
        self.head = Directory # Will contain the top directory
        self.contents = [[]] # Will contain the directories, top level at zero
        self.current = 0 # Contains the index of contents that it's working in
        
        # If it has members then explore the contents and save it
        
        if dir.has_members():
            for i in dir.contents:
                if i.has_members():
