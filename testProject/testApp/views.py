from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
def index(request):
    return HttpResponse("Hello ! " +request.POST["custom_person_name_display"]+ " Welcome to CS480A6 Computer Science Education Course "  + " Your enrollment state is : " + request.POST["custom_enrollment_state"])
    
