# file: quotes/views.py
from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
import time
import random
# Create your views here.

IMAGES = [
    "https://upload.wikimedia.org/wikipedia/commons/f/f8/Alan_Turing_%281951%29.jpg",
    "https://awl.com/wp-content/uploads/2022/06/29i273kbby241.png",
    "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcR2A9NJyg0KEuIls2WTvmppXcyiLbdM3f-Igw&s",
]

QUOTES = [
    "Sometimes it is the people no one can imagine anything of who do the things no one can imagine.",
    "Those who can imagine anything, can create the impossible.",
    "We can only see a short distance ahead, but we can see plenty there that needs to be done.",
]

def home(request):
    '''
    Define a view to handle the 'home' request.
    '''

    response_text = f'''
    <html>
        <h1>Hello, world!</h1>
        <p> the current time is {time.ctime()} </p>

    </html>
    '''
    
    return HttpResponse(response_text)


def home_page(request):
    '''Define a view to show the 'home.html' template.'''

    # the template to which we will delegate the work
    template = 'quotes/quote.html'

    # a dict of key/value pairs, to be available for use in template
    context = {
        'selected_image': IMAGES[random.randint(0,2)],
        'selected_quote': QUOTES[random.randint(0,2)],
        'current_time': time.ctime(),
    }

    return render(request, template, context)

def about(request):
    '''Define a view to show the 'about.html' template.'''

    # the template to which we will delegate the work
    template = 'quotes/about.html'


    # a dict of key/value pairs, to be available for use in template
    context = {
        'current_time': time.ctime(),
    }

    return render(request, template, context)

def show_all(request):
    '''Define a view to show the 'show_all.html' template.'''

    # the template to which we will delegate the work
    template = 'quotes/show_all.html'

    # a dict of key/value pairs, to be available for use in template
    context = {
        'quotes': QUOTES,
        'images': IMAGES,
        'current_time': time.ctime(),
    }

    return render(request, template, context)