from django.forms import ModelForm
from .models import *
class PayOutForm(ModelForm):
    class Meta:
        model = PlayerPayout
        fields = '__all__'


