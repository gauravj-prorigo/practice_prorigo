class GrandFather:
     def __init__(self,name):
          print("Grandfather specks first",name)
          
class Fathet:
    def __init__(self,fname,gname):
            super().__init__(gname)
            print("father specks Second",fname)
            
class Son(Fathet,GrandFather):
          def __init__(self,sname,fname,gname):
            super().__init__(fname,gname)
            print("son specks at last",sname)  
            
s1 = Son("Gaurav","Saurav","bherav")

# follwing method resolutiin order (MRO)                      