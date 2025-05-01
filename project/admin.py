# File: ./project/admin.py
# Author: Ernesto Rivera (ebrivera@bu.edu), 4/15/25
# Description: Allows us to create an admin instance where
# we can see all of the coffee related objects

from django.contrib import admin

# Register your models here.
from .models import CoffeeBag, Review, Tag, CoffeeBagTag, CoffeeEnthusiast

admin.site.register(CoffeeBag)
admin.site.register(Review)
admin.site.register(Tag)
admin.site.register(CoffeeBagTag)
admin.site.register(CoffeeEnthusiast)