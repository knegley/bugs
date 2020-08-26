from django import forms


class LogInForm(forms.Form):
    username = forms.CharField(max_length=20)
    password = forms.CharField(widget=forms.PasswordInput)
    name = forms.CharField(max_length=20)


class AddTicketForm(forms.Form):
    test = forms.CharField()
