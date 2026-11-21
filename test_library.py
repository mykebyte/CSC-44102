# GenAI acknowledgement:
# I acknowledge the use of ChatGPT (version Astra 6, OpenAI, https://chatgpt.com/)
# and Claude (Claude Opus 5.5, Anthropic, https://claude.ai/) to review a
# draft of my work and provide feedback.

from library_core import Book, LibraryManager

def test_borrow_book():
    """Checks that borrowing a book actually reduces its available copies"""
    lib = LibraryManager()
    
    success, message, user1 = lib.create_user("a", "a@e.com" )
    book = Book("123", "pyth", "fds sd", "dsds", 1242, 2)

    lib.add_book(book)

    old_copies = book.avaliable_copies

    success, message, loan = lib.borrow_book(user1, book)

    assert success is True
    assert loan is not None
    assert loan.user is user1
    assert loan.book is book
    assert book.avaliable_copies == old_copies - 1
    assert loan in lib.loans
    assert loan in user1.loans

def test_borrow_book_unavaliable():
    """" checks borriwing fials when no copies are avaliable"""

    lib = LibraryManager()

    success, message, user1 = lib.create_user("a", "a@e.com" )
    book = Book("123", "pyth", "fds sd", "dsds", 1242, 2)

    lib.add_book(book)

    success, message, loan = lib.borrow_book(user1, book)

    assert success is True
    assert loan is None
    assert book.avaliable_copies == 0
    assert len(lib.loans) == 0

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