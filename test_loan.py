
from library_core import *

lib = LibraryManager()

user = User("1","a","j@email.com")
book = Book("123", "pyth", "fds sd", "dsfs", 1242, 2)

lib.create_user(user)
lib.add_book(book)

loan = Loan(User, book)
book.avaliable_copies -=1
lib.loans.append(loan)

print("Return:", lib.return_book(loan))

print("Return again:", lib.return_book(loan))

print("renew cant:", lib.renew_loan(loan))
