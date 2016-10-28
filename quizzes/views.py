from django.http import HttpResponse
from django.shortcuts import render


def home_page(request):
    if request.method == 'POST':
        return HttpResponse('Correct!')
    return render(request, 'home.html')
