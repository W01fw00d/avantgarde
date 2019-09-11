from django.urls import path

from . import views

app_name = 'book_generator'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('book/<int:pk>', views.DetailView.as_view(), name='edit'),
    path('new', views.new, name='new'),
]
