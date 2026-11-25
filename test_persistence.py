# GenAI acknowledgement:
# I acknowledge the use of ChatGPT (version Astra 6, OpenAI, https://chatgpt.com/)
# and Claude (Claude Opus 5.5, Anthropic, https://claude.ai/) to review a
# draft of my work and provide feedback.

from library_core import Book, LibraryManager

def test_save_load_roundtrip(tmp_path):
    """checks loans/copies/ID come back correctly after loading"""
    files = (tmp_path / "books.txt", tmp_path / "members.txt", tmp_path / "loans.txt")

    lib = LibraryManager()
    book1 = Book("111", "TinkyDinky", "JohnBon", "Fiction", 1943, 2)
    book2 = Book("222", "DinkyTinky", "ofg dsfsd", "Fiction", 1932, 1)

    lib.add_book(book1)
    lib.add_book(book2)

    success, message, user = lib.create_user("Alice", "a@e.com")

    success, message, loan1 = lib.borrow_book(user, book1)
    lib.renew_loan(loan1)

    success, message, loan2 = lib.borrow_book(user, book2)
    lib.return_book(loan2)

    success, message = lib.save_data(*files)
    assert success is True

    new_lib = LibraryManager()
    success,message = new_lib.load_data(*files)
    assert success is True

    assert len(new_lib.books) == 2
    assert len(new_lib.users) == 1
    assert len(new_lib.loans) == 2
    #checks saved data

    #checks active loan
    new_loan = new_lib.find_active_loan("M001", "111")
    assert new_loan is not None
    assert new_loan.due_date == loan1.due_date
    assert new_loan.renewals == 1
    assert new_loan.is_active is True

    assert new_lib.find_active_loan("M001","222") is None

    # returned loan logic
    returned_loan  = None

    for loan in new_lib.loans:
        if loan.book.ISBN == "222":
            returned_loan  = loan
            break
    assert returned_loan is not None
    assert returned_loan.is_active is False 

    #check avaliable copies
    assert new_lib.find_book("111").avaliable_copies == 1
    assert new_lib.find_book("222").avaliable_copies == 1

    #check the loan is linked to loaded user
    new_user = new_lib.search_user("M001")
    assert new_loan.user is new_user
    
    #check next member ID
    success,message,usernew = new_lib.create_user("Bob", "b@e.com")
    assert usernew.member_id == "M002"