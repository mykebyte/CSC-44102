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
    
    
    



class LibraryManager:
    def __init__(self):
        self.books = []
        self.users = []

