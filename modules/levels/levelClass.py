# The template of all levels
class Level:
    # Basic constructor
    def __init__(self, instruct="", help="", check=()):
        self.instruct = instruct
        self.help = help
        self.check = check
    
    # Check if a Level is 'real'
    def has_members(self):
        # Declare some bools
        # True if each exists
        binstruct = False
        bhelp = False
        bcheck = False

        # Define the bools
        binstruct = self.instruct != ""
        bhelp = self.help != ""
        if self.check:
            bcheck = True

        return binstruct and bhelp and bcheck
    
    # Print out the instruct info
    def instruct(self):
        print(self.instruct)
    
    # Print out help info
    def help(self):
        print(self.help)

    # Returns true or false if a check is successful
    def check(self):
        pass

        