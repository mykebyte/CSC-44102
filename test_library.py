from library_core import Book, LibraryManager

def test_borrow_book():
    """Checks that borrowing a book actually reduces its available copies."""
    lib = LibraryManager()
    
    success, message, user1 = lib.create_user("a", "a@e.com" )
    book = Book("123", "pyth", "fds sd", "dsds", 1242, 2)

    lib.add_book(book)

    old_copies = book.avaliable_copies
    result = lib.borrow_book(user1, book)

    assert book.avaliable_copies == old_copies - 1
    assert result[0] is True


def test_auto_member_id(): #auto test
    lib = LibraryManager()

    success, message, user1 = lib.create_user("a", "a@e.com" )

    assert success is True
    assert user1.member_id == "M001"

    success, message, user2 = lib.create_user("b", "b@e.com")

    assert success is True
    assert user2.member_id == "M002"

def test_invalid_without_id():
    """checks the failed registration doesnt use waste member ID."""
    lib = LibraryManager()

    success, message, user1 = lib.create_user("a", "bERROR")

    assert success is False 
    assert user1 is None

    success, message, user2 = lib.create_user("b", "b@email.com")

    assert success is True 
    
    assert user2.member_id == "M001"    

def test_successful_returnid():
    lib = LibraryManager()
    success, message, user1 = lib.create_user("a", "a@email.com")

    

    assert success is True 
    assert user1 is not None
    assert user1.member_id == "M001"    

def test_search_user_existing():
    lib = LibraryManager()

    success, message, user1 = lib.create_user("a", "a@email.com")

    found_user = lib.search_user("M001")

    assert found_user is user1

def test_search_user_unknown():
    
    lib = LibraryManager()
    found_user = lib.search_user("M999")

    assert found_user is None