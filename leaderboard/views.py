from django.shortcuts import render
from .models import Player
from .forms import PlayerForm, VerifyForm
from django.utils.crypto import get_random_string
import django_tables2 as tables
from .tables import PlayerTable
import requests
from datetime import datetime

def join(request):
    form = PlayerForm(request.POST or None)
    username = ""
    url = ""
    flag = ""
    content = ""
    valid = False
    
    # If this is a POST request then process the Form data
    if request.method == 'POST':
        if form.is_valid():
            flag = get_random_string(length=16)
            username = form.cleaned_data['username']
            url = form.cleaned_data['url']
            player = Player.objects.update_or_create(username=username,
            defaults={'url': url, 'flag': flag})

    return render(request, 'leaderboard/join.html',
    context={
        'form': form,
        'flag': flag,
        'username': username,
        'url': url,
        'valid': valid,
    })

def board(request):
    players_done = Player.objects.filter(complete=True)
    table_done = PlayerTable(players_done)
    players_not = Player.objects.filter(complete=False)
    table_not = PlayerTable(players_not)
    return render(request, 'leaderboard/board.html',
    context={
        'table_done': table_done,
        'table_not': table_not
    })

def verify(request):
    url = ""
    flag = ""
    username = ""
    result_message = ""
    not_exist = False
    form = VerifyForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            username = form.cleaned_data['username']
            try:
                player = Player.objects.get(username=username)
            except: # user not exist
                not_exist = True
            else:
                flag = player.flag
                url = player.url
                try:  # Verify the proposed URL
                    response = requests.post(url, "What is tha flag?")
                    content = response.json()
                    if content['flag'] == player.flag:
                        player.complete = True
                        player.complete_time = datetime.now()
                        player.save()
                        result_message = "Microservice response with the right flag!"
                    else:
                        result_message = "Microservice is up, but response with False flag."
                except:
                    result_message = "Microservice does not response."
    return render(request, 'leaderboard/verify.html',
    context = {
        'form': form,
        'not_exist': not_exist,
        'username': username,
        'url': url,
        'flag': flag,
        'result_message': result_message
    })