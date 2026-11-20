
from library_core import *

lib = LibraryManager()

book = Book("123", "pyth", "fds sd", "dsfs", 1242, 2)

success, message, user1 = lib.create_user("a", "j@e.com" )


success, message, new_user = lib.create_user("a","a@e.com")

if success: 
    print(message)
    print("id: ", new_user.member_id)
else:
    print("message")

lib.add_book(book)

# let the manager generate the change instead of the user

loan = Loan(user1, book)
book.avaliable_copies -=1
lib.loans.append(loan)

print("Return:", lib.return_book(loan))

print("Return again:", lib.return_book(loan))

print("renew cant:", lib.renew_loan(loan))
