# Generated by Django 4.1.3 on 2023-01-07 22:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0006_alter_question_creation_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='avatar',
            field=models.ImageField(blank=True, default='static/img/avatar-1.png', null=True, upload_to='avatar/img/%Y.%m/%d/'),
        ),
        migrations.AlterField(
            model_name='tag',
            name='tag_name',
            field=models.CharField(max_length=25),
        ),
    ]
