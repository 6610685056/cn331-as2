from django.http.response import HttpResponse
from django.shortcuts import render

# Create your views here.


def subjects(request):
    return render(request, 'RegCN/MySubjects.html')

def subject(request, subject_id):
    return HttpResponse('subject ID= ' + str(subject_id))
