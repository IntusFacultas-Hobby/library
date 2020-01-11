from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse, HttpResponse
from django.core.paginator import Paginator, EmptyPage
from django.views import View
from core.models import Book


class BookList(View):
    """ Returns a list of books as JSON

    Accepted Arguments:
    :param all: Boolean, returns all books. By default the results will be paginated
    :param pageSize: Integer, number of books to return, by default it will 25
    :param page: Integer, page to return, by default it will be 1
    :param orderBy: String, options are (
        title, author, description, picture, date_published, id,
        -title, -author, -description, -picture, -date_published, -id
    ), by default -id

    Django ORM filters are accepted as well.

    Returns:
    :on success:
        Status 200
        {
            data: [List of JSON objects],
            startIndex: 1-based Integer
            endIndex: 1-based Integer,
            total: 1-based Integer
            numPages: 1-based Integer
        }
    :on error: status 400, error message
    """

    DEFAULT_PAGE_SIZE = 25
    DEFAULT_PAGE = 1
    DEFAULT_ORDER_BY = "-id"
    VALID_ORDER_BY_OPTIONS = [
        "title", "author", "description", "picture", "date_published", "id",
        "-title", "-author", "-description", "-picture", "-date_published", "-id"
    ]

    def options(self, request):
        response = HttpResponse(status=200)
        response['allow'] = ','.join(['get', 'options'])
        return response

    def get(self, request):
        filters = request.GET.copy()
        all_books = request.GET.get("all", None)

        # parse all argument then remove from filters
        if all_books is not None:
            del filters["all"]
            all_books = bool(all_books)
        else:
            all_books = False

        # parse pageSize argument then remove from filters
        page_size = request.GET.get("pageSize", None)
        if page_size is not None:
            del filters["pageSize"]
            try:
                page_size = int(page_size)
            except ValueError:
                return HttpResponse("Malformed request", status=400)
        elif not all_books:
            page_size = self.DEFAULT_PAGE_SIZE

        # parse page argument then remove from filters
        page = request.GET.get("page", None)
        if page is not None:
            del filters["page"]
            try:
                page = int(page)
            except ValueError:
                return HttpResponse("Malformed request", status=400)
        elif not all_books:
            page = self.DEFAULT_PAGE

        # parse orderBy argument then remove from filters
        orderBy = request.GET.get("orderBy", None)
        if orderBy is not None:
            del filters["orderBy"]
            if orderBy not in self.VALID_ORDER_BY_OPTIONS:
                return HttpResponse("Malformed request", status=400)
        else:
            orderBy = self.DEFAULT_ORDER_BY

        # retrieve books from database and order by field provided so we can paginate deterministically
        start_index = 0
        end_index = 0
        num_pages = 0
        try:
            books = Book.objects.all(**filters).order_by(orderBy)
        except Exception:
            return HttpResponse("Malformed request", status=400)
        total = books.count()

        # paginate and get start and end indexes
        if not all_books:
            paginator = Paginator(books, page_size)
            try:
                books = paginator.page(page)
                start_index = books.start_index()
                end_index = books.end_index()
                num_pages = paginator.num_pages
            except EmptyPage:
                books = []
        else:
            end_index = total
            if end_index > 0:
                start_index = 1

        # format response
        data = {
            "data": [book.as_json() for book in books],
            "startIndex": start_index,
            "endIndex": end_index,
            "total": total,
            "numPages": num_pages
        }

        # response
        return JsonResponse(data, safe=False)


class BookDetails(View):
    """ Given a book ID, returns the details for that book as JSON

    Arguments:
    :param pk: the ID of the book

    Returns:
    :on success:
        Status 200
        data as returned by Book.as_json
    :on failure:
        Status 404
    """

    def options(self, request, pk):
        response = HttpResponse(status=200)
        response['allow'] = ','.join(['get', 'options'])
        return response

    def get(self, request, pk):
        book = get_object_or_404(Book, pk=pk)
        return JsonResponse(book.as_json(), safe=False)


class Storefront(View):
    """ Serves the Storefront page
    """

    def get(self, request):
        return render(request, "core/storefront.html", {})


class Details(View):
    """ Serves the Book Details page
    """

    def get(self, request, pk):
        return render(request, "core/details.html", {"pk": pk})
