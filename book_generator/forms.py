from django.forms import ModelForm, SelectDateWidget
from .models import Book

class NewBookForm(ModelForm):
    class Meta:
        model = Book
        fields = '__all__'
        widgets = {
            'start': SelectDateWidget(),
            'end': SelectDateWidget(),
        }

    def process(self):
        book = self.save(commit=False)
        # commit=False tells Django that "Don't send this to database yet.
        # I have more things I want to do with it."

        book.save() # Now you can send it to DB
