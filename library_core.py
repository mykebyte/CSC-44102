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

        self.avaliable_copies = total_copies

    def check_avaliability(self):
        return self.avaliable_copies > 0
        # checks to see if teh book if avaliable (quantity > 0)
        # added self so it checks the specific books copies
    
    def update_quantity(self, amount):
        # to prevent reducing totla copies below teh actual number of borrwed books

        currently_borrowed = self.total_copies - self.avaliable_copies
        new_total = self.total_copies + amount


        # update total copies of the book, after every borrow or return
        if new_total < 0 or new_total < currently_borrowed:
            print("ERROR: Total copies cannot fall below 0")
            return False

        self.total_copies = new_total
        self.avaliable_copies = self.total_copies - currently_borrowed

        return True


    def show_book_info(self):
        return(f"ID: {self.ISBN}, title: {self.title}, Author: {self.author}, Genre {self.genre}, year {self.year}, total_copies {self.total_copies}")

    



class LibraryManager:
    def __init__(self):
        self.books = []
        self.users = []

    def create_user(self, new_user):
    # Check if new user doesnt correlate with old user, checks the user isbn and works from there
        if any(current_user.ISBN == new_user.ISBN for current_user in self.users):
            print("ERROR: User already exists, new ID required")
            return
        self.users.append(new_user)
        print(f"USER {new_user.name} added successfully.")


    def search_book(self, title):
        found_books = []

        for book in self.books:
            if title.lower() in book.title.lower():
                found_books.append(book)
        
        return found_book