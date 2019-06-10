from django.db.models import Q
from django.views.generic import DetailView, TemplateView

from .models import Team, Group, Match


class HomeView(TemplateView):
    template_name = 'main/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['matches'] = Match.objects.all()
        return context


class GroupsView(TemplateView):
    template_name = 'main/groups.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['groups'] = Group.objects.all()
        return context


class GroupDetailView(DetailView):
    model = Group

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['matches'] = Match.objects.filter(
            Q(home_team__group=self.object) | Q(away_team__group=self.object)
        )
        return context


class TeamView(DetailView):
    model = Team

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['matches'] = Match.objects.filter(
            Q(home_team=self.object) | Q(away_team=self.object)
        )
        return context
