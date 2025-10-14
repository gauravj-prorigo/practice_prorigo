class Book:
    therory = "Vijay"
    def __init__(self, title, author, year):
        self.title = title
        self.author = author
        self.year = year

    def display_details(self):
        print(f"Title: {self.title}")
        print(f"Author: {self.author}")
        print(f"Year Published: {self.year}")
        
    @classmethod
    def supet_Star(cls):
        print(cls.therory)
        
    def supet_Star(notebook):
        print(notebook.a)

book1 = Book("Shyamchi Aait", "Sane Guruji", 1988)
book2 = Book("Yayati", "V. S. Khandeka", 1959)
book3 = Book("Mrutyunjay", "Shivaji Sawant", 1967)

book1.display_details()
print()
book2.display_details()
print()
book3.display_details()
book3.supet_Star()



class notbook:
    a = 10
    b = 20