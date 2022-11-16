from django.db import models
from django.core.paginator import Paginator
from django.shortcuts import render

# Create your models here.

Questions = [
    {
        'id': question_id,
        'title': 'title' + str(question_id),
        'text': 'text' + str(question_id),
        'answers_count': question_id * question_id,
        'tags': [
            {
                'id': tag_id,
                'tag_name_': 'tag' + str(tag_id),
            } for tag_id in range(3*question_id)
        ],
        'answers': [
            {
                'id': answer_id,
                'text': 'answer text' + str(answer_id),
            } for answer_id in range(question_id * question_id)
        ]
    } for question_id in range(20)
]


def find_questions(tag_name):
    questions = []
    for question_item in Questions:
        tags = question_item.get('tags')
        for tag_item in tags:
            if tag_item.get('tag_name_').__contains__(tag_name) and not questions.__contains__(question_item):
                questions.append(question_item)

    return questions


def paginate(objects_list, request, per_page=10):
    p = Paginator(objects_list, per_page)
    page_number = request.GET.get('page')
    page_object = p.get_page(page_number)

    return page_object
