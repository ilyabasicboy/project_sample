# -*- coding: utf-8 -*-
from django.shortcuts import render
from .forms import ReviewForm
from .models import Review


def reviews_list(request):

    template = "reviews/review_list.html"
    form = ReviewForm()
    data = {
        'form': form,
        'review_list': Review.objects.filter(show=True).order_by('-date')
    }
    return render(request, template, data)


def submit_review(request):
    if request.method == "POST":
        form = ReviewForm(request.POST, request.FILES)
        if form.is_valid():
            question = form.save()
            form.mail(request)
            return render(request, 'reviews/thankyou.html', {'form': form})
    else:
        form = ReviewForm()
    return render(request, 'reviews/feedback.html', {'form':form})