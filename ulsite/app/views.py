from django.shortcuts import render
from django.http import JsonResponse
from .models import Area, Region, Quest

def quest_homepage_list(request):
    areas = Area.objects.all().order_by("id")
    regions = Region.objects.all().order_by("id")
    quests = Quest.objects.all().order_by("id")
    return render(request, "areas.html", {"areas": areas,
                                          "regions": regions,
                                          "quests": quests})

def homepage(request):
    return render(request, "homepage.html")