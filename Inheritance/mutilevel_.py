class GrandFather:
     def __init__(self,snmae):
          self.age = 18
          print("Grandfather specks first",snmae)
          
class Fathet(GrandFather):
    
    def __init__(self,name,sname):
        print(name)
        super().__init__(sname)

    def peop(self):
        print("in charm")
            
class Son(Fathet):
    def __init__(self, name, sname):
        super().__init__(name, sname)
    
         
s1 = Son("Gaurav","Jadhav")
print(s1.age)

# follwing method resolutiin order (MRO)                      