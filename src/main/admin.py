import csv
import sys

from django.contrib import admin, messages
from django.db.models import Q
from django.forms.models import BaseInlineFormSet
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.template.defaultfilters import time
from django.urls import path

from adminsortable2.admin import SortableAdminMixin
from solo.admin import SingletonModelAdmin

from main.services import Schedule

from .forms import GroupsForm
from .models import Team, Group, Match, SiteConfiguration, TeamForbiddenSlot


class TeamForbiddenSlotInline(admin.TabularInline):
    model = TeamForbiddenSlot
    extra = 1


class MatchInlineFormSet(BaseInlineFormSet):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.queryset = Match.objects.filter(
            Q(home_team=self.instance)
            | Q(away_team=self.instance))


class MatchInline(admin.TabularInline):
    model = Match
    fk_name = 'home_team'
    formset = MatchInlineFormSet
    extra = 0
    fields = [
        'name',
        'home_team',
        'home_team_points',
        'away_team',
        'away_team_points',
        'match_type',
        'get_start_time',
        'get_field',
    ]

    readonly_fields = [
        'get_start_time',
        'get_field',
    ]

    def has_change_permission(self, request, obj=None):
        return False

    def has_add_permission(self, request, obj):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = [
        '__str__',
        'category',
        'modality',
        'group',
        'points',
        'points_against',
        'games_played',
        'games_won',
        'games_lost',
        'competition_points',
    ]

    inlines = [
        # TeamForbiddenSlotInline,
        MatchInline,
    ]

    readonly_fields = [
        'points',
        'points_against',
        'games_played',
        'games_won',
        'games_lost',
        'competition_points',
    ]

    list_filter = [
        'category',
        'modality',
        'group',
    ]

    search_fields = [
        'name',
    ]

    actions = ['add_teams']

    def add_teams(self, request, queryset):
        if queryset.count() < 3:
            self.message_user(
                request,
                "No es pot crear un grup amb menys de 3 equips",
                level=messages.ERROR,
            )
            return HttpResponseRedirect(request.get_full_path())

        form = None

        if 'post' in request.POST:
            form = GroupsForm(request.POST)

            if form.is_valid():
                group = form.cleaned_data['group']

                queryset.update(group=group)

                self.message_user(request, "Grups afegits correctament")

                return HttpResponseRedirect(request.get_full_path())

        if not form:
            form = GroupsForm(
                initial={'_selected_action': request.POST.getlist(admin.ACTION_CHECKBOX_NAME)}
            )

        return render(
            request,
            'main/admin/add_teams.html',
            context={
                **self.admin_site.each_context(request),
                'form': form,
                'teams': queryset,
                'back_url': request.get_full_path(),
            }
        )
    add_teams.short_description = "Afegir equips seleccionats a un grup"


class TeamInline(admin.TabularInline):
    model = Team
    extra = 1

    fields = [
        'name',
        'category',
        'modality',
        'points',
        'points_against',
        'games_played',
        'games_won',
        'games_lost',
    ]

    def has_add_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False


@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    list_display = [
        '__str__',
        'competition_type',
    ]

    list_filter = [
        'competition_type',
    ]

    search_fields = [
        'name',
    ]

    inlines = [
        TeamInline,
    ]


@admin.register(Match)
class MatchAdmin(SortableAdminMixin, admin.ModelAdmin):
    change_list_template = "main/admin/matches_changelist.html"
    list_per_page = sys.maxsize

    list_display = [
        '__str__',
        'get_start_time',
        'get_game_field',
        'get_score',
        'get_group',
        'my_order',
        'match_type',
    ]

    search_fields = [
        'name',
        'home_team__name',
        'away_team__name',
    ]

    actions = [
        'export_as_csv',
    ]

    list_filter = [
        'match_type',
    ]

    fields = [
        'name',
        'match_type',
        'home_team',
        'home_team_points',
        'away_team',
        'away_team_points',
        'get_group',
        'get_start_time',
        'get_game_field',
    ]

    readonly_fields = [
        'get_group',
        'get_start_time',
        'get_game_field',
    ]

    def get_group(self, obj: Match):
        return obj.group or "-"
    get_group.short_description = "Grup"

    def get_start_time(self, obj: Match):
        return time(obj.get_start_time(), "H:i")
    get_start_time.short_description = "Hora de joc"

    def get_game_field(self, obj: Match):
        return obj.get_field()
    get_game_field.short_description = "Pista"

    def get_score(self, obj: Match):
        return obj.get_score()
    get_score.short_description = "Resultat"

    def get_urls(self):
        urls = super().get_urls()

        my_urls = [
            path('schedule/', self.create_schedule),
        ] + urls

        return my_urls

    def create_schedule(self, request):
        if Match.objects.all().exists():
            self.message_user(request, "Ja hi ha partits creats", level=messages.ERROR)
        else:
            Schedule().create_schedule()
            self.message_user(request, "S'han creat tots els partits")

        return HttpResponseRedirect("../")

    def export_as_csv(self, request, queryset):
        meta = self.model._meta
        field_names = [field.name for field in meta.fields]

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename={}.csv'.format(meta)
        writer = csv.writer(response)

        writer.writerow(field_names)
        for obj in queryset:
            writer.writerow([getattr(obj, field) for field in field_names])

        return response
    export_as_csv.short_description = "Exportar a CSV"


admin.site.register(SiteConfiguration, SingletonModelAdmin)
