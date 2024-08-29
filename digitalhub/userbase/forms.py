from django import forms
from .models import Company



class CompanyForm(forms.ModelForm):
    class Meta:
        model = Company
        fields = ('company_name', 'address', 'company_website', 'category')

        widgets = {
            'company_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder':'Enter Name'}),
            'address': forms.TextInput(attrs={'class': 'form-control', 'placeholder':'Enter Address'}),
            'company_website': forms.TextInput(attrs={'class': 'form-control', 'placeholder':'Enter Company Website'}),
            'category': forms.Select(attrs={'class': 'form-control', 'placeholder':'Select Company Category'}),
        }