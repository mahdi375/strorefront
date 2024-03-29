from django.contrib import admin
from .models import TaggedItem, Tag


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    search_fields = ['lable']
