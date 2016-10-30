from django.http import HttpResponse
from django.shortcuts import render

from .models import Question


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

    return render(
        request,
        'home.html',
        {
            'result': result,
            'question_number': question_number,
            'question_text': Question.objects.get(pk=question_number).text
        }
    )
