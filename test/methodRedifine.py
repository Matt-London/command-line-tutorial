# A test to see if you can redefine a method
# SPOILER: You can't
class Test:
    def print(self):
        print("Fail")

test1 = Test()
test1.print()
def test1.print(self):
    print("Pass")

test1.print()