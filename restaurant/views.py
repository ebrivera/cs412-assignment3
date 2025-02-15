from django.shortcuts import render
from django.http import HttpResponse, HttpRequest
import random
import time

# Create your views here.


SPECIALS = [
    "Chimi Churri Sauce",
    "Red Salsa",
    "Pico De Gayo",
    "Green Salsa",
    "Rice",
]

def order_page(request):
    """
        Show the form to the user.
    """
    template_name = 'restaurant/form.html'
    
    context = {
        'special': SPECIALS[random.randint(0,len(SPECIALS) - 1)],
        'current_time': time.ctime(),
    }

    return render(request, template_name, context=context)

def main_page(request):
    """
        show the main welcome page
    """
    template_name = 'restaurant/main.html'

    context = {
        'current_time': time.ctime(),
    }

    return render(request, template_name, context=context)


def submit(request: HttpRequest):
    '''Process the form submission, and generate a result.'''

    template_name = "restaurant/confirmation.html"


    if request.POST:

        name = request.POST.get("name")
        phone = request.POST.get("phone")
        email = request.POST.get("email")
        
        food = [
            ["Tacos", request.POST.get("Tacos")],
            ["Burrito", request.POST.get("Burrito")],
            ["Cheese", request.POST.get("Cheese")],
            ["Guac", request.POST.get("Guac")],
            ["Extra Meat", request.POST.get("extra-meat")],
            ["Enchiladas", request.POST.get("Enchiladas")],
            ["Quesadilla", request.POST.get("Quesadilla")],
            ["Special", request.POST.get("special")],
        ]

        food_updated = []

        for item, cost in food:
            if cost:
                food_updated.append((item, int(cost)))
        
        total_cost = 0
        for food in food_updated:
            total_cost += food[1]
        
        print(total_cost)
        
        specialInstructions = request.POST.get("special-instructions")

        context = {
            'name': name,
            'phone': phone,
            'email': email,
            'food': food_updated, # array with tuples containing item and cost
            'cost': total_cost,
            'instructions': specialInstructions,
            'current_time': time.ctime(),
            'readytime': readytime,
        }


    return render(request, template_name, context=context)



def readytime():
    current_time = time.time()  # current time
    random_addition = random.randint(30 * 60, 60 * 60)  # Random time in seconds between 30-60 minutes
    future_timestamp = current_time + random_addition 
    return time.ctime(future_timestamp) 
    
