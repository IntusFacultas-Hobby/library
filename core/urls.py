from django.urls import path, include
from core.views import BookDetails, BookList, Storefront, Details
app_name = "core"

urlpatterns = [
    path("api/stable/", include([
        path("books", BookList.as_view(), name="api-books"),
        path("book/<int:pk>", BookDetails.as_view(), name="api-book"),
    ])),
    path("api/v1/", include([
        path("books", BookList.as_view(), name="api-books"),
        path("book/<int:pk>", BookDetails.as_view(), name="api-book"),
    ])),
    path("book/<int:pk>", Details.as_view(), name="book"),
    path("", Storefront.as_view(), name="storefront")
]