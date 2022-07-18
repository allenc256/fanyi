from django import forms
from django.core.exceptions import ValidationError

from .models import Entry

class EntryEditForm(forms.ModelForm):
    class Meta:
        model = Entry
        fields = ['difficulty', 'notes']

class EntryVocabForm(forms.Form):
    phrase = forms.CharField(label='Phrase', max_length=1024, required=False)
    translation = forms.CharField(label='Translation', max_length=1024, required=False)

    def clean(self):
        data = super().clean()
        if not data.get('phrase'):
            raise ValidationError('phrase cannot be empty.')
        if not data.get('translation'):
            raise ValidationError('translation cannot be empty.')
