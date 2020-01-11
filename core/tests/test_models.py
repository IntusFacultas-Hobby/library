import pytest
from core.models import Book

@pytest.fixture
def book():
    return Book.objects.create(
        
    )


@pytest.mark.django_db
def test_book_str()