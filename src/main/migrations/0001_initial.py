# Generated by Django 2.2.1 on 2019-05-25 08:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Field',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Nom')),
                ('for_finals', models.BooleanField(default=False, verbose_name='Per jugar finals')),
            ],
        ),
        migrations.CreateModel(
            name='Group',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Nom')),
                ('category', models.CharField(choices=[('inf', 'Infantil'), ('cad', 'Cadet'), ('abs', 'Absoluta')], max_length=255, verbose_name='Categoria')),
                ('modality', models.CharField(choices=[('masc', 'Masculina'), ('fem', 'Femenina'), ('mix', 'Mixta')], max_length=255, verbose_name='Modalitat')),
            ],
        ),
        migrations.CreateModel(
            name='Team',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Nom')),
                ('category', models.CharField(choices=[('inf', 'Infantil'), ('cad', 'Cadet'), ('abs', 'Absoluta')], max_length=255, verbose_name='Categoria')),
                ('modality', models.CharField(choices=[('masc', 'Masculina'), ('fem', 'Femenina'), ('mix', 'Mixta')], max_length=255, verbose_name='Modalitat')),
                ('points', models.PositiveIntegerField(default=0, verbose_name='Punts a favor')),
                ('points_against', models.PositiveIntegerField(default=0, verbose_name='Punts en contra')),
                ('games_played', models.PositiveIntegerField(default=0, verbose_name='Partits jugats')),
                ('games_won', models.PositiveIntegerField(default=0, verbose_name='Partits guanyats')),
                ('games_lost', models.PositiveIntegerField(default=0, verbose_name='Partits perduts')),
                ('group', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='main.Group', verbose_name='Grup')),
            ],
            options={
                'verbose_name': 'Equip',
            },
        ),
        migrations.CreateModel(
            name='Match',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Nom')),
                ('home_team_points', models.PositiveIntegerField(default=0, verbose_name='Punts equip local')),
                ('away_team_points', models.PositiveIntegerField(default=0, verbose_name='Punts equip visitant')),
                ('start_time', models.DateTimeField()),
                ('away_team', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='games_as_away_team', to='main.Team', verbose_name='Equip visitant')),
                ('game_field', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='main.Field', verbose_name='Pista')),
                ('home_team', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='games_as_home_team', to='main.Team', verbose_name='Equip local')),
            ],
        ),
    ]
