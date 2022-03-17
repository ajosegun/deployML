from django import forms
from .models import Customer, Diabetes

class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = "__all__"

    gender = forms.TypedChoiceField(choices=[('Male', 'Male'), ('Female', 'Female')])
    age = forms.IntegerField()
    salary = forms.IntegerField()

class DiabetesForm(forms.ModelForm):
    class Meta:
        model = Diabetes
        fields = "__all__"

    pregnancies = forms.IntegerField()
    glucose = forms.IntegerField()
    bloodPressure = forms.IntegerField()
    skinThickness = forms.IntegerField()
    insulin = forms.IntegerField()
    bmi = forms.DecimalField()
    diabetesPedigreeFunction = forms.DecimalField()
    age = forms.IntegerField()