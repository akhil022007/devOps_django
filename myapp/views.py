from django.shortcuts import render

def home(request):
    # This will render the 'taj_mahal.html' template
    return render(request, 'myapp/taj_mahal.html')
