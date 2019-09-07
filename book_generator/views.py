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

        if 'setParticipant' in request.POST:
            # print('setParticipant')

            form.fields['jobs'].required = True

            if form.is_valid():
                if 'participants' not in request.session:
                    request.session['participants'] = []

                request.session['participants'].append({
                    'id': form.cleaned_data['participant'],
                    'jobs': form.cleaned_data['jobs'],
                })
                request.session.modified = True

                for participant in request.session['participants']:
                    print(participant)

        elif 'save' in request.POST:
            form.fields['number'].required = True
            form.fields['title'].required = True
            form.fields['rounds'].required = True
            form.fields['start'].required = True
            form.fields['end'].required = True

            # print('save')

            if form.is_valid():
                print('valid save')

                if False:
                    request.session['participants'] = []
                    request.session.modified = True

                    form.process()
                    return HttpResponseRedirect(reverse('generator:index'))
    else:
        # print('reset')
        form = NewBookForm()
        request.session['participants'] = []

    form.fields['number'].required = False
    form.fields['title'].required = False
    form.fields['rounds'].required = False
    form.fields['start'].required = False
    form.fields['end'].required = False
    form.fields['jobs'].required = False

    return render(request, 'book/new.html', {'form': form})
