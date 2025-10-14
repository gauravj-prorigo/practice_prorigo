class Human:
    def talk(self):
        print("Human is only livung-thing that can talk...")
        
    def brain(self):
        print("big brain")    
        
class Male:
    def walk(self):
        print("Human is one of  livung-thing that can walk on 2 leg...")  
        
    def brain(self):
        print("Size of brain is incessing with your body")      
        
class Boy(Human,Male):
    pass

b = Boy()
b.talk()
b.walk() 
Male.brain(b)          