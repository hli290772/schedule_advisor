# Generated by Django 4.1.7 on 2023-04-17 16:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('schedule_advisor', '0007_remove_department_abbre_department_abbreviation_and_more'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Department',
            new_name='Subject',
        ),
    ]