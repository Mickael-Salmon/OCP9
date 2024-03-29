from itertools import chain

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.core.exceptions import PermissionDenied
from django.core.paginator import Paginator
from django.db.models import Value, CharField
from django.shortcuts import render, redirect, get_object_or_404
from django.utils.datastructures import MultiValueDictKeyError
from django.views.generic import DeleteView

from .forms import NewReviewForm, NewTicketForm
from .models import Review, Ticket
from .utils import (
    get_user_viewable_reviews,
    get_user_viewable_tickets,
    get_replied_tickets,
    get_user_follows,
)


# -------- Feeds --------
@login_required
def feed(request):
    followed_users = get_user_follows(request.user)

    # Reviews and Tickets from followed users and the current user
    reviews = get_user_viewable_reviews(request.user)
    reviews = reviews.annotate(content_type=Value('REVIEW', CharField()))

    tickets = get_user_viewable_tickets(request.user)
    tickets = tickets.annotate(content_type=Value('TICKET', CharField()))

    # Replied tickets and reviews
    replied_tickets, replied_reviews = get_replied_tickets(tickets)

    # Pending tickets without a review response
    pending_tickets = Ticket.objects.exclude(id__in=[r.ticket.id for r in Review.objects.all()])
    pending_tickets = pending_tickets.annotate(content_type=Value('PENDING_TICKET', CharField()))

    # Combine all posts and sort them
    posts_list = sorted(
        chain(reviews, tickets, pending_tickets),
        key=lambda post: post.time_created,
        reverse=True
    )

    # Pagination
    if posts_list:
        paginator = Paginator(posts_list, 5)
        page = request.GET.get('page')
        posts = paginator.get_page(page)
    else:
        posts = None

    context = {
        'posts': posts,
        'r_tickets': replied_tickets,
        'r_reviews': replied_reviews,
        'title': 'Feed',
        'followed_users': followed_users,
        'pending_tickets': pending_tickets  # New key for pending tickets
    }

    return render(request, 'reviews/feed.html', context)


@login_required
def user_posts(request, pk=None):
    if pk:
        user = get_object_or_404(User, id=pk)
    else:
        user = request.user

    followed_users = get_user_follows(request.user)

    reviews = Review.objects.filter(user=user)
    reviews = reviews.annotate(content_type=Value('REVIEW', CharField()))

    tickets = Ticket.objects.filter(user=user)
    tickets = tickets.annotate(content_type=Value('TICKET', CharField()))

    replied_tickets, replied_reviews = get_replied_tickets(tickets)

    posts_list = sorted(chain(reviews, tickets), key=lambda post: post.time_created, reverse=True)

    if posts_list:
        paginator = Paginator(posts_list, 5)
        page = request.GET.get('page')
        posts = paginator.get_page(page)
        total_posts = paginator.count
    else:
        posts = None
        total_posts = 0

    context = {
        'posts': posts,
        'title': f"{user.username}'s posts ({total_posts})",
        'r_tickets': replied_tickets,
        'r_reviews': replied_reviews,
        'followed_users': followed_users
    }

    return render(request, 'reviews/feed.html', context)


# -------- Reviews --------
@login_required
def review_new(request):
    if request.method == 'POST':
        t_form = NewTicketForm(request.POST, request.FILES)
        r_form = NewReviewForm(request.POST)

        if t_form.is_valid() and r_form.is_valid():
            try:
                image = request.FILES['image']
            except MultiValueDictKeyError:
                image = None

            t = Ticket.objects.create(
                user=request.user,
                title=request.POST['title'],
                description=request.POST['description'],
                image=image
            )
            t.save()
            Review.objects.create(
                ticket=t,
                user=request.user,
                headline=request.POST['headline'],
                rating=request.POST['rating'],
                body=request.POST['body']
            )
            messages.success(request, 'Your review has been posted!')
            return redirect('reviews-feed')

    else:
        t_form = NewTicketForm()
        r_form = NewReviewForm()

    context = {
        't_form': t_form,
        'r_form': r_form,
        'title': 'New Review'
    }

    return render(request, 'reviews/review_form.html', context)


@login_required
def review_response(request, pk):
    ticket = get_object_or_404(Ticket, id=pk)

    if request.method == 'POST':
        r_form = NewReviewForm(request.POST)

        if r_form.is_valid():
            Review.objects.create(
                ticket=ticket,
                user=request.user,
                headline=request.POST['headline'],
                rating=request.POST['rating'],
                body=request.POST['body']
            )
            messages.success(request, f'Your response to "{ticket.title}" has been posted!')
            return redirect('reviews-feed')

    else:
        r_form = NewReviewForm()

    context = {
        'r_form': r_form,
        'post': ticket,
        'title': 'Response Review'
    }

    return render(request, 'reviews/review_form.html', context)


@login_required
def review_update(request, pk):
    review = get_object_or_404(Review, id=pk)
    if review.user != request.user:
        raise PermissionDenied()

    if request.method == 'POST':
        r_form = NewReviewForm(request.POST, instance=review)

        if r_form.is_valid():
            r_form.save()
            messages.success(request, 'Your review has been updated!')
            return redirect('reviews-feed')

    else:
        r_form = NewReviewForm(instance=review)

    context = {
        'r_form': r_form,
        'post': review.ticket,
        'title': 'Update Review'
    }

    return render(request, 'reviews/review_form.html', context)


@login_required
def review_detail(request, pk):
    review = get_object_or_404(Review, id=pk)
    followed_users = get_user_follows(request.user)

    context = {
        'post': review,
        'title': 'Review detail',
        'followed_users': followed_users
    }

    return render(request, 'reviews/post_detail.html', context)


class ReviewDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Review
    success_url = '/'
    context_object_name = 'post'

    def test_func(self):
        review = self.get_object()
        if self.request.user == review.user:
            return True
        return False

    def delete(self, request, *args, **kwargs):
        messages.warning(self.request, f'Your review "{self.get_object().headline}" has been deleted.')
        return super(ReviewDeleteView, self).delete(request, *args, **kwargs)


# -------- Tickets --------
@login_required
def ticket_new(request):
    if request.method == 'POST':
        form = NewTicketForm(request.POST, request.FILES)

        if form.is_valid():
            image = request.FILES.get('image', None)
            Ticket.objects.create(
                user=request.user,
                title=request.POST['title'],
                description=request.POST['description'],
                image=image
            )
            messages.success(request, 'Your ticket has been posted!')
            return redirect('reviews-feed')

    else:
        form = NewTicketForm()

    context = {
        'form': form,
        'title': 'New Ticket'
    }

    return render(request, 'reviews/ticket_form.html', context)


@login_required
def ticket_update(request, pk):
    ticket = get_object_or_404(Ticket, id=pk)
    if ticket.user != request.user:
        raise PermissionDenied()

    if request.method == 'POST':
        form = NewTicketForm(request.POST, request.FILES, instance=ticket)

        if form.is_valid():
            form.save()
            messages.success(request, 'Your ticket has been updated!')
            return redirect('reviews-feed')

    else:
        form = NewTicketForm(instance=ticket)

    context = {
        'form': form,
        'title': 'Update Ticket'
    }

    return render(request, 'reviews/ticket_form.html', context)


@login_required
def ticket_detail(request, pk):
    ticket = get_object_or_404(Ticket, id=pk)
    followed_users = get_user_follows(request.user)

    replied_tickets, replied_reviews = get_replied_tickets([ticket])

    context = {
        'post': ticket,
        'title': 'Ticket detail',
        'r_tickets': replied_tickets,
        'r_reviews': replied_reviews,
        'followed_users': followed_users,
    }

    return render(request, 'reviews/post_detail.html', context)


class TicketDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Ticket
    success_url = '/'
    context_object_name = 'post'

    def test_func(self):
        ticket = self.get_object()
        if self.request.user == ticket.user:
            return True
        return False

    def delete(self, request, *args, **kwargs):
        messages.warning(self.request, f'Your ticket "{self.get_object().title}" has been deleted.')
        return super(TicketDeleteView, self).delete(request, *args, **kwargs)
