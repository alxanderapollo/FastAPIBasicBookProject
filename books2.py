# path is a way for us to validate path params
from fastapi import FastAPI, Path,Query, HTTPException 
from pydantic import BaseModel, Field
# automatically installed with FASTAPI
from starlette import status
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
    publishedDate: int

    def __init__(self, id, title, author, description, rating, publishedDate):
        self.id = id
        self.title = title
        self.author = author
        self.description = description
        self.rating = rating
        self.publishedDate = publishedDate

# this class serves as our validator for our book items
class BookRequest(BaseModel):
    id: Optional[int] = None
    title: str = Field(min_length=3)
    author: str =  Field(min_length=1)
    description: str =  Field(min_length=1, max_length=100)
    # gt means greater than so we're saying > than -1, lt means lessthan
    rating:int = Field(gt=0,lt=6)
    publishedDate:int = Field(gt=0, lt=2025)

    # config for having an automatic example in our schema
    class Config:
        json_schema_extra ={
            'example' : {
                'title': 'A new book',
                'author': 'codingwithroby',
                'description': ' A new description of a book',
                'rating': 5,
                'publishedDate': 2002
            }
        }


# book request objt, to validate our book request so that we can transform it into  abook and add it to our list

BOOKS = [ 
    Book(1,'Blood Meridian', 'Cormac McCarthy', 'old west tale', 5, 2001),
    Book(2,'All the pretty horses', 'Cormac McCarthy', 'romance', 5, 2001),
    Book(3,'No Country for old men', 'Cormac McCarthy', 'western', 5, 2001),
    Book(4,'Computer Science pro', 'coding with roby', 'comp sci book', 5, 2011),
    Book(5,'physics', 'anthony pacheco', 'science book', 1, 2012),
    Book(6,'principles of langauges', 'Tat Young Kong', 'College Textbook', 1, 2022),
    Book(7,'Animal Farm', 'George Orwell', 'narrtive fiction in communisum', 3, 2024),
    Book(8,'A heart so white', 'Javier marias', 'fiction', 2, 2001),
]

# status_code=status.HTTP_200_OK -> this means to send a status ok after returning what was asked for
@app.get("/books", status_code=status.HTTP_200_OK)
async def read_All_Books():
    return BOOKS


# api endpoint to find a book based on an ID
# our book id path param needs to be greater than 0 or it will throw an error
@app.get('/books/{book_id}', status_code=status.HTTP_200_OK)
async def read_book(book_id:int = Path(gt=0)):
    for book in BOOKS:
        if book.id == book_id:
            return book
        # if the book is not found return 404
    
    raise HTTPException(status_code=404, detail='Item not found')
        
@app.get('/books/',status_code=status.HTTP_200_OK)
async def read_book_by_rating(book_rating: int = Query(gt=0, lt = 6)):
    booksToReturn = []
    for book in BOOKS:
        if book.rating == book_rating:
            booksToReturn.append(book)
    
    return booksToReturn


# get books by publishing date
@app.get('/books/published/',status_code=status.HTTP_200_OK)
async def read_book_by_published_date(book_published: int = Query(gt=0, lt=2025)):
    booksToReturn = []
    for book in BOOKS:
        if book.publishedDate == book_published:
            booksToReturn.append(book)
    
    return booksToReturn



'''
1.book request is of type BookRequest(our validation model above)
2.then we create a new book of our type Book class from above, model dump turns into a dictionary
    2A. and the ** spreads the values so that they fit like incoming params into our class
3. Finally we just append the book to our list of books

'''
@app.post('/create-book',status_code=status.HTTP_201_CREATED)
async def create_book(book_request: BookRequest):
    new_book = Book(**book_request.model_dump())
    BOOKS.append(findBookId(new_book))


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

# this is to update one of our objects, and to do it by ID

# update objects
@app.put('/books/update_book',status_code=status.HTTP_204_NO_CONTENT)
async def update_book(book: BookRequest):
    book_change = False
    for i in range(len(BOOKS)):
        if BOOKS[i].id == book.id:
            BOOKS[i] = book
            # if we found the book and change it set it True
            book_change = True

    if not book_change:
        raise HTTPException(status_code=404, detail='Item not found')


# delete objects

@app.delete('/books/{book_id}',status_code=status.HTTP_204_NO_CONTENT)
async def delete_book(book_id: int = Path(gt=0)):
    book_change = False

    for i in range(len(BOOKS)):
        if BOOKS[i].id == book_id:
            BOOKS.pop(i)
            book_change = True
            break
    
    if not book_change:
        raise HTTPException(status_code=404, detail='Item not found')





