# GenAI acknowledgement:
# I acknowledge the use of ChatGPT (version Astra 6, OpenAI, https://chatgpt.com/)
# and Claude (Claude Opus 5.5, Anthropic, https://claude.ai/) to review a
# draft of my work and provide feedback.

from library_core import LibraryManager


BOOKS = "books.txt"
MEMBERS= "members.txt"
LOANS = "loans.txt"

def books_menu(lib):
    print("Books:")
    print("Not built yet")

def members_menu(lib):
    print("Members:")
    print("Not built yet")

def loans_menu(lib):
    print("Loans:")
    print("Not built yet")1


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
                print("Closing.")
                break

        else:
            print("Try again")


if __name__ == "__main__":
    main()




