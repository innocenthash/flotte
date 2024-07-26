# forms.py
from django import forms

from compte.models import ImageUser


class ImageUserForm(forms.ModelForm):
    class Meta:
        model = ImageUser
        fields = ['profil']
