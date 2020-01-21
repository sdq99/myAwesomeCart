from django import forms
from django.core.validators import MaxValueValidator

class contactForm(forms.Form):
    name = forms.CharField(label='Your name :', max_length=50, help_text='10 characters max.', required=False)
    email = forms.EmailField(label='Your Email :', max_length=50)
    phone = forms.IntegerField(label='Your Phone :', validators=[MaxValueValidator(10)])
    msg = forms.CharField(label="How May We Help You :", widget=forms.Textarea(attrs={'id':'msg_field'} ))