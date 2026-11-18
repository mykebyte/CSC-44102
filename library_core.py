from datetime import date
from datetime import timedelta

# Following the PEP8 style guidfe, all my classes will use pascalCase, constants will use UPPER_CASE, the rest snake_case


# Initilise the Book class, given it key detials such as ISBN, title, author, genre, year, total_copies
# For example. self.title daves the genre into the the object, allowing it to be used later


class Book:
    def __init__(self, ISBN, title, author, genre, year, total_copies):
        if not ISBN or not title or not author:
            raise ValueError("ERROR: - ISBB, title and author required")
        
        if not isinstance(total_copies, int) or isinstance(total_copies, bool) or total_copies < 0:
            raise ValueError("ERROR: Total copies be non-negative")

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

        # return self.avaliable_copies > 0 
    
        if not isinstance(amount, int) or isinstance(amount, bool):
            return False

        currently_borrowed = self.total_copies - self.avaliable_copies
        new_total = self.total_copies + amount

        if new_total < currently_borrowed:
            return False
        
        if new_total < 0:
            return False

        self.total_copies = new_total
        self.avaliable_copies = self.total_copies - currently_borrowed

        return True


    def show_book_info(self):
        return(f"ID: {self.ISBN}, title: {self.title}, Author: {self.author}, Genre {self.genre}, year {self.year}, total_copies {self.total_copies}")

class User:
    MAX_LOANS = 3

    def __init__(self, member_id, name, email):

        if not member_id or not name or not email:
            raise ValueError("ERROR: memmerb id, or name or email is required")
        
        if "@" not in email or "." not in email:
            raise ValueError("enter email")

        self.member_id = member_id
        self.name = name
        self.email = email

        self.loans = []

    def active_loan_count(self):
        count = 0

        for loan in self.loans:
            if loan.is_active:
                count += 1
        return count

    def show_user_info(self):
        return self.member_id, self.name, self.email 



class Loan:
    LOAN_PERIOD = 14
    MAX_RENEWALS = 1


    def __init__(self, user, book):
        self.user = user
        self.book = book
        self.loan_date = date.today() # find when the book as actually borrowed
        self.due_date = self.loan_date + timedelta(days=self.LOAN_PERIOD) #fiond due date
        self.renewals = 0
        self.is_active = True 

    def check_overdue(self): # done
        if self.is_active and date.today() > self.due_date:
            return True
        return False 
    
    def renew_loan(self): #renewal logic
        if not self.is_active:
            return False, "Loan is not active"

        if self.renewals >= self.MAX_RENEWALS:
            return False, "Maximum renewals reached"
        

        if self.check_overdue():
            return False, "Overdue book cannot be renewed"

        self.due_date += timedelta(days = self.LOAN_PERIOD)

        self.renewals +=1

        return True, "Loan renewed successfully"

    def return_loan(self): # return logic
        if not self.is_active: #sotyp it being returned more than once
            return False, "Loan has already been returned"

        self.is_active = False #inmactive bc its been reutrned
        
        self.book.avaliable_copies += 1

        return True, "Book returned succesffully"




class LibraryManager:
    def __init__(self):
        self.books = []
        self.users = []
        self.loans = []

    def create_user(self, new_user):
    # Check if new user doesnt correlate with old user, checks the user isbn and works from there
        if any(current_user.member_id == new_user.member_id for current_user in self.users):
            
            return False, "User exists alreaady"
        
        self.users.append(new_user)
        return True, "User addedd successfully"

    def search_book(self, title):

        if not isinstance(title, str):
            return False, "Wrong Format"
        

        found_books = []

        for book in self.books:
            if title.lower() in book.title.lower():
                found_books.append(book)
        
        return found_books
    
                # reveiver poitned out an important issue, with my old code, is the isbn didnt exist, python wouldve skipped the enitre if block, and the method would've reached the end without the book being added
    def add_book(self, new_book):
        if any(book.ISBN == new_book.ISBN for book in self.books): # basically search is a book already exists
            return False
        
        self.books.append(new_book)
        return True
    
    def search_user(self, member_id):
       for user in self.users:
           if user.member_id == member_id:
               return user


    
    def remove_book(self, ISBN):
        for book in self.books:
            if book.ISBN == ISBN:

                if book.avaliable_copies != book.total_copies:
                    return False, "Can't remove book because its borrowed"
                
                self.books.remove(book)

                return True

        return False
    
    def borrow_book(self, user, book):

        if user not in self.users: # see if user exits
            return False, "User doesn't exist"
        
        if book not in self.books: #see if book exists
                return False, "Book doesn't exist"
        
        if not book.check_avaliability():
            return False, "Book not avaliable"
        
        if user.active_loan_count() >= User.MAX_LOANS:
            return False, "Maximum loans reached"
        
        new_loan = Loan(user, book)
        book.avaliable_copies -= 1

        user.loans.append(new_loan)
        self.loans.append(new_loan)
        
        return True, "Book borrowed successfully"
    
    def return_book(self, loan):

        if loan not in self.loans:
            return False, "Loan does not exist"
        return loan.return_loan()
        
    def renew_loan(self, loan):
        if loan not in self.loans:
            return False, "Loan doesn't exist"

        return loan.return_loan()
        

 
    

    def show_all_books(self): #thought this would be nice, to show all books
        if not self.books:
            found_books = []

            for book in self.books:
                found_books.append(book.show_book_info())

            return found_books

    def show_all_user(self):
        if not self.users:
            return("no users")
        
        return [user.show_user_info() for user in self.users]
    
