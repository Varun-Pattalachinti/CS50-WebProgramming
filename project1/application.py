import os

from flask import Flask, session
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
import requests
from flask import request
from flask import render_template,redirect
from flask import jsonify
#import numpy as np


app = Flask(__name__)

#need to run set env of FLASK_APP to application.py
# $env:FLASK_APP = "application.py"

os.environ['DATABASE_URL'] = "postgres://xaciptytblugqm:34b58ebf93a364b25b100b494f0fdde4ff4e579b291cf005d706cf2098a5ad25@ec2-3-91-112-166.compute-1.amazonaws.com:5432/ddgs4bokj900uo"
# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Set up database
engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))


#checking if api is set up properly
goodreads_api_key = "TKbqwqg451cDHQz26Vz0Tw"
res = requests.get("https://www.goodreads.com/book/review_counts.json", params={"key": goodreads_api_key, "isbns": "9781632168146"})
#print(res.json())

#need to check if user is valid user
def addAdminUser():
    """
    adding the admin/test username and password to the database users
    """
    os.environ['DATABASE_URL'] = "postgres://xaciptytblugqm:34b58ebf93a364b25b100b494f0fdde4ff4e579b291cf005d706cf2098a5ad25@ec2-3-91-112-166.compute-1.amazonaws.com:5432/ddgs4bokj900uo"
    engine = create_engine(os.getenv("DATABASE_URL"))
    db = scoped_session(sessionmaker(bind=engine))
    username = 'vpatt'
    password = 'LifeConnor2020!!'
    db.execute("INSERT INTO users (username,password) VALUES (:username, :password)",
                {"username": username, "password": password}) # substitute values from CSV line into SQL command, as per this dict
    db.commit()
#addAdminUser()
def addUserColumnToReviewsMethod():
    """
    adding user column to review database
    """
    os.environ['DATABASE_URL'] = "postgres://xaciptytblugqm:34b58ebf93a364b25b100b494f0fdde4ff4e579b291cf005d706cf2098a5ad25@ec2-3-91-112-166.compute-1.amazonaws.com:5432/ddgs4bokj900uo"
    engine = create_engine(os.getenv("DATABASE_URL"))
    db = scoped_session(sessionmaker(bind=engine))
    db.execute('ALTER TABLE "reviews" ADD username VARCHAR NOT NULL')
    db.commit()

    #Test
    reviews ="Good Book!"
    book_id = 380795272
    username = "mountain"
    db.execute("INSERT INTO reviews (reviews,book_id,username) VALUES (:reviews, :book_id,:username)",
                {"reviews": reviews , "book_id": book_id, "username":username})
    db.commit()
    reviews_db = db.execute('SELECT * from "reviews"').fetchall()
    print(reviews_db)

#addUserColumnToReviewsMethod()
def addRatingColumnToReviewsMethod():
    """
    adding user column to review database
    """
    os.environ['DATABASE_URL'] = "postgres://xaciptytblugqm:34b58ebf93a364b25b100b494f0fdde4ff4e579b291cf005d706cf2098a5ad25@ec2-3-91-112-166.compute-1.amazonaws.com:5432/ddgs4bokj900uo"
    engine = create_engine(os.getenv("DATABASE_URL"))
    db = scoped_session(sessionmaker(bind=engine))
    db.execute('ALTER TABLE "reviews" ADD rating INTEGER')
    db.commit()

    #Test
    reviews ="Good Book!"
    book_id = 380795272
    username = "mountain"
    rating = 4
    db.execute("INSERT INTO reviews (reviews,book_id,username,rating) VALUES (:reviews, :book_id,:username,:rating)",
                {"reviews": reviews , "book_id": book_id, "username":username,"rating":rating})
    db.commit()
    reviews_db = db.execute('SELECT * from "reviews"').fetchall()
    print(reviews_db)
#addRatingColumnToReviewsMethod()
def isValidUser(username,password):
    """
    checking if valid user
    """
    os.environ['DATABASE_URL'] = "postgres://xaciptytblugqm:34b58ebf93a364b25b100b494f0fdde4ff4e579b291cf005d706cf2098a5ad25@ec2-3-91-112-166.compute-1.amazonaws.com:5432/ddgs4bokj900uo"

    engine = create_engine(os.getenv("DATABASE_URL"))
    db = scoped_session(sessionmaker(bind=engine))
    users = db.execute('SELECT id, username, password FROM "users"').fetchall()
    print(users)
    #print("ff")
    for user in users:
        #print(user.username)
        #print(user.password)
        #print(username)
        #print(password)
        if user.username == username and user.password == password:
            return True
    return False
@app.route("/", methods = ["POST","GET"])
def index():
    session["username"] = None
    session["password"] = None
    if request.method == "POST":
        if request.form.get("submit_button") == "Login":
            username = request.form.get("username")
            password = request.form.get("password")
            if isValidUser(username,password):
                #need to create user profile
                session["username"] = username
                session["password"] = password
                return redirect("/userprofile/"+username) # go
            else:
                return render_template("login.html",message="invalid username or password!",new_user=True)
        elif request.form.get("submit_button") == "New User":
            return redirect("/new_user")
    return render_template("login.html",message = "")
def isValidUsername(new_username):
    """
    checks to see if username is already in database
    """
    os.environ['DATABASE_URL'] = "postgres://xaciptytblugqm:34b58ebf93a364b25b100b494f0fdde4ff4e579b291cf005d706cf2098a5ad25@ec2-3-91-112-166.compute-1.amazonaws.com:5432/ddgs4bokj900uo"
    engine = create_engine(os.getenv("DATABASE_URL"))
    db = scoped_session(sessionmaker(bind=engine))

    #in order to check against sql injection attacks I should probably just get all
    usernames = db.execute('SELECT username FROM "users"').fetchall()
    #print(type(usernames))
    print(usernames)
    print(usernames[0][0])
    for username in usernames:
        if username[0] == new_username:
            return True
    return False

def addNewUser(new_username,new_password):
    """
    add new user in new users db
    """
    os.environ['DATABASE_URL'] = "postgres://xaciptytblugqm:34b58ebf93a364b25b100b494f0fdde4ff4e579b291cf005d706cf2098a5ad25@ec2-3-91-112-166.compute-1.amazonaws.com:5432/ddgs4bokj900uo"
    engine = create_engine(os.getenv("DATABASE_URL"))
    db = scoped_session(sessionmaker(bind=engine))
    username = new_username
    password = new_password
    db.execute("INSERT INTO users (username,password) VALUES (:username, :password)",
                {"username": username, "password": password}) # substitute values from CSV line into SQL command, as per this dict
    db.commit()

@app.route("/new_user" ,methods = ["GET","POST"])
def new_user():
    #need to create new_user template
    #print("got here")
    if request.method == "POST":
        username = request.form.get("new_username")
        password = request.form.get("new_password")
        #print(username)
        #print(password)
        if isValidUsername(username):
            #need to loop over usernames to see if username is used
            #addUser(username,password)
            return render_template("new_user_template.html",message="username already exists are you sure you are a new user?")

        else:
            #is a new user_name and password
            #can login with new information
            addNewUser(username,password)
            return redirect("/")
    return render_template("new_user_template.html",message = "")

#need to create new user profile page
@app.route("/userprofile/<string:username>" ,methods = ["GET","POST"])
def userprofile(username):
    if session["username"] != username:
        return redirect("/");
    if request.method == "POST":
        if request.form.get("button") == "logout":
            session["username"] = None
            session["password"] = None
            return redirect("/")
        if request.form.get("button") == "search":
            isbn = request.form.get("isbn")
            title = request.form.get("title")
            author = request.form.get("author")
            book_search_db = book_search(isbn,title,author)
            return render_template("user_profile.html",jinja_username=session["username"],search_results=book_search_db)
        if 'book_button_title' in request.form:
            print(request.form)
            title = request.form.get("book_button_title")
            name = request.form.get("book_button_name") #author
            isbn = request.form.get("book_button_isbn")
            return redirect("/bookpage/"+title+"/"+name+"/"+isbn)
            #print(book_title)
    return render_template("user_profile.html", jinja_username = session["username"],search_results = [])

def book_search(isbn,title,author):
    """
    need to get all book search possibilities, if any of the
    fields have a possiblity of matching I should return the whole entry
    should take into account mispellings in title or author
    """


    isbn_length = len(isbn)
    title_length = len(title)
    author_length = len(author)
    searchbyIsbn = False
    searchbyTitle = False
    searchbyAuthor = False
    if isbn_length != 0:
        searchbyIsbn=True
    if title_length != 0:
        searchbyTitle = True
    if author_length != 0:
        searchbyAuthor = True
    books = db.execute('SELECT * from "books"').fetchall()
    book_search_db = []
    for book in books:
        flag = False
        if searchbyIsbn and close_enough(book.isbn,isbn,0,len(book.isbn),isbn_length):
            flag = True
        if searchbyAuthor and close_enough(book.author,author,3,len(book.author),author_length):
            flag = True
        if searchbyTitle and close_enough(book.title,title,3,len(book.title),title_length):
            flag = True
        if flag:
            book_search_db.append([book.isbn,book.author,book.title,book.id])
    print(book_search_db)
    return book_search_db

def close_enough(str1,str2,distance,m,n):
    """
    an algorithm to check if two pieces of text are close enough in terms of edit distance
    """
    # Create a table to store results of subproblems
    dp = [[0 for x in range(n + 1)] for x in range(m + 1)]

    # Fill d[][] in bottom up manner
    for i in range(m + 1):
        for j in range(n + 1):

            # If first string is empty, only option is to
            # insert all characters of second string
            if i == 0:
                dp[i][j] = j    # Min. operations = j

            # If second string is empty, only option is to
            # remove all characters of second string
            elif j == 0:
                dp[i][j] = i    # Min. operations = i

            # If last characters are same, ignore last char
            # and recur for remaining string
            elif str1[i-1] == str2[j-1]:
                dp[i][j] = dp[i-1][j-1]

            # If last character are different, consider all
            # possibilities and find minimum
            else:
                dp[i][j] = 1 + min(dp[i][j-1],        # Insert
                                   dp[i-1][j],        # Remove
                                   dp[i-1][j-1])    # Replace

    if(dp[m][n]<=distance):
        return True
    return False

#Book Page: When users click on a book from the results of the search page,
# they should be taken to a book page, with details about the book:
#its title, author, publication year, ISBN number, and any reviews that users
# have left for the book on your website.
#Review Submission: On the book page, users should be able to submit
#a review: consisting of a rating on a scale of 1 to 5, as well as a text
#component to the review where the user can write their opinion about a book.
#Users should not be able to submit multiple reviews for the same book.
#Goodreads Review Data: On your book page, you should
#also display (if available) the average rating and
#number of ratings the work has received from Goodreads.
@app.route("/bookpage/<string:title>/<string:name>/<string:ISBN>" ,methods = ["GET","POST"])
def book_page(title,name,ISBN):
    #get reviews for book
    #add only one review for book
    #average goodreads ratings
    #number of ratings
    res = requests.get("https://www.goodreads.com/book/review_counts.json", params={"key": goodreads_api_key, "isbns": ISBN})
    #book_dict = json.JSONDecoder(res.json())
    if res.status_code!=200:
        return render_template("book_page.html",review_db = [])
    average_rating=res.json()['books'][0]['average_rating']
    ratings_count=res.json()['books'][0]['ratings_count']
    if ISBN[-1] == 'X':
        ISBN = ISBN[0:-1]
    isbn_number = int(ISBN)
    #get all reviews for the book from database
    reviews = []
    reviews = getReviews(isbn_number)
    #figure out if review is written by username if Post

    if request.method == "POST":
        reviews = getReviews(isbn_number)
        if reviews == [] and 'post_review' in request.form:
            #print("1")
            #then don't nee to check username and can just check if rating is valid
            new_post_review = request.form.get("post_review")
            rating_number = int(request.form.get("rating"))
            #need to fugure out type of ratingn umber to correctly process it
            if rating_number <= 5 and rating_number >= 1:
                Addpost(new_post_review,isbn_number,session["username"],rating_number)
                reviews = getReviews(isbn_number)
                return render_template("book_page.html",review_db=reviews,title_render = title, author_render = name,ISBN_render = ISBN, message = "", average_rating = average_rating, ratings_count=ratings_count)
            else:
                return render_template("book_page.html",review_db=reviews,title_render = title, author_render = name,ISBN_render = ISBN, message = "The rating needs to be between 1 and 5", average_rating = average_rating, ratings_count=ratings_count)
        if 'post_review' in request.form and oldPost(reviews,session["username"]) ==False:
            #can simply add the REVIEW
            #print("2")
            new_post_review = request.form.get("post_review")
            rating_number = int(request.form.get("rating"))
            #need to fugure out type of ratingn umber to correctly process it
            if rating_number <= 5 and rating_number >= 1:
                Addpost(new_post_review,isbn_number,session["username"],rating_number)
                reviews = getReviews(isbn_number)
                return render_template("book_page.html",review_db=reviews,title_render = title, author_render = name,ISBN_render = ISBN, message = "",average_rating = average_rating, ratings_count=ratings_count)
            else:
                return render_template("book_page.html",review_db=reviews,title_render = title, author_render = name,ISBN_render = ISBN, message = "The rating needs to be between 1 and 5",average_rating = average_rating, ratings_count=ratings_count)
        if 'post_review' in request.form and oldPost(reviews,session["username"])==True:
            #print("3")
            new_post_review = request.form.get("post_review")
            rating_number = int(request.form.get("rating"))

            if rating_number <= 5 and rating_number >= 1:
                Deletepost(isbn_number,session["username"])
                Addpost(new_post_review,isbn_number,session["username"],rating_number)
                reviews = getReviews(isbn_number)
                return render_template("book_page.html",review_db=reviews,title_render = title, author_render = name,ISBN_render = ISBN, message = "",average_rating = average_rating, ratings_count=ratings_count)
            else:
                return render_template("book_page.html",review_db=reviews,title_render = title, author_render = name,ISBN_render = ISBN, message = "The rating needs to be between 1 and 5",average_rating = average_rating, ratings_count=ratings_count)
    return render_template("book_page.html",review_db = reviews, title_render = title, author_render = name , ISBN_render = ISBN, message = "",average_rating = average_rating, ratings_count=ratings_count)

def getReviews(isbn_number):
    """
    get the reviews for a particular book
    """
    os.environ['DATABASE_URL'] = "postgres://xaciptytblugqm:34b58ebf93a364b25b100b494f0fdde4ff4e579b291cf005d706cf2098a5ad25@ec2-3-91-112-166.compute-1.amazonaws.com:5432/ddgs4bokj900uo"
    engine = create_engine(os.getenv("DATABASE_URL"))
    db = scoped_session(sessionmaker(bind=engine))
    reviews = db.execute('SELECT id,reviews,book_id,username,rating FROM "reviews"').fetchall()
    #print(reviews)
    book_reviews = []
    for review in reviews:
        if review[2] == isbn_number:
            book_reviews.append(review)
    #print(book_reviews)
    return book_reviews

def oldPost(reviews,username):
    print(reviews)
    print(len(reviews))
    for i in range(len(reviews)):
        review = reviews[i]
        if review[3]==username:
            return True
    return False

def Addpost(new_post_review,isbn_number,username,rating):
    """
    add a review to reviews
    """
    #access the database
    os.environ['DATABASE_URL'] = "postgres://xaciptytblugqm:34b58ebf93a364b25b100b494f0fdde4ff4e579b291cf005d706cf2098a5ad25@ec2-3-91-112-166.compute-1.amazonaws.com:5432/ddgs4bokj900uo"
    engine = create_engine(os.getenv("DATABASE_URL"))
    db = scoped_session(sessionmaker(bind=engine))

    db.execute("INSERT INTO reviews (reviews,book_id,username,rating) VALUES (:reviews, :book_id,:username,:rating)",
                {"reviews": new_post_review , "book_id": isbn_number, "username":username,"rating":rating})
    db.commit()
    #reviews_db = db.execute('SELECT * from "reviews"').fetchall()
    #print(reviews_db)

#test
#Addpost("Book is Great!",1416949658,'mountain')

def Deletepost(isbn_number,username):
    """
    delete a review in reviews
    """
    os.environ['DATABASE_URL'] = "postgres://xaciptytblugqm:34b58ebf93a364b25b100b494f0fdde4ff4e579b291cf005d706cf2098a5ad25@ec2-3-91-112-166.compute-1.amazonaws.com:5432/ddgs4bokj900uo"
    engine = create_engine(os.getenv("DATABASE_URL"))
    db = scoped_session(sessionmaker(bind=engine))

    db.execute("DELETE FROM reviews WHERE book_id = :book_id AND username = :username",{"book_id":isbn_number,"username":username})
    db.commit()
    #reviews_db = db.execute('SELECT * from "reviews"').fetchall()
    #print(reviews_db)

#Test
#Deletepost(380795272,'mountain')



@app.route("/api/<string:isbn>")
def book_api(isbn):
    os.environ['DATABASE_URL'] = "postgres://xaciptytblugqm:34b58ebf93a364b25b100b494f0fdde4ff4e579b291cf005d706cf2098a5ad25@ec2-3-91-112-166.compute-1.amazonaws.com:5432/ddgs4bokj900uo"
    engine = create_engine(os.getenv("DATABASE_URL"))
    db = scoped_session(sessionmaker(bind=engine))

    books = db.execute('SELECT * from "books"').fetchall()
    book_for_api = []
    for book in books:
        #print(book)
        if (book[1]) == isbn:
            book_for_api = book
    #print(book_for_api)
    if len(book_for_api) == 0:
        print("hello fail")
        return jsonify({"error": "Invalid isbn number make sure to have the right number of leading zeros"}), 404
    #need to try to convert the isbn to a int
    if isbn[-1] == 'X':
        isbn_mod = isbn[0:-1]
        #need to get number of reviews and average rating
    else:
        isbn_mod = isbn
    isbn_num = int(isbn_mod)
    avg_rating,num_reviews = getAvgRatingandNumofReviews(isbn_num)
    title = book_for_api[1]
    author = book_for_api[2]
    year = book_for_api[3]
    return jsonify({
        "title": title,
        "author": author,
        "year": year,
        "isbn":isbn,
        "review_count": num_reviews,
        "average_score": avg_rating
    })

def getAvgRatingandNumofReviews(isbn_num):
    os.environ['DATABASE_URL'] = "postgres://xaciptytblugqm:34b58ebf93a364b25b100b494f0fdde4ff4e579b291cf005d706cf2098a5ad25@ec2-3-91-112-166.compute-1.amazonaws.com:5432/ddgs4bokj900uo"
    engine = create_engine(os.getenv("DATABASE_URL"))
    db = scoped_session(sessionmaker(bind=engine))
    count = 0
    rating_tot=0
    reviews = db.execute('SELECT id,reviews,book_id,username,rating FROM "reviews"').fetchall()
    for review in reviews:
        if(book_id == isbn_num):
            count = count+1
            rating_tot = review[3] + rating_tot
    if count == 0:
        return 0,0
    return rating_tot/count,count
