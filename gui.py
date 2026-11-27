# GenAI acknowledgement:
# I acknowledge the use of ChatGPT (version Astra 6, OpenAI, https://chatgpt.com/)
# and Claude (Claude Opus 5.5, Anthropic, https://claude.ai/) to review a
# draft of my work and provide feedback.


import tkinter as tk
from tkinter import ttk, messagebox

from library_core import LibraryManager

BOOKS = "books.txt"
MEMBERS = "members.txt"
LOANS = "loans.txt"

class LibraryApp(tk.Frame):
    """Main winbdow for library system
    
    class structure from: https://docs.python.org/3/library/tkinter.html"""

    def __init__(self, master=None):
        tk.Frame.__init__(self, master)

        self.lib = LibraryManager()

        self.grid()

        self.loaded = self.load()
        if not self.loaded:
            return

        self.create_widgets()


        #save data when window is closed
        master.protocol("WM_DELETE_WINDOW", self.close_app)

    def create_widgets(self):
        """sets up tabs for books, members and loans"""

        notebook = ttk.Notebook(self)
        notebook.grid(row=0, column=0, padx=10, pady=10)

        ##### TAB SEPERATING #####
        
        self.book_tab = ttk.Frame(notebook, padding=10)
        self.members_tab = ttk.Frame(notebook, padding=10)
        self.loans_tab = ttk.Frame(notebook, padding=10)

        ##### ADDING TABS #####

        notebook.add(self.book_tab, text="Books")
        notebook.add(self.members_tab, text="Members")
        notebook.add(self.loans_tab, text="Loans")

        # PLACEHOLDERS

        self.create_books_tab()
        ttk.Label(self.members_tab, text="Not built yet").grid(row=0, column=0)
        ttk.Label(self.loans_tab, text="Not built yet").grid(row=0, column=0)

    def load(self):
        """loads saved books, members and loans"""

        success, message = self.lib.load_data(BOOKS, MEMBERS, LOANS)

        if success:
            messagebox.showinfo("Data loaded", message)
        else:
            messagebox.showerror("Load failed", message)
        return success

    def save(self):
        """saves my library data"""

        success, message = self.lib.save_data(BOOKS, MEMBERS, LOANS)

        if not success:
            messagebox.showerror("Save failed", message)
        return success

    def close_app(self):
        """saves before closing window """

        if self.save():
            self.master.destroy()     

        ### HELPERS ###

    def show_result(self, title, success, message):
        """Helps find if an action successful or not"""

        if success:
            messagebox.showinfo(title, message)
        else:
            messagebox.showerror(title, message) 

        return success

    def read_text(self, entry, field):
        """read text from input, + check its not empty"""
        val = entry.get().strip()

        if not val:
            messagebox.showerror(f"invalid input: ", f"{field} cant be blank")
            return None
        return val

    def read_whole_no(self, entry, field,minimum=None):
        """read a whole no and check it meets the requirmenets"""
        val = self.read_text(entry, field)

        if val is None:
            return None
        
        try:
            no = int(val)
        except ValueError:
            messagebox.showerror(f"invalid input", f"{field} must be whole no. ")
            return None

        if minimum is not None and no < minimum:
            messagebox.showerror(f"invalid input", f"{field} must be at least {minimum}")
            return None
        
        return no
    
    def read_member_id(self, entry):
        """read ID, convert to uppercase"""
        member_id = self.read_text(entry, "Member ID")

        if member_id is None:
            return None
        
        return member_id.upper()
    
    def after_change(self):
        """save data + updates books table"""

        if self.save():
            self.refresh_books()
            return True
        

        return False
            
            
            
        
            
    def make_entry(self, parent, text, row, column, width=25):
        """creates label + entry box"""

        ttk.Label(parent, text=text).grid( row=row, column=column,padx=5,pady=3,sticky="w")
        entry = ttk.Entry(parent, width=width)
        entry.grid(row=row,column=column+1,padx=5,pady=3)

        return entry 

    def create_books_tab(self):
        """creates the book form buttons and table"""

        form = ttk.Frame(self.book_tab)
        form.grid(row=0, column=0, sticky="w")

        self.isbn_entry = self.make_entry(form, "ISBN",0,0)
        self.title_entry = self.make_entry(form, "Title",1,0)
        self.author_entry = self.make_entry(form, "Author",2,0)
        self.genre_entry = self.make_entry(form, "Genre",0,2,15)
        self.year_entry = self.make_entry(form, "Year",1,2,15)
        self.copies_entry = self.make_entry(form, "Copies",2,2,15)
        self.amount_entry = self.make_entry(form, "Amount",3,2,15)

        buttons = ttk.Frame(self.book_tab)
        buttons.grid(row=1,column=0,sticky="w",pady="10")

        ttk.Button(buttons, text="Add").grid(row=0,column=0, padx=5) 
        ttk.Button(buttons, text="Remove").grid(row=0,column=1, padx=5) 
        ttk.Button(buttons, text="Change quantity").grid(row=0,column=2, padx=5) 
        ttk.Button(buttons, text="Search").grid(row=0,column=3, padx=5) 
        ttk.Button(buttons, text="Show all",command = self.refresh_books).grid(row=0,column=4,padx=5)

        table_frame = ttk.Frame(self.book_tab)
        table_frame.grid(row=2, column=0, sticky="nsew")

        columns = ("isbn", "title", "author", "genre", "year", "available")

        self.books_table = ttk.Treeview(table_frame, columns=columns, show="headings", height=10)

        headings = {
                "isbn":            ("ISBN", 90),
                "title":           ("Title", 200),
                "author":          ("Author", 140),
                "genre":           ("Genre", 100),
                "year":            ("Year", 60),
                "available":       ("Available", 80)
                }
        
        for column in columns:
            name, width = headings[column]
            self.books_table.heading(column, text=name)
            self.books_table.column(column, width = width)

        scrollbar = ttk.Scrollbar(
            table_frame, orient="vertical",
            command = self.books_table.yview
        )

        self.books_table.configure(yscrollcommand=scrollbar.set)

        self.books_table.grid(row=0, column=0, sticky="nsew")
        scrollbar.grid(row=0, column=1, sticky="ns")

        self.refresh_books()
        
    def refresh_books(self, books=None):
        """Updates the table with the current books, sorted by title."""

        if books is None:
            books = self.lib.books

        self.books_table.delete(*self.books_table.get_children())

        for book in sorted(books, key=lambda b: b.title.lower()):
            available = str(book.avaliable_copies) + " / " + str(book.total_copies)

            self.books_table.insert("", "end", iid=book.ISBN,
                                    
                                    values=(book.ISBN, book.title, book.author,
                                    book.genre, book.year, available)
                                    )




def main():
    root = tk.Tk()
    root.title("Library")

    app = LibraryApp(master=root)
    if not app.loaded:
        root.destroy()
        return

    app.mainloop()

if __name__ == "__main__":
    main()
