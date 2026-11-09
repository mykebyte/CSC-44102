book = {
    "title": "The Pragmatic Programmer",
    "author": "Aaaa Bbbb and Cccc Dddd",
    "year": 2004,
    "isbn": "353665465",
    "genre": "Programming",
    "avaliable": True 
}

#setting up dictionary with key chaarcteristics

def display_book(book_dict):
    if not isinstance(book_dict, dict):
        raise TypeError("Dictionary expected")
    
    print("Book Details")
    for k,v in book_dict.items():
        print(f"{k}, {v}")

#end