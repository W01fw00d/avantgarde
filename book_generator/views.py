from django.http import HttpResponse, Http404
# from django.template import loader
from django.shortcuts import render, get_object_or_404

from .models import Book


def index(request):
    book_list = Book.objects.order_by('start')
    context = {'book_list': book_list,}
    # template = loader.get_template('book/index.html')
    # return HttpResponse(template.render(context, request))
    return render(request, 'book/index.html', context)

def new(request):
    return HttpResponse("You can start a new Exquisite Corpse Book here.")

def edit(request, book_id):
    # return HttpResponse("You can edit book " + str(book_id) + " here.")
    book = get_object_or_404(Book, pk=book_id)

    return render(request, 'book/edit.html', {'book': book})
