from django import forms
from django.forms import ModelForm, SelectDateWidget

from django.contrib.auth.models import User
from .models import Book, Rule
from .enums.book_jobs import BookJobs

from django.utils.safestring import mark_safe

import random, ast

# Making custom version of CheckboxSelectMultiple with horizontal style
class HorizontalCheckboxSelectMultiple(forms.CheckboxSelectMultiple):
    def render(self, *args, **kwargs):
        output = super(HorizontalCheckboxSelectMultiple, self).render(*args,**kwargs)
        return mark_safe(output.replace(u'<ul>', u'')
            .replace(u'</ul>', u'')
            .replace(u'<li>', u'<p style="display: initial">')
            .replace(u'</li>', u'</p>'))

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
                print('choices: ', choices)
                print('participant to remove: ', (participant_dict, participant_dict['name']))
                if choices:
                    choices.remove((participant_dict, participant_dict['name']))

        self.fields['participant'].choices = choices

    number = forms.IntegerField(label='Number:', required=False, widget=forms.NumberInput())
    rounds = forms.IntegerField(label='Rounds:', required=False, widget=forms.NumberInput())

    rules_choices = [({"id": rule.id, "name": rule.name}, rule.name) for rule in Rule.objects.all()]
    rules = forms.MultipleChoiceField(widget=HorizontalCheckboxSelectMultiple, choices=rules_choices, required=False)

    user_choices = [({"id": user.id, "name": user.username}, user.username) for user in User.objects.all()]
    participant = forms.ChoiceField(widget=forms.Select, choices=user_choices, required=False)

    job_choices=[(job.name, job.value) for job in BookJobs]
    jobs = forms.MultipleChoiceField(widget=HorizontalCheckboxSelectMultiple, choices=job_choices, required=False)

    def process(self, participants):
        # print('form: ', self.cleaned_data)
        # print('participants: ', participants)

        if participants:
            print('all participants: ', participants)
            rules_participants = participants

            for rule in self.cleaned_data['rules']:
                # If there are still rules but no participants, refill the list
                if not rules_participants:
                    rules_participants = participants
                rule_participant = random.choice(rules_participants)
                rules_participants.remove(rule_participant)
                print(rule, ' will be chosen by ', rule_participant)

        # book = self.save(commit=False)
        # commit=False tells Django that "Don't send this to database yet.
        # I have more things I want to do with it."
        # book.save() # Now you can send it to DB
