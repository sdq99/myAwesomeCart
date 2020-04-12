from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.core.validators import MaxValueValidator

class contactForm(forms.Form):
    name = forms.CharField(label='Your name :', max_length=50, help_text='10 characters max.', required=False)
    email = forms.EmailField(label='Your Email :', max_length=50)
    phone = forms.IntegerField(label='Your Phone :', validators=[MaxValueValidator(10)])
    msg = forms.CharField(label="How May We Help You :", widget=forms.Textarea(attrs={'id':'msg_field'} ))


class userRegistration(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    last_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2',)