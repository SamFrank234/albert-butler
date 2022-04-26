from typing import final
from django.shortcuts import render
import json
from django.contrib.auth.models import User #####
from django.http import JsonResponse , HttpResponse ####
from .models import RateMyProfRatings

def index(request):
    professors = RateMyProfRatings.objects.all()
    context={
        'professors' : professors
    }
    return render(request, 'index.html', context)


def get_prof_rating(request):
    
    f_name = request.GET.get('first')
    l_name = request.GET.get('last')

    print(request.GET)
    print(f_name)
    print(l_name)


    professors = RateMyProfRatings.objects.all()
    finalprof = None

    for professor in professors:
        if (l_name == professor.last_name):
            print("success")
            finalprof = professor
            break

    if(finalprof == None):
        data = {
            'rating': 'none',
            'no_of_ratings': 0,
        }
    else:
        data = {
            'first_name': finalprof.first_name,
            'last_name': finalprof.last_name,
            'rating': finalprof.rating,
            "no_of_ratings": finalprof.no_of_ratings,
        }

    #print('json-data to be sent: ', data)

    return JsonResponse(data)

