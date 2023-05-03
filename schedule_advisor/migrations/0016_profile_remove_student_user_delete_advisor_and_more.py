# Generated by Django 4.1.7 on 2023-04-25 15:23

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('schedule_advisor', '0015_advisor_name_student_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_advisor', models.BooleanField(default=False)),
                ('advisor', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='advisee', to=settings.AUTH_USER_MODEL)),
                ('courses', models.ManyToManyField(to='schedule_advisor.course')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.RemoveField(
            model_name='student',
            name='user',
        ),
        migrations.DeleteModel(
            name='Advisor',
        ),
        migrations.DeleteModel(
            name='Student',
        ),
    ]
