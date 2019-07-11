from django.urls import path

from . import views

app_name = 'generator'
urlpatterns = [
    path('', views.index, name='index'),
    path('new', views.new, name='new'),
    path('book/<int:book_id>', views.edit, name='edit'),
]
