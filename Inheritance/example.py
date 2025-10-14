class Animal:
    
    def __init__(self,name):
         self.a =10
         self.b =20
         self.name = name
    
    
    def ani(self):
        print("the can't speack!")
        
class Dog(Animal):
    def __init__(self,name):
         super().__init__(name)
         self.c =110
         self.d =220
    
    def doj(self):
          print("the can bark !")  
          
    def dis(self):
        print(self.name , self.a)       
          
          
D = Dog("GAurav")  
D.dis()        
# D.ani()
# D.doj()
# print(D.a)
# print(D.b)
# print(D.c)
# print(D.d)