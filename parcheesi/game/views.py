from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.contrib.auth.models import User
from .models import *
from django.contrib import messages
import random
import json
from django.http import JsonResponse
from game.consumers import GameConsumer
from asgiref.sync import async_to_sync
#from rest_framework import serializers
from django.core import serializers


######################################################################################

#FIXME: gerek olmayabilir

""" class GameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Game
        fields = ('id', 'winner', 'creator', 'opponent', 'cols', 
                  'rows', 'completed', 'created', 'current_turn')
        depth = 1


class CellSerializer(serializers.ModelSerializer):
    class Meta:
        model = GameSquare
        fields = ('id', 'game', 'owner', 'status', 'row', 'col')


class GameLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = GameLog
        fields = ('id', 'text', 'player', 'created')
        depth = 1 """


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
def changePlayer(player, game):
    players = game.getGamePlayers()
    player_list = []
    next_player_id = 0
    player_size = 0
    for pl in players:
        player_list.append(pl.id)
        player_size+=1
    player_list.sort()
    for pl_index in range(0,player_size):
        if player.id == player_list[pl_index]:
            if pl_index == player_size-1: #new round
                next_player_id = player_list[0]
                message = "Round {} ended".format(game.current_round)
                log = game.addLog(message)
                game.current_round += 1
                for p in players:
                    p.credits += game.cycle_value # cycle_value default is 0
                    p.save()
            else:
                next_player_id = player_list[pl_index+1]

    game.current_player_id = next_player_id
    #player.save()
    game.save()
    

def didPlayerBroke(game,player):
    
    if player.credits <= 0 and game.termination_condition != "firstbroke":
        changePlayer(player, game)
        #game.player_count -= 1
        #player.delete()
        return True

    return False

@login_required
def detail(request, game_id):

    player = User.objects.get(username = request.user).player
    game = get_object_or_404(Game, pk = game_id)
    player_brokeness = didPlayerBroke(game, player)
    context = {
        'game': game,
        'player': player,
        'title': 'Detail',
        'status': player_brokeness
    }
    return render(request, 'game/detail.html', context)

@login_required

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
    game.broadCastGame()
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
    
    messages.success(request, f'You are ready for the game')
    
    if(game.ready_player_count == game.player_count):
        game.game_status = "playing"
        players = game.getGamePlayers()
        player_list = []
        for pl in players:
            player_list.append(pl.id)
        player_list.sort()
        game.current_player_id = player_list[0]
        game.cell_count = len(game.getGameCells())
        
        messages.warning(request, f'Game is Starting')

    player.save()
    game.save()
        
    return HttpResponseRedirect(reverse('game-detail', args=(game.id,)))


@login_required
def game_next(request, game_id):

    player = User.objects.get(username = request.user).player
    game = player.game
    current_player_id = game.current_player_id
    print(request.user.pk)
    gameLog_Serialized = serializers.serialize('json', game.getGameLog(),fields=('message'))
    #gameLog_Serialized = json.loads(gameLog_Serialized)
    #print("serialized gamelog", json.dumps(gameLog_Serialized))

    #GameConsumer.broadcast(gameLog_Serialized)

    if current_player_id != player.pk:
        msg = 'This is not your turn! Please wait...'
        game.broadCastGame()
        return JsonResponse({"msg":"","gameId": game.id, "warning": msg}) 
        #messages.warning(request, msg)
        #return HttpResponseRedirect(reverse('game-detail', args=(game.id,)))

    if request.method != 'POST':
        msg = 'Request type is not POST'
        game.broadCastGame()
        return JsonResponse({"msg":"","gameId": game.id, "warning": msg})
        #messages.warning(request, msg)
        #return HttpResponseRedirect(reverse('game-detail', args=(game.id,)))

    if(player.skip_left_round != 0):
        log = game.addLog("You can't play in this round, you should wait for " + str(player.skip_left_round) + " to play",player )
        player.skip_left_round -= 1
        player.save()

    elif 'roll' in request.POST:
        print("View Roll Called")
        if player.next_available_move != "roll":
            msg = "You are in the " + player.next_available_move +" phase!"
            game.broadCastGame()
            return JsonResponse({"msg":"","gameId": game.id, "warning": msg})
            #messages.warning(request, msg)
            #return HttpResponseRedirect(reverse('game-detail', args=(game.id,)))
        
        diceRoll = random.randrange(game.dice) + 1
        log = game.addLog("Dice rolled" + str(diceRoll),player )
        actionName = ActionName.objects.get(pk=9) # jumpR foreign key is 9
        action = Action(name=actionName, value=diceRoll)
        game.takeAction(player, action)
        game.save()
        cell = game.cell_set.get(cell_index=player.current_cell)
        if cell.artifact is not None:
            player.next_available_move = "pick"
            player.save()
        else:
            player.next_available_move = "next"
            player.save()
    elif 'next' in request.POST:
        if player.next_available_move != "next":
            msg = "You are in the " + player.next_available_move +" phase!"
            game.broadCastGame()
            return JsonResponse({"msg":"","gameId": game.id, "warning": msg}) 
            #messages.warning(request, msg)
            #return HttpResponseRedirect(reverse('game-detail', args=(game.id,)))
        
        player.next_available_move = "roll"
        cell = game.cell_set.get(cell_index=player.current_cell)
        if cell.action is not None:
            game.takeAction(player, cell.action)
            game.save()
        else:
            pass

        changePlayer(player, game)
    
    #gameLog_Serialized = serializers.serialize('xml', game.getGameLog())
    #print("serialized gamelog", gameLog_Serialized)
    #async_to_sync(GameConsumer.broadcast("BroadCast"))
    #GameConsumer.broadcast(gameLog_Serialized)
    
    game.broadCastGame()
    return JsonResponse({"msg":"SUCCESS - Game-Next","gameId": game.id, "warning": ""})                
    #return HttpResponseRedirect(reverse('game-detail', args=(game.id,)))

@login_required
def pick(request, game_id):

    player = User.objects.get(username = request.user).player
    game = player.game #TODO: buraya bakalim tekrardan
    current_player_id = game.current_player_id
    player_cell = game.cell_set.get(cell_index=player.current_cell)
    if current_player_id != player.pk:
        msg = 'This is not your turn! Please wait...'
        #messages.warning(request, msg)
        #return HttpResponseRedirect(reverse('game-detail', args=(game.id,)))
        game.broadCastGame()
        return JsonResponse({"msg":"","gameId": game.id, "warning": msg}) 
    
    if request.method != 'POST':
        msg = 'Request type is not POST'
        game.broadCastGame()
        return JsonResponse({"msg":"","gameId": game.id, "warning": msg})
        #return HttpResponseRedirect(reverse('game-detail', args=(game.id,)))

    if 'pick' in request.POST:
        if player.next_available_move != "pick":
            player.next_available_move = "roll"
            player.save()
            msg = "You are in the " + player.next_available_move +" phase!"
            game.broadCastGame()
            return JsonResponse({"msg":"","gameId": game.id, "warning": msg})
            #messages.warning(request, msg)
            #return HttpResponseRedirect(reverse('game-detail', args=(game.id,)))
        
        #pick = True       

        if player_cell.artifact.owned == True:
            player.next_available_move = "roll"
            player.save()
            log = game.addLog("Artifact can't be selected, it is already owned" , player)
            changePlayer(player, game)
            game.broadCastGame()
            return JsonResponse({"msg":"","gameId": game.id, "warning": ""})            
            #return HttpResponseRedirect(reverse('game-detail', args=(game.id,)))
            
        if(player_cell.artifact.price >= 0 and player.credits >= player_cell.artifact.price):
            log = game.addLog("Artifact is successfully owned" , player)
            player_cell.artifact.owned = True        
            player_cell.artifact.player = player
            player_cell.artifact.save()
            player.credits -= player_cell.artifact.price
            player.artifact_count += 1

            if player_cell.artifact.action == None:
                log = game.addLog("There is no action in the picked artifact, cell action(if exists) will be done" , player)

                if player_cell.action == None:
                    log = game.addLog("There is no action in the cell" , player)
                else:
                    game.takeAction(player, player_cell.action)

            else:
                log = game.addLog("Artifact action will be done, instead of cell action" , player)
                game.takeAction(player, player_cell.artifact.action)

        else:
            log = game.addLog("Artifact can't be owned, lack of user credit!" , player)
            
            #FIXME: artifact silmeyi kontrol et
            removed_artifact = player_cell.artifact
            player_cell.artifact_set.remove(removed_artifact)

        player.next_available_move = "roll"
        game.save()
        player.save()
        player_cell.save() 
            
    elif 'no_pick' in request.POST:
        if player.next_available_move != "pick":
            msg = "You are in the " + player.next_available_move +" phase!"
            game.broadCastGame()
            return JsonResponse({"msg":"","gameId": game.id, "warning": msg})
            #messages.warning(request, msg)
            #return HttpResponseRedirect(reverse('game-detail', args=(game.id,)))

        #pick = False
        log = game.addLog("Picked FALSE, cell action(if exists) will be done" , player)

        if player_cell.action == None:
            log = game.addLog("There is no action in the cell" , player)
        else:
            game.takeAction(player, player_cell.action)
         
    changePlayer(player, game)
    game.broadCastGame()
    return JsonResponse({"msg":"SUCCESS - Game-Pick","gameId": game.id, "warning": ""})
    #return HttpResponseRedirect(reverse('game-detail', args=(game.id,)))