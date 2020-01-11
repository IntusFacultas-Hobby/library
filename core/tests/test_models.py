import pytest
from core.models import Book
from django.utils import timezone
from datetime import timedelta


@pytest.fixture
def publish_date():
    return timezone.now() - timedelta(days=730)


@pytest.fixture
def checkout_date():
    return timezone.now() - timedelta(days=1)


@pytest.fixture
def book(publish_date, checkout_date):
    return Book.objects.create(
        title="Test Book",
        author="Pedro Del Moral",
        description="A test book for testing",
        picture="/media/whatever/img.jpeg",
        date_published=publish_date,
        date_checked_out=checkout_date,
        checked_out=True,
    )


@pytest.mark.django_db
def test_book_str(book):
    assert str(book) == f"{book.title} by {book.author}"


@pytest.mark.django_db
def test_book_as_json(book):
    data = book.as_json()
    assert data["id"] == book.id
    assert data["title"] == book.title
    assert data["author"] == book.author
    assert data["description"] == book.description
    assert data["picture"] == book.picture.url
    assert data["datePublished"] == book.date_published.strftime("%Y-%m-%d")
    assert data["dateCheckedOut"] == book.date_checked_out.strftime("%Y-%m-%d")
    assert data["checkedOut"] == book.checked_out
