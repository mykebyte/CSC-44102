# GenAI acknowledgement:
# I acknowledge the use of ChatGPT (version ___, OpenAI, https://chatgpt.com/)
# and Claude (Claude Opus 5.5, Anthropic, https://claude.ai/) to review a
# draft of my work and provide feedback.

from datetime import date
from datetime import timedelta
from datetime import date, timedelta

# Following the PEP8 style guidfe, all my classes will use pascalCase, constants will use UPPER_CASE, the rest snake_case


# Initilise the Book class, given it key detials such as ISBN, title, author, genre, year, total_copies
# For example. self.title daves the genre into the the object, allowing it to be used later


class Book:
    """represents the book + manages its available and total copies."""

    def __init__(self, ISBN, title, author, genre, year, total_copies):
        """Initialises the book with its details and copy quantities."""
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
        """Checks if the book has any available copies."""
        return self.avaliable_copies > 0
        # checks to see if teh book if avaliable (quantity > 0)
        # added self so it checks the specific books copies
    
    def update_quantity(self, amount):
        """Updates the total copies making sure they're not reduced below borrowed copies
           returns: [success, message].
        """
        # to prevent reducing totla copies below teh actual number of borrwed books

        # return self.avaliable_copies > 0 
    
        if not isinstance(amount, int) or isinstance(amount, bool):
            return False, "Needs to be a whole number"

        currently_borrowed = self.total_copies - self.avaliable_copies
        new_total = self.total_copies + amount

        if new_total < 0:
            return False, "Total copies cannot be negative"

        if new_total < currently_borrowed:
            return False, "cant remove copies that are borrowed"
        
        

        self.total_copies = new_total
        self.avaliable_copies = self.total_copies - currently_borrowed

        return True, "Quantity successfully updated"


    def show_book_info(self):
        """returns the book's details as a formatted string."""
        return(f"ID: {self.ISBN}, title: {self.title}, Author: {self.author}, Genre {self.genre}, year {self.year}, total_copies {self.total_copies}")

class User:
    """represents the library member + stores their loans."""
    MAX_LOANS = 3

    def __init__(self, member_id, name, email):
        """Initialises the specifrc member using their ID, name and email

        and raises a ValueError if the required details /email validation fail.
        """
        if not member_id or not name or not email:
            raise ValueError("ERROR: memmerb id, or name or email is required")
        
        if "@" not in email or "." not in email:
            raise ValueError("enter email")

        self.member_id = str(member_id)
        self.name = name
        self.email = email

        self.loans = []

    def active_loan_count(self):
        """Returns number of currently active loans which belongs to each member."""
        count = 0

        for loan in self.loans:
            if loan.is_active:
                count += 1
        return count

    def show_user_info(self):
        """Returns member's ID, name and email."""
        return self.member_id, self.name, self.email 

class Loan:
    """Represents the book loan and manages its return and renewal."""
    LOAN_PERIOD = 14
    MAX_RENEWALS = 1


    def __init__(self, user, book):
        """Creates the loan with a borrowing date and a 14day expiry"""
        self.user = user
        self.book = book
        self.loan_date = date.today() # find when the book as actually borrowed
        self.due_date = self.loan_date + timedelta(days=self.LOAN_PERIOD) #fiond due date
        self.renewals = 0
        self.is_active = True 

    def check_overdue(self): 
        """Checks if a active loan is passed its due date."""
        if self.is_active and date.today() > self.due_date:
            return True
        return False 
    
    def renew_loan(self): 
        """Renews an active loan by 14 days if renewal rules allow.

        Returns [success, message]
        Only a single renewal is allowed, 
        Overdue loans cannot be renewed.
        """
        if not self.is_active:
            return False, "Loan is not active"

        if self.renewals >= self.MAX_RENEWALS:
            return False, "Maximum renewals reached"
        

        if self.check_overdue():
            return False, "Overdue book cannot be renewed"

        self.due_date += timedelta(days = self.LOAN_PERIOD)

        self.renewals +=1

        return True, "Loan renewed successfully"

    def return_loan(self): 
        """returns the active loan, also increasing the books avaliable copies.

        Returns (success, message)
        Prevents the same loan from being returned twice.
        """
        if not self.is_active: #sotyp it being returned more than once
            return False, "Loan has already been returned"

        self.is_active = False #inmactive bc its been reutrned
        
        self.book.avaliable_copies += 1

        return True, "Book returned succesffully"


class LibraryManager:
    """Manages the library's: books, members and loans."""
    def __init__(self):
        """initialises the: empty book, member and loan collections."""
        self.books = []
        self.users = []
        self.loans = []
        self.next_member_no = 1

    def create_user(self, name, email):
        """creates a new member with  automatically generated id

        Returns: [success, message, user], or None for the user if the case if the creation fails.
        ID counter would only increase after the reg was successsful.
        """

        
        member_id = f"M{self.next_member_no:03d}"       


        try:
            new_user = User(member_id, name, email)

        except ValueError as error:
            return False, str(error), None # try exscept, if validationf ails, 

        self.users.append(new_user)
        self.next_member_no += 1

        return True, "User addedd successfully", new_user

    def search_book(self, title):
        """finds books whose titles contain the supplied search text

        returns: a list of matching books.
        """
        found_books = []

        if not isinstance(title, str):
            return found_books
 
        for book in self.books:
            if title.lower() in book.title.lower():
                found_books.append(book)
        
        return found_books
    
                # reveiver poitned out an important issue, with my old code, is the isbn didnt exist, python wouldve skipped the enitre if block, and the method would've reached the end without the book being added
    def add_book(self, new_book):
        """adds the book if its ISBN isnt already registered

        Returns [success, message]
        """
        if any(book.ISBN == new_book.ISBN for book in self.books): # basically search is a book already exists
            return False, "Book already exists"
        
        self.books.append(new_book)
        return True, "Book added successfully"
    
    def search_user(self, member_id):
        """ find a member using their ID, returns None if not found."""
        member_id = str(member_id)

        for user in self.users:
            if user.member_id == member_id:
                return user
                   
        return None # Added didnce hte method searches for a yuserm so either return no usr or none


    
    def remove_book(self, ISBN):
        """removes the book if it has no outstanding borrowed copies

        Returns (success, message)
        """
        for book in self.books:
            if book.ISBN == ISBN:

                if book.avaliable_copies != book.total_copies:
                    return False, "Can't remove book because its borrowed"
                
                self.books.remove(book)

                return True, "Book succesfully removed"

        return False, "Book no exists"
    
    def borrow_book(self, user, book):
        """creates a loan if the member and book are valid

        Returns (success, message).
        Also, a member cannot exceed three active loans, and the book must be available.
        """

        if user not in self.users: # see if user exits
            return False, "User doesn't exist", None
        
        if book not in self.books: #see if book exists
            return False, "Book doesn't exist", None
        
        if not book.check_avaliability():
            return False, "Book not avaliable", None
        
        if user.active_loan_count() >= User.MAX_LOANS:
            return False, "Maximum loans reached", None
        
        new_loan = Loan(user, book)
        book.avaliable_copies -= 1

        user.loans.append(new_loan)
        self.loans.append(new_loan)
        
        return True, "Book borrowed successfully", new_loan
    
    def find_active_loan(self, member_id, ISBN):
        """
        finds an active loan using a member ID+ISBN
        returns;:loan object, else None
        """

        user = self.search_user(member_id)

        if user is None:
            return None
        
        for loan in user.loans: #loop through loans and confirm if isbn exists or not
            if loan.book.ISBN == ISBN and loan.is_active:
                return loan
            
        return None

    def get_user_loans(self, member_id):
        """
        Returns all loans, including returned loans, belongiong to a member
        returns: empty list, if teh member doesn texist
        """
        user = self.search_user(member_id)

        if user is None: 
            return []
        
        return list(user.loans)

    def get_overdue_loans(self):


        """returns all overdue loans in the style of overdue first
        
        returns a list of loan objects/or empty list if nothing is overdue"""
        overdue_loans = []

        for loan in self.loans:
            if loan.check_overdue():
                overdue_loans.append(loan)

        overdue_loans.sort(key=lambda loan: loan.due_date)
        return overdue_loans

    

    def return_book(self, loan):
        """returns a loan 

        Returns (success, message).
        """

        if loan not in self.loans:
            return False, "Loan does not exist"
        return loan.return_loan()
        
    def renew_loan(self, loan):
        """Renews a loan belonging to the library under its renewal rules.

        Returns (success, message).
        """
        if loan not in self.loans:
            return False, "Loan doesn't exist"

        return loan.renew_loan()
        

 
    

    def show_all_books(self):
            """Returns in proper formatting all of the books in the library"""
            found_books = []

            for book in self.books:
                found_books.append(book.show_book_info())

            return found_books

    def show_all_user(self):
        """returns the details of all the registered library members"""
        found_users = []

        for user in self.users:
            found_users.append(user.show_user_info())

        return found_users


