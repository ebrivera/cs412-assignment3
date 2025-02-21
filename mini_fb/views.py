# mini_fb/views.py
from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Article
import random

# Create your views here.
class ShowAllView(ListView):
    """Define a view class to show all blog articles."""
    model = Article
    template_name = "mini_fb/show_all.html"
    context_object_name = "articles"

class ArticleView(DetailView):
    """Display a single article"""

    model = Article
    template_name = "mini_fb/article.html"
    context_object_name = "article" #singular

class RandomArticleView(DetailView):
    """Display a single article view at random"""

    model = Article
    template_name = "mini_fb/article.html"
    context_object_name = "article" #singular

    # method
    def get_object(self):
        """return one instance of the Article object at random"""

        all_articles = Article.objects.all()
        article = random.choice(all_articles)
        return article