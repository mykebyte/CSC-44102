# GenAI acknowledgement:
# I acknowledge the use of ChatGPT (version Astra 6, OpenAI, https://chatgpt.com/)
# and Claude (Claude Opus 5.5, Anthropic, https://claude.ai/) to review a
# draft of my work and provide feedback.

from datetime import date, timedelta

from library_core import Book, LibraryManager, Loan


def make_loan_setup(copies=2):
    """creates librabry with a single: memebr, book and loan
    returnsL lib, user, book and loan"""

    lib = LibraryManager()

    success, message, user1 = lib.create_user("a", "a@e.com" )
    book = Book("123", "pyth", "fds sd", "dsfs", 1242, copies)

    lib.add_book(book)

    success, message, loan = lib.borrow_book(user1, book)

    assert success is True
    return lib, user1, book, loan


def test_return_book():
    """checks returnigna loan ends it and gives the copy back"""
    lib, user1, book, loan = make_loan_setup()
    old_copies = book.avaliable_copies

    success, message = lib.return_book(loan)

    assert success is True
    assert loan.is_active is False
    assert book.avaliable_copies == old_copies + 1

def test_return_book_twice():
    """checks returnign teh same loan again fails + doesnt add an extra copy"""
    lib, user1, book, loan = make_loan_setup()

    lib.return_book(loan)
    copies_after_return = book.avaliable_copies

    success, message = lib.return_book(loan)

    assert success is False
    assert book.avaliable_copies == copies_after_return


def test_renew_loan():
    """checks renewing an active loan adds a loan period to teh due date"""
    lib, user1, book, loan = make_loan_setup()

    old_due = loan.due_date
    success, message = lib.renew_loan(loan)

    assert success is True
    assert loan.due_date == old_due + timedelta(days=Loan.LOAN_PERIOD)
    assert loan.renewals == 1

def test_renew_loan_again():
    """checks a second renrewal fail with due date staing the same"""
    lib, user1, book, loan = make_loan_setup()

    lib.renew_loan(loan)
    due_after_renewal = loan.due_date

    success, message = lib.renew_loan(loan)

    assert success is False
    assert loan.due_date == due_after_renewal
    assert loan.renewals == 1

def test_renew_overdue_loan():
    """checks a overdue laon cant be renewed"""
    lib, user1, book, loan = make_loan_setup()

    loan.due_date = date.today() - timedelta(days=1)
    old_due = loan.due_date

    success, message = lib.renew_loan(loan)

    assert success is False
    assert loan.due_date == old_due
    assert loan.renewals == 0

def test_renew_after_return():
    """checks a RETURNED laon cant be renewed"""
    lib, user1, book, loan = make_loan_setup()

    lib.return_book(loan)
    old_due = loan.due_date

    success, message = lib.renew_loan(loan)

    assert success is False
    assert loan.due_date == old_due
    assert loan.renewals == 0
