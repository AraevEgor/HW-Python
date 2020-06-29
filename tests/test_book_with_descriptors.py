import pytest

from book_with_descriptors import Book

def test_book_construct_normal_params():
    test_book = Book('John Johnson', 'My Book', 99)
    
def test_book_counstruct_price_out_of_bounds():
    with pytest.raises(ValueError) as e:
        test_book = Book('John Johnson', 'My Book', 199)
    assert str(e.value) == 'Price must be between 0 and 100', 'Unexpected error message'
    
def test_book_change_price_positive():
    test_book = Book('John Johnson', 'My Book', 99)
    test_book.price = 88

def test_book_change_price_out_of_bounds():
    test_book = Book('John Johnson', 'My Book', 99)
    with pytest.raises(ValueError) as e:
        test_book.price = 199
    assert str(e.value) == 'Price must be between 0 and 100', 'Unexpected error message'

def test_book_change_author_forbidden():
    test_book = Book('John Johnson', 'My Book', 99)
    with pytest.raises(ValueError) as e:
        test_book.author = 'John Malkovich'
    assert str(e.value) == 'Author cannot be changed', 'Unexpected error message'
    
def test_book_change_name_forbidden():
    test_book = Book('John Johnson', 'My Book', 99)
    with pytest.raises(ValueError) as e:
        test_book.name = 'Not My Book'
    assert str(e.value) == 'Name cannot be changed', 'Unexpected error message'
