class A:
    def __init__(self):
        print("Class A constructor")
        
    def display(Self):
        print("Display in A")    

class B(A):
    def __init__(self):
        print("Class B constructor")
    # def display(Self):
    #     print("Display in B")    
        
class C(A):
    def __init__(self):
        print("Class C constructor")
    # def display(Self):
    #         print("Display in C")    


class D(B, C):
    def __init__(self):
        print("Class D constructor")

d1 = D()
d1.display()