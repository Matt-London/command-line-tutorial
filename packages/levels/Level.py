from ..resources import functions as function
# The template of all levels
class Level:
    # Basic constructor
    def __init__(self, instruction="", helpMessage="", checkTup=()):
        self.instruction = instruction
        self.helpMessage = helpMessage
        self.checkTup = checkTup
    
    # Check if a Level is 'real'
    def has_members(self):
        # Declare some bools
        # True if each exists
        binstruct = False
        bhelp = False
        bcheck = False

        # Define the bools
        binstruct = self.instruction != ""
        bhelp = self.helpMessage != ""
        bcheck = self.checkTup != ()

        return binstruct and bhelp and bcheck
    
    # Print out the instruct info
    def instruct(self):
        print(self.instruction)
    
    # Print out help info
    def help(self):
        print(self.helpMessage)

    # Returns true or false if a check is successful
    def check(self):
        return function.check(self.checkTup)
        