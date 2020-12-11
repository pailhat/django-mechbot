from django.forms import ModelForm
from .models import Alert



class AlertForm(ModelForm):
    class Meta:
        model = Alert
        fields = ('origin','has','wants',)
class AlertFormUpdate(ModelForm):
    class Meta:
        model = Alert
        fields = ('origin','has','wants','enabled')
