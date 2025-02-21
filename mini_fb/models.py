from django.db import models

# Create your models here.
class Profile(models.Model):
    '''Encapsulate the idea of an Article by some author.'''

    # define the data attributes of the Article object
    title = models.TextField(blank=True)
    author = models.TextField(blank=True)
    text = models.TextField(blank=True)
    published = models.DateTimeField(auto_now=True)
    image_url = models.URLField(blank=True)
    

    def __str__(self):
        """return a string representation of the model instance"""
        return f'{self.title}'