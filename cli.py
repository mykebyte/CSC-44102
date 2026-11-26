# GenAI acknowledgement:
# I acknowledge the use of ChatGPT (version Astra 6, OpenAI, https://chatgpt.com/)
# and Claude (Claude Opus 5.5, Anthropic, https://claude.ai/) to review a
# draft of my work and provide feedback.

from library_core import LibraryManager
from library_core import Book, LibraryManager

BOOKS = "books.txt"
MEMBERS= "members.txt"
LOANS = "loans.txt"

def show_book(book):
    """Show detials of book"""
    print(f'ISBN: {book.ISBN} | title: {book.title} | author: {book.author} | title: {book.title} | genre: {book.genre} | year: {book.year} | avaliable_copies: {book.avaliable_copies} / {book.total_copies} avaliable. | ')

def add_book_option(lib):
    """Gets book details, adds to library"""
    ISBN = get_non_empty_input("ISBN: ")
    title = get_non_empty_input("title: ")
    author = get_non_empty_input("author: ")
    genre = get_non_empty_input("genre: ")
    year = get_non_empty_input("year: ")
    copies = get_non_empty_input("copies: ")

    try: 
        book = Book(ISBN, title, author, genre, year, copies)
    except ValueError as error:
        print(f"Couldn't add book: {error}")
        return

    success,message = lib.add_book(book)
    print(message)

def view_book_options(lib):
    """Shows all books currently in library"""
    if not lib.books:
        print("No books found")
        return
    
    for book in lib.books:
        show_book(book)


def get_non_empty_input(prompt):
    """Keeps asking the user for text, until something is entered."""
    while True:
        answer = input(prompt).strip()
        if answer != "":
            return answer
        print("Please enter, answer cannot be blank")

def get_whole_no(prompt, minimum=None):
    """Keeps asking for a whole number; check it meets the minimum if there is a minimum."""
    while True:
        answer = input(prompt).strip()

        try:
            number = int(answer)
        except ValueError:
            print("Please enter a valid whole number: ")
            continue

        if minimum is not None and number < minimum:
            print(f"Enter a number of at leastm {minimum}, Thanks") 
            continue   

        return number


def books_menu(lib):
    print("Books:")
    print("Not built yet")

def members_menu(lib):
    print("Members:")
    print("Not built yet")

def loans_menu(lib):
    print("Loans:")
    print("Not built yet")


def main():
    lib = LibraryManager()
    success, message = lib.load_data(BOOKS, MEMBERS, LOANS)
    print(message)

    while True:
        print("\nLibrary Management System")
        print("1. Books")
        print("2. Members")
        print("3. Loans")
        print("4. Save and exit")

        choice = str(input("Enter a comand: ")).strip()

        if choice == "1":
            add_book_option(lib)
        elif choice == "2":
            view_book_options(lib)
        elif choice in ("3", "4", "5"):
            print("Not built yetd")
        elif choice == "6":
            return

        else:
            print("Try again")


if __name__ == "__main__":
    main()




