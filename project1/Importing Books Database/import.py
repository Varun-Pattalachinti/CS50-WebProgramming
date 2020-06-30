import os
import csv
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

def create_book_table(db,csv_reader):
    """
    Creates books data table
    """

    db.execute('CREATE TABLE "books" ('
      'id SERIAL PRIMARY KEY,'
      'isbn VARCHAR NOT NULL,'
      'title VARCHAR NOT NULL,'
      'author VARCHAR NOT NULL,'
       'year INTEGER NOT NULL'');')

    flag = False;
    for isbn,title,author,year in csv_reader: # loop gives each column a name
        #print(year)
        #print(isbn)
        if(flag):

          db.execute("INSERT INTO books (isbn, title,author,year) VALUES (:isbn, :title, :author,:year)",
                      {"isbn": isbn, "title": title, "author": author, "year":int(year)}) # substitute values from CSV line into SQL command, as per this dict
        flag = True
    db.commit()

def create_user_table(db):
    db.execute('CREATE TABLE "users" ('
    'id SERIAL PRIMARY KEY,'
    'username VARCHAR NOT NULL,'
    'password VARCHAR NOT NULL'');')

    db.commit()

def create_review_table(db):
    db.execute('CREATE TABLE "reviews" ('
    'id SERIAL PRIMARY KEY,'
    'reviews VARCHAR NOT NULL,'
    'book_id INTEGER'');')

    db.commit()


def main():
    # Set up database
    os.environ['DATABASE_URL'] = "postgres://xaciptytblugqm:34b58ebf93a364b25b100b494f0fdde4ff4e579b291cf005d706cf2098a5ad25@ec2-3-91-112-166.compute-1.amazonaws.com:5432/ddgs4bokj900uo"

    engine = create_engine(os.getenv("DATABASE_URL"))
    db = scoped_session(sessionmaker(bind=engine))
    books = open("books.csv")
    books_reader = csv.reader(books)


    create_book_table(db,books_reader);
    books = db.execute('SELECT * from "books"').fetchall()
    print(books)

    create_user_table(db)
    create_review_table(db)

if __name__ == "__main__":
      main()
