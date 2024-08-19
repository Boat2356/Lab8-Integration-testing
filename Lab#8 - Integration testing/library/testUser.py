# Lab8 - Integration testing
# นายชลพัฒน์ ปิ่นมุนี รหัส 653380126-0
# Unit test -> class User in main.py

import pytest
from main import User

# uses the db_session fixture inside conftest.py
def test_add_user(db_session):
    # Create a new user instance
    new_user = User(username="test_newuser1", fullname="test_fullname1")
    db_session.add(new_user)
    db_session.commit()
    
    # Query the database for the new user    
    user = db_session.query(User).filter(User.username == "test_newuser1").first()
    assert user is not None
    assert user.fullname == "test_fullname1"
   
def test_delete_user(db_session):
    # Create a new user instance
    new_user = User(username="test_newuser2", fullname="test_fullname2")
    db_session.add(new_user)
    db_session.commit()
    
    # Delete the test_newuser2
    db_session.delete(new_user)
    db_session.commit()
    
    # Query the test_newuser2 to check if it is deleted
    deleted_user = db_session.query(User).filter(User.username == "test_newuser2").first()
    assert deleted_user is None
    