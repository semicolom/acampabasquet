from django.contrib import admin

from . import models


@admin.register(models.Team)
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
    ]

    readonly_fields = [
        'points',
        'points_against',
        'games_played',
        'games_won',
        'games_lost',
    ]

    list_filter = [
        'category',
        'modality',
        'group',
    ]

    search_fields = [
        'name',
    ]


@admin.register(models.Group)
class GroupAdmin(admin.ModelAdmin):
    list_display = [
        '__str__',
        'category',
        'modality',
    ]

    list_filter = [
        'category',
        'modality',
    ]

    search_fields = [
        'name',
    ]


@admin.register(models.Field)
class FieldAdmin(admin.ModelAdmin):
    list_display = [
        '__str__',
        'for_finals',
    ]


@admin.register(models.Match)
class MatchAdmin(admin.ModelAdmin):
    list_display = [
        '__str__',
        'home_team',
        'home_team_points',
        'away_team',
        'away_team_points',
        'start_time',
        'game_field',
    ]

    list_filter = [
        'game_field',
    ]

    search_fields = [
        'name',
        'home_team__name',
        'away_team__name',
    ]
