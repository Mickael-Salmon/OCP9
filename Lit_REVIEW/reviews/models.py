from PIL import Image, ImageOps

from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone


class Ticket(models.Model):
    """
    A model representing a ticket.

    Attributes:
        title (CharField): The title of the ticket.
        description (TextField): A description of the ticket.
        user (ForeignKey): The user who created the ticket.
        time_created (DateTimeField): The time the ticket was created.
        image (ImageField): An optional image related to the ticket.
    """

    title = models.CharField(max_length=128)
    description = models.TextField(max_length=2048, blank=True)
    user = models.ForeignKey(
        to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    time_created = models.DateTimeField(default=timezone.now)

    image = models.ImageField(blank=True, null=True, upload_to='reviews_img')

    def __str__(self):
        return f'Ticket-{self.title}'

    if image is True:
        def save(self, *args, **kwargs):
            """Override the save method to handle image resizing."""
            super().save()

            img = ImageOps.contain(
                Image.open(self.image.path),
                (200, 200),
                method=3
            )

            img.save(self.image.path)


class Review(models.Model):
    """
    A model representing a review.

    Attributes:
        ticket (ForeignKey): The ticket that the review is associated with.
        rating (PositiveSmallIntegerField): The rating of the review.
        headline (CharField): The headline of the review.
        body (TextField): The body text of the review.
        user (ForeignKey): The user who created the review.
        time_created (DateTimeField): The time the review was created.
    """

    ticket = models.ForeignKey(to=Ticket, on_delete=models.CASCADE)
    rating = models.PositiveSmallIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    headline = models.CharField(max_length=128)
    body = models.TextField(max_length=8192, blank=True)
    user = models.ForeignKey(
        to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    time_created = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f'Review-{self.headline}'
