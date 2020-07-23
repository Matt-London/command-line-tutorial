# SOURCE: https://www.quora.com/How-can-I-take-multiline-input-from-a-user-and-assign-it-to-a-single-variable-in-Python

import sys
print("Enter the data")
data = sys.stdin.read()   # Use Ctrl d to stop the input
print(data)
