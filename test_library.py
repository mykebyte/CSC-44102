from library_core import *

lib = LibraryManager()

user = User("1","a","j@email.com")
book = Book("123", "pyth", "fds sd", "dsfs", 1242, 2)

lib.create_user(user)
lib.add_book(book)

result = lib.borrow_book(user, book)

assert result == (True, "Book borrowed successfully")
assert book.avaliable_copies == 1

print("Borrow test passed!")