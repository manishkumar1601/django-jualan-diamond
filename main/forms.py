from django import forms
from django import forms

class CheckIdForm(forms.Form):
    id = forms.IntegerField()
    server = forms.IntegerField()  


class GeneratePaymentForm(forms.Form):
    userid = forms.IntegerField()
    zoneid = forms.IntegerField()
    nowa = forms.CharField()
    item = forms.CharField()
    payment = forms.CharField()