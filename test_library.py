from library_core import *

lib = LibraryManager()

user = User("1","a","j@email.com")
book = Book("123", "pyth", "fds sd", "dsfs", 1242, 2)

lib.create_user(user)
lib.add_book(book)

old_copies = book.avaliable_copies
result = lib.borrow_book(user, book)


assert book.avaliable_copies == old_copies - 1
assert result[0] is True
assert book.avaliable_copies == old_copies


print("Borrow test passed!")