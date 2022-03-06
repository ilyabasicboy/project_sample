from tordoors_new.faq.views import faq_list, faq_feedback_view
from django.conf.urls import url


urlpatterns = [
    url(r'^$', faq_list, name='faq_list'),
    url(r'^faq_feedback_ajax/$', faq_feedback_view, name='ajax_faq_feedback'),
]
