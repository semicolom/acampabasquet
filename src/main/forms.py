from django import forms

from .models import Group, Match


class GroupsForm(forms.Form):
    _selected_action = forms.CharField(widget=forms.MultipleHiddenInput)
    group = forms.ModelChoiceField(
        label="Grup",
        queryset=Group.objects.all(),
    )


class MatchForm(forms.ModelForm):
    model = Match

    def clean(self):
        start_time = self.cleaned_data.get('start_time')
        game_field = self.cleaned_data.get('game_field')

        if start_time and game_field:
            if Match.objects.filter(
                start_time=start_time,
                game_field=game_field,
            ).exclude(id=self.instance.id).exists():
                self.add_error(
                    'start_time',
                    error="Ja existeix un partit a aquella hora en aquella pista"
                )
