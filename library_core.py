# Following the PEP8 style guidfe, all my classes will use pascalCase, constants will use UPPER_CASE, the rest snake_case


# Initilise the Book class, given it key detials such as ISBN, title, author, genre, year, total_copies
# For example. self.title daves the genre into the the object, allowing it to be used later


class Book:
    def __init__(self, ISBN, title, author, genre, year, total_copies):
        self.ISBN = ISBN
        self.title = title
        self.author = author
        self.genre = genre
        self.year = year
        self.total_copies = total_copies

        

    def check_avaliability(self):
        return self.total_copies > 0
        # checks to see if teh book if avaliable (quantity > 0)
        # added self so it checks the specific books copies
    
    def update_quantity(self, total_copies):
        self.total_copies += total_copies
        # update total copies of the book, after every borrow or return
    
    def show_book_info(self):
        print(f"ID: {self.ISBN}, title: {self.title}, Author: {self.author}, Genre {self.genre}, year {self.year}, total_copies {self.total_copies}")

    



class LibraryManager:
    def __init__(self):
        self.books = []
        self.users = []

