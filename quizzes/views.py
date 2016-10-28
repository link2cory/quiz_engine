from django.http import HttpResponse
from django.shortcuts import render


def home_page(request):
    result = ''
    if request.method == 'POST':
        answer = request.POST.get('answer', False)
        if (answer == "John"):
            result = 'Correct!'
        else:
            result = 'Wrong!'
    return render(request, 'home.html', {'result': result})
