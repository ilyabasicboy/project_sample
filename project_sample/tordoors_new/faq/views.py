# -*- coding: utf-8 -*-
from django.shortcuts import render
from tordoors_new.faq.models import FaqQuestion, FaqTheme
from tordoors_new.faq.forms import FaqQuestionForm


# отдать список вопросов/ответов
def faq_list(request):
    themes = FaqTheme.objects.all().order_by('order_key')
    questions_by_themes = []
    form = FaqQuestionForm()
    for theme in themes:
        questions = FaqQuestion.objects.filter(theme=theme, show=True).exclude(answer='').order_by('order_key')
        if questions:
            questions_by_themes.append((theme, questions))
    context = {
                'questions_by_themes': questions_by_themes,
                'form': form
               }
    template = 'faq/questions_list.html'
    return render(request, template, context)


def faq_feedback_view(request):
    if request.method == "POST":
        form = FaqQuestionForm(request.POST)
        if form.is_valid():
            template = 'faq/faq_thankyou.html'
            question = form.save()
            question.order_key = question.pk
            question.save()
            form.mail(request)
            return render(request, template, {'form': form})
    else:
        form = FaqQuestionForm()

    template = 'faq/faq_feedback.html'
    return render(request, template, {'form': form})
