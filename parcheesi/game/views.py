from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.contrib.auth.models import User
from .models import *
from django.contrib import messages
import random


#######################################################################################
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

#######################################################################################


@login_required
def join(request, game_id):
    player = User.objects.get(username = request.user).player
    game = player.game
    if request.method != 'POST' or 'join' not in request.POST:
        return HttpResponseRedirect(reverse('game-detail', args=(game.id,)))

    player = User.objects.get(username = request.user).player    
    game = Game.getGameById(game_id)    
    
    if player in game.getGamePlayers():
        messages.warning(request, f'You are already joined to this game')
        return HttpResponseRedirect(reverse('game-detail', args=(game.id,)))
        
    elif game.ready_player_count > 0:
        messages.warning(request, f'The game is about to start, you are late!')
        return HttpResponseRedirect(reverse('game-detail', args=(game.id,)))

    player.game = game
    game.player_count += 1
    player.save()
    game.save()

    messages.success(request, f'You are successfully joined the game')    
    return HttpResponseRedirect(reverse('game-detail', args=(game.id,)))

@login_required
def ready(request, game_id):
    player = User.objects.get(username = request.user).player
    game = player.game
    if request.method != 'POST' or 'ready' not in request.POST or game.player_count < 2:
        return HttpResponseRedirect(reverse('game-detail', args=(game.id,)))
    
    if player.is_ready == False:
        game.ready_player_count += 1
        player.is_ready = True
        player.save()
    
    messages.success(request, f'You are ready for the game')
    
    if(game.ready_player_count == game.player_count):
        game.game_status = "Game is started"
        players = game.getGamePlayers()
        player_list = []
        for pl in players:
            player_list.append(pl.id)
        player_list.sort()
        game.current_player = player_list[0]
        game.save()
        
        #TODO: current player index setle
        messages.warning(request, f'Game is Starting')
        
    return HttpResponseRedirect(reverse('game-detail', args=(game.id,)))


@login_required
def game_next(request, game_id):

    player = User.objects.get(username = request.user).player
    game = player.game #TODO: buraya bakalim tekrardan
    #current_player = game.getCurrentPlayer()
    current_player_id = game.current_player_id

    if current_player_id != player.pk:
        messages.warning(request, f'This is not your turn! Please wait...')
        return HttpResponseRedirect(reverse('game-detail', args=(game.id,)))

    if request.method != 'POST':
        return HttpResponseRedirect(reverse('game-detail', args=(game.id,)))
    
    if 'roll' in request.POST:
        if player.next_available_move != "roll":
            msg = "You are in the " + player.next_available_move +" phase!"
            messages.warning(request, msg)
            return HttpResponseRedirect(reverse('game-detail', args=(game.id,)))
        else:
            diceRoll = random.randrange(game.dice) + 1
            #TODO: state change
            #stateChange["actions"].append({"dice roll ": diceRoll})
            log = game.addLog("Dice rolled" + str(diceRoll),player )
            action = Action("jumpR", diceRoll) #FIXME: burada foreign key gg olabilir
            game.takeAction(player, action)
            game.save()
            cell = Cell.objects.get(cell_index=player.current_cell)
            if cell.artifact is not None:
                player.next_available_move = "pick"
                player.save()
            else:
                player.next_available_move = "next"
                player.save()
    elif 'next' in request.POST:
        if player.next_available_move != "next":
            msg = "You are in the " + player.next_available_move +" phase!"
            messages.warning(request, msg)
            return HttpResponseRedirect(reverse('game-detail', args=(game.id,)))
        else:
            cell = Cell.objects.get(cell_index=player.current_cell)
            if cell.action is not None:
                game.takeAction(player, cell.action)
                game.save()
            else:
                pass

            players = game.getGamePlayers()
            player_list = []
            next_player_id = 0
            player_size = 0
            for pl in players:
                player_list.append(pl.id)
                player_size+=1
            player_list.sort()
            for pl_index in range(0,player_size) :
                if player.id == player_list[pl_index]:
                    if pl_index == player_size-1:
                        next_player_id = player_list[0]
                    else:
                        next_player_id = player_list[pl_index+1]
                    


                


            
        #roll the dice

        
    elif 'next' in request.POST:
        if player.next_available_move != "next":
            messages.warning(request, f'You must click to next button!')
            return HttpResponseRedirect(reverse('game-detail', args=(game.id,)))
        
        #next
        
    


    return HttpResponseRedirect(reverse('game-detail', args=(game.id,)))

    """ student = User.objects.get(username = request.user).student
    player = get request.user pleyari
    game = playerin game objesi 
    game.takeAction(player)
    if action == roll <- bunu nerden cekcez
          game.takeAction(player)
    game.current_player = getNextPlayer """

@login_required
def pick(request, game_id):

    player = User.objects.get(username = request.user).player
    game = player.game #TODO: buraya bakalim tekrardan
    current_player_id = game.current_player_id

    if current_player_id != player.pk:
        messages.warning(request, f'This is not your turn! Please wait...')
        return HttpResponseRedirect(reverse('game-detail', args=(game.id,)))
    
    if request.method != 'POST':
        return HttpResponseRedirect(reverse('game-detail', args=(game.id,)))

    if 'pick' in request.POST:
        if player.next_available_move != "pick":
            msg = "You are in the " + player.next_available_move +" phase!"
            messages.warning(request, msg)
            return HttpResponseRedirect(reverse('game-detail', args=(game.id,)))
        
        #pick = True
        player_cell = Cell.objects.get(cell_index=player.current_cell)

        if player_cell.artifact.owned == True:
            log = game.addLog("Artifact can't be selected, it is already owned" , player)            
            return HttpResponseRedirect(reverse('game-detail', args=(game.id,)))
            
        if(player_cell.artifact.price >= 0 and player.credit >= player_cell.artifact.price):
            log = game.addLog("Artifact is successfully owned" , player)
            player_cell.artifact.owned = True        
            player_cell.artifact.player = player
            player.artifact_count += 1

            if player_cell.action == None:
                log = game.addLog("There is no action in the cell" , player)

            else:
                take_action_log = game.takeAction(player, player_cell.action)
                
                #TODO: gameEnd conditionlari kontrol et
                if game.game_ended == True:
                    pass #TODO: gameEnd icinde log yoksa burada yazdir

        else:
            log = game.addLog("Artifact can't be owned, lack of user credit!" , player)
            
            #FIXME: artifact silmeyi kontrol et
            removed_artifact = player_cell.artifact
            player_cell.artifact_set.remove(removed_artifact)
        
        player.save()
        game.save()
        player_cell.save()
        
            
    elif 'no_pick' in request.POST:
        if player.next_available_move != "pick":
            msg = "You are in the " + player.next_available_move +" phase!"
            messages.warning(request, msg)
            return HttpResponseRedirect(reverse('game-detail', args=(game.id,)))

        #pick = False
        log = game.addLog("Picked false, no action is taken" , player)          

    return HttpResponseRedirect(reverse('game-detail', args=(game.id,)))





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