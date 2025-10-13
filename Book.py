class Book:
    def __init__(self,title,author,year):
        self.title = title
        self.author = author
        self.year = year
    
    def info(self):
        print(f"The title of book is {self.title} and it is written by {self.author} in {self.year}")
        
    def sp_info(self):
        return self.year>2003
    
    
b1 = Book("Sham chi aai","Gaurav Jadhav",2004)

b1.info()
print("its is classic : ",b1.sp_info())
                