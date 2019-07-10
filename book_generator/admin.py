from django.contrib import admin

from .models import Rule, Book, BookPartaker, BookRule, Chapter, ChapterPartaker

admin.site.register(Rule)
admin.site.register(Book)
admin.site.register(BookPartaker)
admin.site.register(BookRule)
admin.site.register(Chapter)
admin.site.register(ChapterPartaker)
