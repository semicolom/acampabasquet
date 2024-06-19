# Generated by Django 3.2.25 on 2024-06-12 15:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0012_teamforbiddenslot_alter_group_options_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='SiteConfiguration',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('available_fields', models.PositiveSmallIntegerField(default=2)),
                ('start_datetime', models.DateTimeField(default='2024-06-21 19:00')),
                ('match_length', models.PositiveSmallIntegerField(default=20, help_text='En minuts')),
            ],
            options={
                'verbose_name': 'Configuració',
            },
        ),
    ]