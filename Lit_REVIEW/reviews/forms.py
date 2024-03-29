﻿from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field
from crispy_forms.bootstrap import InlineRadios

from django import forms

from .models import Review, Ticket


class NewReviewForm(forms.ModelForm):
    """
    A form for creating new reviews.

    Attributes:
        headline (CharField): The title of the review.
        rating (ChoiceField): The rating given for the review, represented as stars.
        body (CharField): The body text of the review.
    """

    headline = forms.CharField(
        label="Title",
        max_length=128,
        widget=forms.TextInput()
    )
    rating = forms.ChoiceField(
        initial=1,
        label="Rating",
        widget=forms.RadioSelect(),
        choices=((1, "1 star"), (2, "2 stars"), (3, "3 stars"), (4, "4 stars"), (5, '5 stars'))
    )
    body = forms.CharField(
        label="Review",
        max_length=8192,
        widget=forms.Textarea(),
        required=False
    )

    class Meta:
        """Meta class for NewReviewForm."""
        model = Review
        fields = ['headline', 'rating', 'body']

    # Crispy forms layout helper
    helper = FormHelper()
    helper.form_class = 'form-group'
    helper.layout = Layout(
        Field('headline'),
        InlineRadios('rating', style="display: flex; justify-content: space-around;"),
        Field('body', rows="10"),
    )


class NewTicketForm(forms.ModelForm):
    """
    A form for creating new tickets.

    Attributes:
        title (CharField): The title of the ticket.
        description (CharField): A description of the ticket.
        image (ImageField): An optional image related to the ticket.
    """

    title = forms.CharField(
        label="Title",
        max_length=128,
        widget=forms.TextInput()
    )
    description = forms.CharField(
        label="Description",
        max_length=2048,
        widget=forms.Textarea(),
        required=False
    )
    image = forms.ImageField(
        label="Image",
        required=False
    )

    class Meta:
        """Meta class for NewTicketForm."""
        model = Ticket
        fields = ['title', 'description', 'image']
