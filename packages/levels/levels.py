from .Level import Level

one = Level("There's a directory called 'test' within your current working path\nOpen this directory (CHANGE your DIRECTORY to 'this')\nThen please print your current working directory to show that you have changed your directory", "You may use the 'cd' command to open a directory\nType 'cd' followed by the name of the directory to open\nYou may type 'pwd' to PRINT your WORKING DIRECTORY", ("cd test", "pwd"))

levels = [one]