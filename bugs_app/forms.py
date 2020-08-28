from django import forms
from bugs_app.models import CustomUser


class LogInForm(forms.Form):
    username = forms.CharField(max_length=20)
    password = forms.CharField(widget=forms.PasswordInput)
    # name = forms.CharField(max_length=20)


class AddTicketForm(forms.Form):
    title = forms.CharField(max_length=50)
    # time = forms.DateTimeField()
    description = forms.CharField(widget=forms.Textarea, max_length=150)
    # user_filed = forms.CharField(max_length=50)
    # assigned_choices = [(name, name) for name in CustomUser.objects.all()]
    # user_assigned = forms.ChoiceField(choices=assigned_choices)
    # user_completed = forms.CharField(max_length=50)
    # ticket_status_choices = [("New", "New"), ("In_Progress", "In_Progress"),
    #                          ("Done", "Done"), ("Invalid", "Invalid")]
    # ticket_status = forms.ChoiceField(choices=ticket_status_choices)


class EditTicketForm(forms.Form):
    title = forms.CharField(max_length=50)
    description = forms.CharField(widget=forms.Textarea, max_length=150)
    ticket_status_choices = [("New", "New"), ("In_Progress", "In_Progress"),
                             ("Done", "Done"), ("Invalid", "Invalid")]
    ticket_status = forms.ChoiceField(choices=ticket_status_choices)
    # user_assigned = forms.CharField(max_length=50)
    assigned_choices = [(name, name)
                        for name in CustomUser.objects.all()]
    user_completed = forms.ChoiceField(
        choices=assigned_choices, required=False)
    user_assigned = forms.ChoiceField(choices=assigned_choices, required=False)
