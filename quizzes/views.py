from django.http import HttpResponse
from django.shortcuts import render

from .models import Question, Answer


def home_page(request):
    result = ''
    question_number = 1
    if request.method == 'POST':
        answer = request.POST.get('answer', False)
        question_number += request.POST.get('question_number', 1)
        if (answer == "John"):
            result = 'Correct!'
        else:
            result = 'Wrong!'

    question = Question.objects.get(pk=question_number)

    answers = Answer.objects.filter(question=question)

    answer_texts = []

    for a in answers:
        answer_texts.append(a.text)

    return render(
        request,
        'home.html',
        {
            'result': result,
            'question_number': question_number,
            'question_text': question.text,
            'answers': answer_texts
        }
    )
