# -*- coding: utf-8 -*-
from django.contrib import admin
from .models import Review



class ReviewAdmin(admin.ModelAdmin):
    model = Review
    list_display = ('content', 'date', 'show')
    list_editable = ('show',)

admin.site.register(Review, ReviewAdmin)