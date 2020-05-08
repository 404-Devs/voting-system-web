from django import forms
from django.forms import ModelForm
from api.models import Voter

class VoterRegistrationForm(ModelForm):
    class Meta:
        model = Voter
        fields = '__all__'