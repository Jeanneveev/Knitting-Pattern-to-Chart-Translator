from django.http.response import HttpResponse
from django.shortcuts import render


# Create your views here.
def input_page(request):
    if request.method == "POST":
        return 

    return render(request, "input.html")