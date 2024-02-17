from fastapi import Body, FastAPI
from pydantic import BaseModel, Field
# to use optional and not required feilds need to be brough over through typing instead of 
# pydantic
from typing import Optional

app = FastAPI()

#  this class creates our book object once we've succesfully validated our items 
class Book:
    id: int
    title: str
    author: str
    description:str
    rating: int

    def __init__(self, id, title, author, description, rating):
        self.id = id
        self.title = title
        self.author = author
        self.description = description
        self.rating = rating

# this class serves as our validator for our book items
class BookRequest(BaseModel):
    id: Optional[int] = None
    title: str = Field(min_length=3)
    author: str =  Field(min_length=1)
    description: str =  Field(min_length=1, max_length=100)
    # gt means greater than so we're saying > than -1, lt means lessthan
    rating:int =  Field(gt=0,lt=6)

    # config for having an automatic example in our schema
    class Config:
        json_schema_extra ={
            'example' : {
                'title': 'A new book',
                'author': 'codingwithroby',
                'description': ' A new description of a book',
                'rating': 5
            }
        }


# book request objt, to validate our book request so that we can transform it into  abook and add it to our list

BOOKS = [ 
    Book(1,'Blood Meridian', 'Cormac McCarthy', 'old west tale', 5),
    Book(2,'All the pretty horses', 'Cormac McCarthy', 'romance', 5),
    Book(3,'No Country for old men', 'Cormac McCarthy', 'western', 5),
    Book(4,'Computer Science pro', 'coding with roby', 'comp sci book', 5),
    Book(5,'physics', 'anthony pacheco', 'science book', 1),
    Book(6,'principles of langauges', 'Tat Young Kong', 'College Textbook', 1),
    Book(7,'Animal Farm', 'George Orwell', 'narrtive fiction in communisum', 3),
    Book(8,'A heart so white', 'Javier marias', 'fiction', 2),
]
@app.get("/books")
async def readAllBooks():
    return BOOKS


# api endpoint to find a book based on an ID
@app.get('/books/{book_id}')
async def read_book(book_id:int):
    for book in BOOKS:
        if book.id == book_id:
            return book
        
@app.get ('/books/')
async def read_book_by_rating(book_rating: int):
    booksToReturn = []
    for book in BOOKS:
        if book.rating == book_rating:
            booksToReturn.append(book)
    
    return booksToReturn



'''
1.book request is of type BookRequest(our validation model above)
2.then we create a new book of our type Book class from above, model dump turns into a dictionary
    2A. and the ** spreads the values so that they fit like incoming params into our class
3. Finally we just append the book to our list of books

'''
@app.post('/create-book')
async def create_book(book_request: BookRequest):
    new_book = Book(**book_request.model_dump())
    BOOKS.append(findBookId(book_request))


def findBookId(book:Book):
    # if we have books in our list
        # get the last book in the list and add 1 to the new book
    # otherwise its our first book in the list, assign one

    # return the book
    if len(BOOKS) > 0:
        book.id = BOOKS[-1].id + 1
    else:
        book.id = 1
    
    return book
