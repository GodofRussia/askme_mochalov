import datetime
import random

from django.contrib.auth.hashers import make_password
from django.core.management.base import BaseCommand, CommandError
from django.db.models import Q

from app import models


def create_users(ratio: int):
    passwords = ['_password1', 'pass2', '2pas3', 'pafd3gwe2eff', 'pafqqfwgg32', 'pfsfqfj23ns', 'flqlg32oigoai',
                 'qqjofqqjof', 'et235lkl2mf', '49fskfknlga']
    logins = ['us_log21', 'user_2login32', 'fqkflkge', 'fewf2gbvc', 'sfqgdbdg2', 'wegweh45gns', 'aggg434ai',
              'qqjfqg323fasf', 'gek235la;vv', '4wggqg543']
    users_to_create = [models.User(username=f'User {user_id}',
                                   password=make_password(passwords[user_id % len(passwords)]),
                                   last_login=datetime.datetime.now()
                                   ) for user_id in range(1, 1 + ratio)]
    models.User.objects.bulk_create(users_to_create)
    first_user_id = models.User.objects.first().id
    profiles_to_create = [models.Profile(user_id=profile_id,
                                         login=logins[profile_id % len(logins)],
                                         avatar=f'static/img/avatar-1.png'
                                         ) for profile_id in range(first_user_id, first_user_id + ratio)]
    models.Profile.objects.bulk_create(profiles_to_create)


def create_tags(ratio: int):
    tags_to_create = [models.Tag(tag_name=f'Tag {tag_id}',
                                 ) for tag_id in range(1, 1 + ratio)]
    models.Tag.objects.bulk_create(tags_to_create)


def create_questions(ratio: int):
    first_profile_id = models.Profile.objects.first().id
    questions_to_create = [models.Question(title=f'Title {question_id}',
                                           text=f'Text {question_id}',
                                           creation_date=datetime.datetime.now(),
                                           profile_id=first_profile_id + question_id % ratio,
                                           ) for question_id in range(ratio * 10)]
    models.Question.objects.bulk_create(questions_to_create)


def create_answers(ratio: int):
    first_profile_id = models.Profile.objects.first().id
    first_question_id = models.Question.objects.first().id
    answers_to_create = [models.Answer(text=f'Text {answer_id}',
                                       profile_id=first_profile_id + answer_id % ratio,
                                       question_id=first_question_id + answer_id % (10 * ratio)
                                       ) for answer_id in range(ratio * 100)]
    models.Answer.objects.bulk_create(answers_to_create)


def create_question_ratings(ratio: int):
    first_profile_id = models.Profile.objects.first().id
    first_question_id = models.Question.objects.first().id
    for profile_ind in range(ratio):
        question_ratings_to_create = [models.QuestionRating(value=bool(rating_id % 2),
                                                            profile_id=first_profile_id + profile_ind,
                                                            question_id=first_question_id + rating_id % (
                                                                    10 * ratio)
                                                            ) for rating_id in range(10 * ratio)]
        models.QuestionRating.objects.bulk_create(question_ratings_to_create)


def create_answer_ratings(ratio: int):
    first_profile_id = models.Profile.objects.first().id
    first_answer_id = models.Answer.objects.first().id
    for profile_ind in range(ratio):
        answer_ratings_to_create = [models.AnswerRating(value=bool(rating_id % 2),
                                                        profile_id=first_profile_id + profile_ind,
                                                        answer_id=first_answer_id + rating_id % (
                                                                100 * ratio)
                                                        ) for rating_id in range(100 * ratio)]
        models.AnswerRating.objects.bulk_create(answer_ratings_to_create)


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('ratio', type=int)

    def handle(self, *args, **options):
        ratio = options['ratio']
        self.stdout.write('Starting users creation', ending='\n')
        create_users(ratio)
        self.stdout.write('Finishing users creation', ending='\n')

        self.stdout.write('Starting tags creation', ending='\n')
        create_tags(ratio)
        self.stdout.write('Finishing tags creation', ending='\n')

        self.stdout.write('Starting questions creation', ending='\n')
        create_questions(ratio)
        self.stdout.write('Finishing questions creation', ending='\n')

        self.stdout.write('Starting answers creation', ending='\n')
        create_answers(ratio)
        self.stdout.write('Finishing answers creation', ending='\n')

        self.stdout.write('Starting ratings creation', ending='\n')
        create_answer_ratings(ratio)
        create_question_ratings(ratio)
        self.stdout.write('Finishing ratings creation', ending='\n')

        tags = models.Tag.objects.all()
        instances = models.Question.objects.all()
        max_tag_number = 3
        for i in range(len(instances)):
            for j in range(random.randint(1, max_tag_number)):
                instances[i].tag.add(random.choice(tags))
