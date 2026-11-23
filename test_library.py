# GenAI acknowledgement:
# I acknowledge the use of ChatGPT (version Astra 6, OpenAI, https://chatgpt.com/)
# and Claude (Claude Opus 5.5, Anthropic, https://claude.ai/) to review a
# draft of my work and provide feedback.

from library_core import Book, LibraryManager

def make_book(ISBN="123", copies=2):
    """creates a test book with teh given ISBN, including no.of copies"""
    return Book(ISBN, "pyth", "fds sd", "dsds", 1242, copies)

def make_lib_with_user():
    """creates library with a  registered memebr
    
    returns lib, user1"""
    lib = LibraryManager()
    success, message, user1 = lib.create_user("a", "a@e.com" )
    return lib, user1

def test_borrow_book():
    """checks that borrowing a book actually reduces its avaliable copies + records the loan"""

    lib, user1 = make_lib_with_user()
    book = make_book()

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

    lib, user1 = make_lib_with_user()

    book = make_book(copies=0)

    lib.add_book(book)
    success, message, loan = lib.borrow_book(user1, book)

    assert success is False
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

def test_search_user_existing():
    lib, user1 = make_lib_with_user()


    found_user = lib.search_user("M001")

    assert found_user is user1

def test_search_user_unknown():
    
    lib = LibraryManager()
    found_user = lib.search_user("M999")

    assert found_user is None


def test_find_active_loan():
    """checks to see if an active loan can be foudn using a vliad ID+ISBN"""
    lib, user1 = make_lib_with_user()

    book = make_book()
    lib.add_book(book)

    success, message, loan = lib.borrow_book(user1, book)

    loan_found = lib.find_active_loan("M001","123")

    assert loan_found is loan

def test_find_active_loan_unknown():
    """checks None is returned when no matching loan is exists"""

    lib = LibraryManager()
    
    loan_found = lib.find_active_loan("M999","543")

    assert loan_found is None


def test_find_returned_loan():
    """checks to see if returned loans cant be found as active loans"""
    lib, user1 = make_lib_with_user()
    book = make_book()

    lib.add_book(book)
    success, message, loan = lib.borrow_book(user1, book)
    lib.return_book(loan)
    loan_found = lib.find_active_loan("M001","123")

    
    assert loan_found is None


def test_get_user_loans():
    """checks all loans are returned """

    lib, user1 = make_lib_with_user()
    book1 = make_book("123")
    book2 = make_book("456")

    lib.add_book(book1) 
    lib.add_book(book2)



    success, message, loan1 = lib.borrow_book(user1, book1)
    success, message, loan2 = lib.borrow_book(user1, book2)

    user_loans = lib.get_user_loans("M001")

    assert len(user_loans) == 2
    assert user_loans[0] is loan1
    assert user_loans[1] is loan2


def test_loan_includes_return():
    """checks teh loans are in the loan history"""

    lib, user1 = make_lib_with_user()

    book = make_book()
    lib.add_book(book)

    success, message, loan = lib.borrow_book(user1, book)
    lib.return_book(loan)

    user_loans = lib.get_user_loans("M001")

    assert len(user_loans) == 1
    assert user_loans[0] is loan
    assert user_loans[0].is_active is False


def test_get_user_loans_unknown():
    """checks empty list is returned for the unknwon member"""
    lib = LibraryManager()
    user_loans = lib.get_user_loans("M999")

    assert user_loans == []
    










