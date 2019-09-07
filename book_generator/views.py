from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.views import generic

from .models import Book
from .forms import NewBookForm

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
    if request.method == 'POST':
        form = NewBookForm(request.POST)

        if form.is_valid():

            if 'setParticipant' in request.POST:
                form.fields['jobs'].required = True

                print('setParticipant', form.cleaned_data['participant'], form.cleaned_data['jobs'])

            elif 'save' in request.POST:
                form.fields['number'].required = True
                form.fields['title'].required = True
                form.fields['rounds'].required = True
                form.fields['start'].required = True
                form.fields['end'].required = True
                print('save')

                if False:
                    form.process()
                    return HttpResponseRedirect(reverse('generator:index'))
    else:
        form = NewBookForm()

    return render(request, 'book/new.html', {'form': form})
