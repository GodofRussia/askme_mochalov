# Generated by Django 4.1.3 on 2022-12-23 21:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_answer_rating_question_rating'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='creation_date',
            field=models.DateField(),
        ),
    ]
