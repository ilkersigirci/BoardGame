from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required

from django.contrib.auth.models import User
from .models import *


posts = [
    {
        'author': 'Ilker',
        'title': 'Bolumden Nefret Ediyorum',
        'content': 'First post content',
        'date_posted': 'December 22, 2019'
    },
    {
        'author': 'Onur',
        'title': 'Hem de Coook',
        'content': 'Second post content',
        'date_posted': 'December 22, 2019'
    }
]

@login_required
def home(request):
    """ initial game page"""
    
    player = User.objects.get(username = request.user).player

    allGames = Game.listGames()

    context = {
        'games': allGames
    }
    return render(request, 'game/home.html', context)

def detail(request, game_id):

    player = User.objects.get(username = request.user).player
    game = get_object_or_404(Game, pk = game_id)

    context = {
        'game': game,
        'player': player
    }
    return render(request, 'game/detail.html', context)

@login_required
def about(request):
    return render(request, 'game/about.html', {'title': 'About'})

@login_required
def state(request):
    """ returns the game state """
    '''
    def state(self):
        cells = self.getGameCells()
        gameLog = self.getGameLog()
        players = self.getGamePlayers();
        return
    '''
    pass

@login_required
def next(request):
    #student = User.objects.get(username = request.user).student
    # player = get request.user pleyari
    # game = playerin game objesi 
    # game.takeAction(player)
    # if action == roll <- bunu nerden cekcez
    #       game.takeAction(player)
    # game.current_player = getNextPlayer
    pass
