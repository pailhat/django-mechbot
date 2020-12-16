from django.forms import ModelForm, TextInput
from .models import Alert



class AlertForm(ModelForm):
    class Meta:
        model = Alert
        fields = ('origin','has','wants',)
        labels = {
            "origin": "Origin",
            "has": "Has [H]",
            "wants": "Wants [W]",
        }
        widgets = {
            'origin': TextInput(attrs={'class': 'input is-primary'}),
            'has': TextInput(attrs={'class': 'input is-primary'}),
            'wants': TextInput(attrs={'class': 'input is-primary'}),
        }
class AlertFormUpdate(ModelForm):
    class Meta:
        model = Alert
        fields = ('origin','has','wants','enabled')
        labels = {
            "origin": "Origin",
            "has": "Has [H]",
            "wants": "Wants [W]",
            "enabled": "Enabled",
        }
        widgets = {
            'origin': TextInput(attrs={'class': 'input is-primary'}),
            'has': TextInput(attrs={'class': 'input is-primary'}),
            'wants': TextInput(attrs={'class': 'input is-primary'}),
        }