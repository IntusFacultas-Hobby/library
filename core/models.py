from django.db import models


class Book(models.Model):
    """ Book Django ORM Object
    """
    title = models.CharField("Title", max_length=512)
    author = models.CharField("Author", max_length=128)
    description = models.CharField("Description", max_length=1024)
    picture = models.ImageField("Image")
    date_published = models.DateField("Date Published")

    def __str__(self):
        """ Returns Book Title and Author

        Arguments: None
        Returns: String
        """
        return f'{self.title} by {self.author}'

    def as_json(self):
        """ Converts a Django ORM object into a dict that can be passed to the frontend as JSON

        Arguments: None
        Returns: dict
        {
            "id": Integer,
            "title": String,
            "author": String,
            "description": String,
            "picture": String,
            "datePublished": DateString (YYYY-MM-DD)
        }
        """
        return {
            "id": self.id,
            "title": self.title,
            "author": self.author,
            "description": self.description,
            "picture": self.picture.url,
            "datePublished": self.date_published.strftime("%Y-%m-%d")
        }