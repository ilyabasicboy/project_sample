from django.shortcuts import render
from feedback.utils import get_feedback_form
from tordoors_new.reviews.forms import ReviewForm
from tordoors_new.faq.forms import FaqQuestionForm


def ajax_reset_form(request):
    form_key = request.GET.get('form_key')
    if form_key == 'review':
        form = ReviewForm
        templates = ['reviews/feedback.html',]
    elif form_key == 'question':
        form = FaqQuestionForm
        templates = ['faq/faq_feedback.html', ]
    else:
        form = get_feedback_form(form_key)
        templates = ['feedback/%s/feedback.html' % form_key, 'feedback/feedback.html']
    return render(request, templates, {'form': form})