from django import forms

class GetDataSet(forms.Form):
    fileInput = forms.FileField()