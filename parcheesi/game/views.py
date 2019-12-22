from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.contrib.auth.models import User
from .models import *
from django.contrib import messages


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

    """ if request.method == 'POST':
        if 'action2' in request.POST:
            return HttpResponseRedirect(reverse('game-home')) """

    player = User.objects.get(username = request.user).player

    allGames = Game.listGames()

    context = {
        'games': allGames
    }
    return render(request, 'game/home.html', context)


@login_required
def join(request, game_id):

    player = User.objects.get(username = request.user).player
    game = player.game #TODO: buraya bakalim tekrardan
    #current_player = game.getCurrentPlayer()
    current_player_id = game.current_player_id
    
    """ if request.method == 'POST':
        if 'roll' in request.POST:
            game.dice 
        elif 'pick' in request.POST:
        elif 'no_pick' in request.POST:
        elif 'next' in request.POST: """    

    context = {
        'game': game,
        'player': player
    }

    return HttpResponseRedirect(reverse('game-detail', args=(game.id,)))

@login_required
def ready(request, game_id):
    player = User.objects.get(username = request.user).player
    game = player.game #TODO: buraya bakalim tekrardan
    #current_player = game.getCurrentPlayer()
    if player.is_ready == False:
        game.ready_player_count += 1
        player.is_ready = True
        game.save()
        player.save()
    
    return HttpResponseRedirect(reverse('game-detail', args=(game.id,)))


@login_required
def action(request, game_id):

    player = User.objects.get(username = request.user).player
    game = player.game #TODO: buraya bakalim tekrardan
    #current_player = game.getCurrentPlayer()
    current_player_id = game.current_player_id
    
    """ if request.method == 'POST':
        if 'roll' in request.POST:
            game.dice 
        elif 'pick' in request.POST:
        elif 'no_pick' in request.POST:
        elif 'next' in request.POST: """    

    context = {
        'game': game,
        'player': player
    }
    if current_player_id != player.pk:
        messages.warning(request, f'This is not your turn! Please wait...') #FIXME: alert
        #return render(request, 'game/detail.html', context)
        return HttpResponseRedirect(reverse('game-detail', args=(game.id,)))



    #return render(request, 'game/detail.html', context)
    return HttpResponseRedirect(reverse('game-detail', args=(game.id,)))

@login_required
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
