from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse


def index(request):
    """ initial game page"""
    return HttpResponse("Hello, world. You're at the polls index.")



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
