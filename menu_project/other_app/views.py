from django.shortcuts import render

def other_index(request, args=''):
    return render(request, 'index.html')
