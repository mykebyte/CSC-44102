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
    print(f'ISBN: {book.ISBN} | title: {book.title} | author: {book.author} | genre: {book.genre}| year: {book.year} | avaliable_copies: {book.avaliable_copies} / {book.total_copies} avaliable.  ')

def add_book_option(lib):
    """Gets book details, adds to library"""
    ISBN = get_non_empty_input("ISBN: ")
    title = get_non_empty_input("title: ")
    author = get_non_empty_input("author: ")
    genre = get_non_empty_input("genre: ")
    year = get_whole_no("year: ",0)
    copies = get_whole_no("copies: ",0)

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
    """loops the menu options until the user reverts"""
    while True:
        print("\nBooks")
        print("1. Add a book")
        print("2. View books")
        print("3. Search books")
        print("4. Remove a book")
        print("5. Update copies")
        print("6. Back")

        answer = input("Enter a command: ").strip()

        if answer == "1":
            add_book_option(lib)
        elif answer == "2":
            view_book_options(lib)
        elif answer == "3":
            search_books_option(lib)
        elif answer == "4":
            remove_book_option(lib)
        elif answer == "5":
            update_copies_option(lib)
        elif answer == "6":
            return

        else:
            print("Try again")

        


def members_menu(lib):
    print("\nMembers:")
    print("Not built yet")

def loans_menu(lib):
    print("\nLoans:")
    print("Not built yet")

def search_books_option(lib):
    """Lets user search for a book by title or ISBN"""
    print("1 - seach by title")
    print("2 - seach by ISBN")

    answer = input("Enter a command: ").strip()

    if answer == "1":
        title=get_non_empty_input("Title, or the first few characters: ")
        found_books = lib.search_book(title)

        if not found_books:
            print("No matching books")
            return
        
        for book in found_books:
            show_book(book)

    elif answer == "2":
        ISBN = get_non_empty_input("ISBN: ")
        book = lib.find_book(ISBN)

        if book is None:
            print("Book not found")
        else:
            show_book(book)

    else:
        print("try again")

def remove_book_option(lib):
    """Removes a book, via its ISBN"""
    ISBN = get_non_empty_input("ISBN: ")
    success, message = lib.remove_book(ISBN)
    print(message)


def update_copies_option(lib):
    """Allows the user to up or down the copies"""
    ISBN = get_non_empty_input("ISBN: ")
    book = lib.find_book(ISBN)

    if book is None:
        print("Book not found")
        return
    
    show_book(book)

    change = get_whole_no("Change in copies: ")
    success, message = book.update_quantity(change)

    print(message)

    if success:
        show_book(book)




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
            books_menu(lib)
        elif choice == "2":
            members_menu(lib)
        elif choice == "3":
            loans_menu(lib)
        elif choice == "4":
            success, message = lib.save_data(BOOKS, MEMBERS, LOANS)
            print(message)

            if success:
                print("Closing...")
                break
        else:
            print("Try again")


if __name__ == "__main__":
    main()




