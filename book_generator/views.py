from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.views import generic

from .models import Book
from .forms import NewBookForm

import json

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
            form.fields['jobs'].required = True

            if form.is_valid():
                if 'participants' not in request.session:
                    request.session['participants'] = []

                new_participant = {
                    'participant': form.cleaned_data['participant'],
                    'jobs': form.cleaned_data['jobs'],
                }

                if (new_participant not in request.session['participants']):
                    request.session['participants'].append(new_participant)
                    request.session.modified = True

        elif 'save' in request.POST:
            form.fields['number'].required = True
            form.fields['title'].required = True
            form.fields['rounds'].required = True
            form.fields['start'].required = True
            form.fields['end'].required = True

            # ## Debug mock
            def mock_form_data(request, form):
                def is_valid_mocked():
                    return True

                form.is_valid = is_valid_mocked

                form.cleaned_data = json.loads(
                    '{"number": 1,"title": "Fake Book", "rounds": 1, "start": "", "end": "", "rules": [], "participant": "", "jobs": []}'
                )
                form.cleaned_data['rules'] = json.loads(
                    '[{"id": 0, "name": "Character"}, {"id": 1, "name": "Theme"}, {"id": 2, "name": "Restriction"}]'
                )
                request.session['participants'] = json.loads(
                    '[{"participant": {"id": 1, "name": "Gabo"}, "jobs": ["WRITER", "DIRECTOR"]}, {"participant": {"id": 2, "name": "JPM"}, "jobs": ["WRITER", "ILLUSTRATOR"]}, {"participant": {"id": 3, "name": "JJ"}, "jobs": ["WRITER", "ILLUSTRATOR"]}, {"participant": {"id": 4, "name": "Navi"}, "jobs": ["WRITER"]}, {"participant": {"id": 5, "name": "LuisB"}, "jobs": ["WRITER"]}, {"participant": {"id": 6, "name": "LluisG"}, "jobs": ["WRITER"]}, {"participant": {"id": 7, "name": "Ángela"}, "jobs": ["ILLUSTRATOR"]}, {"participant": {"id": 8, "name": "Sara"}, "jobs": ["ILLUSTRATOR"]}, {"participant": {"id": 9, "name": "Aina"}, "jobs": ["ILLUSTRATOR"]}, {"participant": {"id": 10, "name": "Marta"}, "jobs": ["WRITER"]}, {"participant": {"id": 11, "name": "Albert"}, "jobs": ["WRITER"]}, {"participant": {"id": 12, "name": "Isis"}, "jobs": ["WRITER", "ILLUSTRATOR"]}, {"participant": {"id": 13, "name": "Xisca"}, "jobs": ["WRITER"]}]'
                )

            mock_form_data(request, form)
            # ## Debug mock

            # All fields are valids and there're chosen participants
            if form.is_valid() and request.session['participants']:
                participants = request.session['participants']
                request.session['participants'] = []
                request.session.modified = True
                form.process(participants)
                # return HttpResponseRedirect(reverse('book_generator:index'))

    else:
        form = NewBookForm()
        request.session['participants'] = []

    form.fields['number'].required = False
    form.fields['title'].required = False
    form.fields['rounds'].required = False
    form.fields['start'].required = False
    form.fields['end'].required = False
    form.fields['jobs'].required = False

    # Review if choices are already chosen on form participant field
    form.addaptParticipantChoices(request.session['participants'])

    if not form.fields['participant'].choices:
        are_choices_left = False
    else:
        are_choices_left = True
    #

    return render(
        request,
        'book/new.html',
        {
            'form': form,
            'are_choices_left': are_choices_left
        }
    )
