from django.shortcuts import render
from django.http import HttpResponse
#from .models import Game


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


def home(request):
    """ initial game page"""
    context = {
        'posts': posts
    }
    return render(request, 'game/home.html', context)


def about(request):
    return render(request, 'game/about.html', {'title': 'About'})


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

def next(request):
    #student = User.objects.get(username = request.user).student
    # player = get request.user pleyari
    # game = playerin game objesi 
    # game.takeAction(player)
    # if action == roll <- bunu nerden cekcez
    #       game.takeAction(player)
    # game.current_player = getNextPlayer
    pass
