# Lab8 - Integration testing
# นายชลพัฒน์ ปิ่นมุนี รหัส 653380126-0
# Unit test -> class Book in main.py

import pytest
from main import Book

# uses the db_session fixture inside conftest.py
def test_add_book(db_session):
    # Create a new book instance
    new_book = Book(title="test_newbook1", firstauthor="test_author1", isbn="test_isbn1")
    db_session.add(new_book)
    db_session.commit()
    
    # Query the database for the new book    
    book = db_session.query(Book).filter(Book.title == "test_newbook1").first()
    assert book is not None
    assert book.firstauthor == "test_author1"
    assert book.isbn == "test_isbn1"
    
def test_delete_book(db_session):
    # Create a new book instance
    new_book = Book(title="test_newbook2", firstauthor="test_author2", isbn="test_isbn2")
    db_session.add(new_book)
    db_session.commit()
    
    # Delete the test_newbook2
    db_session.delete(new_book)
    db_session.commit()
    
    # Query the test_newbook2 to check if it is deleted
    deleted_book = db_session.query(Book).filter(Book.title == "test_newbook2").first()
    assert deleted_book is None