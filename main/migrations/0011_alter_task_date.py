# Generated by Django 4.2.7 on 2023-12-25 23:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0010_remove_date_users_date_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='date',
            field=models.DateField(auto_now_add=True, null=True),
        ),
    ]
