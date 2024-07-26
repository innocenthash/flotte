from django import forms

from card.models import Card
from compte.models import User
from .models import UserWithFlotte

class UserWithFlotteUserAdminForm(forms.ModelForm):
    class Meta:
        model = UserWithFlotte
        fields = '__all__'
    

    def __init__(self, *args, **kwargs):
        super(UserWithFlotteUserAdminForm, self).__init__(*args, **kwargs)
        self.fields['card'].queryset = Card.objects.filter(userwithflotte__isnull=True)
        self.fields['user'].queryset = User.objects.filter(userwithflotte__isnull=True)