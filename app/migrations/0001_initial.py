# Generated by Django 4.1.3 on 2022-12-20 12:58

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Answer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('login', models.CharField(max_length=30)),
                ('avatar', models.ImageField(blank=True, default='static/img/avatar-1.png', null=True, upload_to='')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50)),
                ('text', models.TextField(max_length=200)),
                ('creation_date', models.DateField(auto_now_add=True)),
                ('profile', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='questions', to='app.profile')),
            ],
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tag_name', models.CharField(max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='QuestionRating',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.BooleanField()),
                ('profile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='questionRatings', to='app.profile')),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='questionRatings', to='app.question')),
            ],
        ),
        migrations.AddField(
            model_name='question',
            name='tag',
            field=models.ManyToManyField(blank=True, related_name='questions', to='app.tag'),
        ),
        migrations.CreateModel(
            name='AnswerRating',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.BooleanField()),
                ('answer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='answerRatings', to='app.answer')),
                ('profile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='answerRatings', to='app.profile')),
            ],
        ),
        migrations.AddField(
            model_name='answer',
            name='profile',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='answers', to='app.profile'),
        ),
        migrations.AddField(
            model_name='answer',
            name='question',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='answers', to='app.question'),
        ),
        migrations.AddConstraint(
            model_name='questionrating',
            constraint=models.UniqueConstraint(fields=('question', 'profile'), name='unique_question'),
        ),
        migrations.AddConstraint(
            model_name='answerrating',
            constraint=models.UniqueConstraint(fields=('answer', 'profile'), name='unique_answer'),
        ),
    ]