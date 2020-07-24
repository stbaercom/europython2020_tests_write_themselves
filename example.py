import os

import checker

class MyTestClass:
    def __init__(self):
        self.a = "Hello"
        self.b = 1
        self.c = 2.33433
        self.d = [1, 2.3333, 3.3332]
        self.e = "2020-05-12"

test_data = MyTestClass()
changed_test_data = MyTestClass()
changed_test_data.d.pop()
changed_test_data.c += 0.5


checker = checker.Checker(os.path.dirname(__file__))


assert checker.check(test_data, "name1")
assert checker.check(test_data, "name1")

assert checker.check(test_data, "name2")
assert checker.check(changed_test_data, "name2")

checker.list()

checker.review("name2")

checker.approve("name2")



