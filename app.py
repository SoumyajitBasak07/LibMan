import eel
import sqlite3
from datetime import datetime 

ADMIN_PASS = "libman"

"""
TODO:
[ ] First Screen
  [ ] Welcome Message
  [ ] Student Button
  [ ] Admin Button

[ ] Student Borrowing Page
  [ ] Message
  [ ] List of books
  [ ] Book items should include: Name, Late fine, Genre
  [ ] Option to return
  [ ] Details Entry Form
      [ ]Details Should include: Name
      [ ]Name of the Book

[ ] Admin Page
    [ ]full details of books present
    [ ]restocking of current books
    [ ]Stocking of new Books
"""

eel.init("web")

con = sqlite3.connect("dev.db")
c = con.cursor()


def get_book_list():
  return c.execute("SELECT *  FROM books WHERE quantity > 0 ").fetchall()


@eel.expose
def public_book_list():
  return get_book_list()

#invoked for the password
@eel.expose
def check_pass(password):
  return password == ADMIN_PASS

#invoked when the user issues a book
@eel.expose
def issue_book(user_name, book):
  print(user_name, book)
  # add user to table
  user = c.execute("INSERT INTO users(name) VALUES(?)", (user_name,)).lastrowid
  print(user)
  book=c.execute("SELECT * FROM books WHERE name = ?", (book,)).fetchone()
  # add transaction to library logs
  lib_log = c.execute("INSERT INTO library_log(user_id, book_id, start_date, submitted) VALUES(?, ?, ?, ?)", (user, book[0], datetime.now(), False))
  # subtract quantity of book by 1
  c.execute("UPDATE books SET quantity = ? WHERE id = ?", (book[4] - 1, book[0],))

  # save changes to db
  con.commit()

#invoked while adding a book
@eel.expose
def add_book(book,genre,fine,quantity):
  if quantity==0:
    #adding not allowed if the quantity is 0
    return
  else:
    books=c.execute("INSERT INTO books(name,genre,fine,quantity) VALUES(?, ?, ?, ?)",(book,genre,fine,quantity))
  
  # save changes to db
  con.commit()
#invoked to restock books


@eel.expose
def restock(quantity,book_id):
  quantity = int(quantity)
  book_id = int(book_id)
  print(quantity, book_id)
  if quantity==0:
    #adding not allowed if the quantity is 0
    return
  else:
    books=c.execute("UPDATE books SET quantity = ? WHERE id = ?", (quantity, book_id,))
  
  # save changes to db
  con.commit()
  
  
 


eel.start('index.html', mode='my_portable_chromium', 
                        host='localhost', 
                        port=27000, 
                        block=True )
