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

        ttk.Label(self.book_tab, text="Not built yet").grid(row=0, column=0)
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
        """save data after teh cahnge is successful"""
        return self.save()
            
            
            
        
            


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
