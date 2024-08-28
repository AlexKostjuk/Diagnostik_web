from django.forms import ModelForm

from diagn.models import Diagn


class DiagnForm(ModelForm):
    class Meta:
        model = Diagn
        fields = '__all__'