from django import forms

from .models import Group


class GroupsForm(forms.Form):
    # _selected_action = forms.CharField(widget=forms.MultipleHiddenInput)
    groups = forms.ModelChoiceField(
        label="Gups",
        queryset=Group.objects,
    )
