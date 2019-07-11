from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.views import generic

from .models import Book

class IndexView(generic.ListView):
    template_name = 'book/index.html'
    context_object_name = 'book_list'

    def get_queryset(self):
        """Return all books."""
        return Book.objects.order_by('start')

class DetailView(generic.DetailView):
    model = Book
    template_name = 'book/edit.html'

def new(request):
    return HttpResponse("You can start a new Exquisite Corpse Book here.")

# def save_new(request, book):
#     book = request.POST['book']
#     book.save()
#
#     return HttpResponseRedirect(reverse('book:index'))
