from django import forms
from .models import CoffeeBag, Review, CoffeeEnthusiast, Tag

class CreateCoffeeBagForm(forms.ModelForm):
    """A form to add a coffee bag in the db"""

    class Meta:
        """associate this form with a model from our db"""
        model = CoffeeBag
        fields = [
            'company', 
            'roast', 
            'origin',
            'notes', 
            'image',
        ]

class CreateReviewForm(forms.ModelForm):
    """A form to add a review in the db"""

    tags = forms.ModelMultipleChoiceField(
        queryset=Tag.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
    )

    class Meta:
        """associate this form with a model from our db"""
        model = Review
        fields = [
            'review_text', 
            'rating',
            'brew_method',
        ]

class CreateEnthusiastForm(forms.ModelForm):
    """A form to add a coffee enthusiast in the db"""

    class Meta:
        model = CoffeeEnthusiast
        fields = [
            'profile_image', 
            'favorite_coffee_bags',
        ]


class UpdateCoffeeEnthusiastForm(forms.ModelForm):
    '''A form to update an enthusia to the database.'''

    class Meta:
        '''associate this form with the enthusiast model.'''
        model = CoffeeEnthusiast
        fields = ['profile_image', 'favorite_coffee_bags'] 