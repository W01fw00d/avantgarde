from django import forms
from django.forms import ModelForm, SelectDateWidget

from django.contrib.auth.models import User
from .models import Book, Rule
from .enums.book_jobs import BookJobs

from django.utils.safestring import mark_safe

import random
import ast
import datetime
from random import shuffle


# Making custom version of CheckboxSelectMultiple with horizontal style
class HorizontalCheckboxSelectMultiple(forms.CheckboxSelectMultiple):
    def render(self, *args, **kwargs):
        output = super(
            HorizontalCheckboxSelectMultiple,
            self
        ).render(*args, **kwargs)
        return mark_safe(
            output
            .replace(u'<ul>', u'')
            .replace(u'</ul>', u'')
            .replace(u'<li>', u'<p style="display: initial">')
            .replace(u'</li>', u'</p>')
        )


class NewBookForm(ModelForm):
    class Meta:
        model = Book
        fields = '__all__'
        widgets = {
            'start': SelectDateWidget(),
            'end': SelectDateWidget(),
        }

    def addaptParticipantChoices(self, participants):
        choices = self.fields['participant'].choices
        if participants and choices:
            for participant in participants:
                participant_dict = ast.literal_eval(participant['participant'])
                if choices:
                    choices.remove(
                        (participant_dict, participant_dict['name']))

        self.fields['participant'].choices = choices

    number = forms.IntegerField(
        label='Number:', required=False, widget=forms.NumberInput()
    )
    rounds = forms.IntegerField(
        label='Rounds:', required=False, widget=forms.NumberInput()
    )

    rules_choices = [
        ({"id": rule.id, "name": rule.name}, rule.name)
        for rule in Rule.objects.all()
    ]
    rules = forms.MultipleChoiceField(
        widget=HorizontalCheckboxSelectMultiple,
        choices=rules_choices,
        required=False
    )

    user_choices = [
        ({"id": user.id, "name": user.username}, user.username)
        for user in User.objects.all()
    ]
    participant = forms.ChoiceField(
        widget=forms.Select, choices=user_choices, required=False)

    job_choices = [(job.name, job.value) for job in BookJobs]
    jobs = forms.MultipleChoiceField(
        widget=HorizontalCheckboxSelectMultiple,
        choices=job_choices,
        required=False
    )

    def process(self, participants):
        # print('form: ', self.cleaned_data)
        # print('participants: ', participants)

        if participants:
            print('all participants: ', participants)
            available_participants = participants

            for rule in self.cleaned_data['rules']:
                # If there are still rules but no participants, refill the list
                if not available_participants:
                    available_participants = participants
                rule_participant = random.choice(available_participants)
                available_participants.remove(rule_participant)
                print(rule, ' will be chosen by ', rule_participant)

            writers = []
            for participant in participants:
                if 'WRITER' in participant['jobs']:
                    writers.append(participant)

            chapters = []
            for round in range(0, self.cleaned_data['rounds']):
                number = 1
                available_writers = writers
# First writter would be somebody who hasn't chosen any rule, if possible
                if round == 0:
                    chapter_writer = None

                    while not chapter_writer and available_participants:
                        chapter_writer = random.choice(available_participants)
                        available_participants.remove(chapter_writer)

                        if 'WRITER' not in chapter_writer['jobs']:
                            chapter_writer = None

                    # writer_dict = ast.literal_eval(
                    #     chapter_writer['participant']
                    # )
                    # start_date = datetime.datetime.strptime(
                    #     self.cleaned_data['start'],
                    #     '%Y-%m-%d'
                    # )

                    chapters.append(
                        self.generateRandomChapter(number, chapter_writer)
                    )
                    number += 1

                    # Remove first chapter writer
                    if chapter_writer:
                        available_writers.remove(chapter_writer)

                print('available_writers', available_writers)
                shuffle(available_writers)
                for writer in available_writers:
                    chapters.append(
                        self.generateRandomChapter(number, writer)
                    )
                    number += 1

        print('chapters: ', chapters)

        # book = self.save(commit=False)
        # commit=False tells Django that "Don't send this to database yet.
        # I have more things I want to do with it."
        # book.save() # Now you can send it to DB

    def generateRandomChapter(self, number, writer):
        start_date = self.cleaned_data['start']
        # Hardcoded to 1 week, should be on Book model as chapter_time
        one_week_on_days = 7
        one_week = datetime.timedelta(days=one_week_on_days)
        end = start_date + one_week

        return {
            'number': number,
            'writter': writer['participant'],
            'start': self.cleaned_data['start'],
            'end': end,
        }
