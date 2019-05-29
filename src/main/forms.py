from django import forms

from .models import Group


class GroupsForm(forms.Form):
    _selected_action = forms.CharField(widget=forms.MultipleHiddenInput)
    group = forms.ModelChoiceField(
        label="Grup",
        queryset=Group.objects.all(),
    )
