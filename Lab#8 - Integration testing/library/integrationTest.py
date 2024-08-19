# Lab8 - Integration testing
# นายชลพัฒน์ ปิ่นมุนี รหัส 653380126-0
# Unit test -> class Borrowlist in main.py
# Integration testing - Create a test client to check the connection and interaction
# among different components of the application.

import pytest
from fastapi.testclient import TestClient
from main import app, get_db, Book, User, Borrowlist

# create a test client to interact with the api
@pytest.fixture
def client(db_session):
    def override_get_db():
        try:
            yield db_session
        finally:
            pass
        
    app.dependency_overrides[get_db] = override_get_db
    return TestClient(app)


@pytest.mark.parametrize("username, fullname", [("test_user1", "test_fullname1")])
def test_create_user(client, db_session, username, fullname):
    # makes a POST request to the /users/ endpoint
    response = client.post("/users/?username={}&fullname={}".format(username, fullname))
    
    # check if the response status code is 200
    assert response.status_code == 200
    
    # check if the response contains the username and fullname
    assert response.json()["username"] == username
    assert response.json()["fullname"] == fullname
    
    # check if the user is added to the database
    assert db_session.query(User).filter(User.username == username).first()
    
    
@pytest.mark.parametrize("title, firstauthor, isbn", [("test_book1", "test_author1", "test_isbn1")])
def test_create_book(client, db_session, title, firstauthor, isbn):
    # makes a POST request to the /books/ endpoint
    response = client.post("/books/?title={}&firstauthor={}&isbn={}".format(title, firstauthor, isbn))
    
    # check if the response status code is 200
    assert response.status_code == 200   
    
    # check if the response contains the title, firstauthor and isbn
    assert response.json()["title"] == title
    assert response.json()["firstauthor"] == firstauthor
    assert response.json()["isbn"] == isbn
    
    # check if the book is added to the database
    assert db_session.query(Book).filter(Book.title == title).first()

    
def test_create_borrow_book(client, db_session):
    
    # Create the user to associate with the book
    user = User(username="test_user2", fullname="test_fullname2")
    db_session.add(user)
    db_session.commit()
    
    # Create the book to be borrowed
    book = Book(title="test_book2", firstauthor="test_author2", isbn="test_isbn2")
    db_session.add(book)
    db_session.commit()
    
    # makes a POST request to the /borrowlist/ endpoint
    response = client.post("/borrowlist/?user_id={}&book_id={}".format(user.id, book.id))
    
    # check if the response status code is 200
    assert response.status_code == 200
    
    # check if the response contains the user_id and book_id
    assert response.json()["user_id"] == user.id
    assert response.json()["book_id"] == book.id
    
    # check if the borrowlist is added to the database
    assert db_session.query(Borrowlist).filter(Borrowlist.user_id == user.id).filter(Borrowlist.book_id == book.id).first()
    

#สามารถดูรายการหนังสือที่ผู้ใช้ยืมได้
def test_get_borrowlist(client, db_session):
    # Create the user to associate with the book
    user = User(username="test_user3", fullname="test_fullname3")
    db_session.add(user)
    db_session.commit()
    
    # Create the book to be borrowed
    book1 = Book(title="test_book3", firstauthor="test_author3", isbn="test_isbn3")
    db_session.add(book1)
    db_session.commit()
    
    book2 = Book(title="test_book4", firstauthor="test_author4", isbn="test_isbn4")
    db_session.add(book2)
    db_session.commit()
    
    # Create the borrowlist
    borrow1 = Borrowlist(user_id=user.id, book_id=book1.id)
    db_session.add(borrow1)
    db_session.commit()
    
    borrow2 = Borrowlist(user_id=user.id, book_id=book2.id)
    db_session.add(borrow2)
    db_session.commit()
    
    # makes a GET request to the /borrowlist/ endpoint
    response = client.get("/borrowlist/{}".format(user.id))
    
    # check if the response status code is 200
    assert response.status_code == 200
    
    # check if the response contains the borrowed books
    borrowlist = response.json()
    
    # check if the user borrowed 2 books
    assert len(borrowlist) == 2
    
    # check if we get the correct user_id
    assert borrowlist[0]["user_id"] == user.id
    assert borrowlist[1]["user_id"] == user.id
    
    # check if the user borrowed the correct books
    assert borrowlist[0]["book_id"] == book1.id
    assert borrowlist[1]["book_id"] == book2.id
    
    
    
    

    
    
    