from fastapi import Body, FastAPI
# Post Requests have a piece of information called the body which the get request doesnt
# in order to the use the body, we need to bring that in so that we can send that essential information into our post
# allows uvicorn to know we're brining in fastapi
app = FastAPI()

# query parameters are used to sort/filter resources. On the other hand, path parameters are used to identify a specific resource or resources.


# return a list of books
BOOKS = [
    {'title':'Title One', 'author':'Author One', 'category':'science'},
    {'title':'Title Two', 'author':'Author Two', 'category':'science'},
    {'title':'Title Three', 'author':'Author Three', 'category':'history'},
    {'title':'Title Four', 'author':'Author Four', 'category':'math'},
    {'title':'Title Five', 'author':'Author Five', 'category':'math'},
    {'title':'Title Six', 'author':'Author Two', 'category':'math'},

    ]

# dyanmic apis should always go after static ones bc of priority of the system

# decorator - get method
@app.get("/books")
async def read_all_books():
    return BOOKS

# dynamic path param
# the param dynamic param in the decorator will match the param in Url, and the function below
@app.get("/books/{book_title}")
async def read_book(book_title:str):
    # casefold -> to lowercase
    for book in BOOKS:
        if book.get('title').casefold() == book_title.casefold():
            return book

# Fast API automatically makes query = pairing value like this http://127.0.0.1:8000/books/?category=math, it knows when you do a books/ its knows its a query param
# read books by category - this a by query param 
@app.get("/books/")
async def read_category_by_query(category:str):
    books_to_return = []

    for book in BOOKS:
        if book.get('category').casefold() == category.casefold():
            books_to_return.append(book)

    return books_to_return


# path and query param - the / at the end makes it a query-path param 
@app.get("/books/{book_author}/")
async def read_author_category_by_query(book_author: str, category: str):
    books_to_return = []
    for book in BOOKS:
       if book.get('author').casefold() == book_author.casefold() and \
       book.get('category').casefold() == category.casefold():
           books_to_return.append(book)
    
    return books_to_return

# Create a new API Endpoint that can fetch all books from a specific author using either Path Parameters or Query Parameters
@app.get("/books/fetchByAuthor/{name_of_author}")
async def get_book_by_author(author:str):
    booksByAuthor = []
    for book in BOOKS:
        if book.get('author').casefold() == author.casefold():
            booksByAuthor.append(book)
    
    return booksByAuthor



# Post
@app.post("/books/create_book")
async def create_book(new_book = Body()):
    BOOKS.append(new_book)

# Put - matches the title, and then adds the updated object for that book with all of the acompanying information
@app.put("/books/update_book")
async def update_book(updated_book = Body()):
    for i in range(len(BOOKS)):
        if BOOKS[i].get('title').casefold() == updated_book.get('title').casefold():
            BOOKS[i] = updated_book


# delete method
@app.delete("/books/delete_book/{book_title}")
async def delete_book(book_title: str):
    for i in range(len(BOOKS)):
        if BOOKS[i].get('title').casefold() == book_title.casefold():
            BOOKS.pop(i)
            break 
        
