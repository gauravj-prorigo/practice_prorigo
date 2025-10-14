class GrandFather:
    def __init__(self):
        print("GrandFather constructor")

class Father(GrandFather):
    def __init__(self):
        super().__init__()           # call GrandFather constructor
        print("Father constructor")

class Son(Father):
    def __init__(self):
        super().__init__()           # call Father constructor
        print("Son constructor")

s1 = Son()
