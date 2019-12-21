""" from datetime import datetime
from django.db import models
from django.contrib.auth.models import User


# Create your models here.

    



class Game(models.Model):
    name = models.CharField(max_length=50)
    dice = models.IntegerField(default=3)
    cycles = models.IntegerField(default=1)
    credit = models.IntegerField(default=100)
    current_player_id = models.IntegerField(default=0)
    #current_player = models.ForeignKey(Player, related_name='current_player', on_delete=models.PROTECT)
    cuurent_round = models.IntegerField(default=0)
    winner = models.ForeignKey(User, related_name='winner', null=True, blank=True, on_delete=models.PROTECT)

    game_ended = models.DateTimeField(null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "Game id: {}, Game name: {}".format(self.pk, self.name)

    #TODO: cell create falan yapilabilir boyle, 
    def createGame(self):
        new_cell = self.cell_set.create(...)
        return

    @staticmethod
    def getGameById(game_id):
        try:
            return Game.objects.get(pk=game_id)
        except Game.DoesNotExist:
            print("Requested game doesn't exist")
    

    @staticmethod
    def listGames():
        return Game.objects.filter(gameEnded=None)

    def finishGame(self, winner):
        self.winner = winner
        self.game_ended = datetime.now() #completeddan degistirdim
        self.save()

    def getGameCells(self):
        #return Cell.objects.filter(game=self)
        return self.cell_set.all()

    def getGameLog(self):
        #return GameLog.objects.filter(game=self)
        return self.gamelog_set.all() #TODO: gamelog yazisini nasil olacak tekrardan bakmak lazim
    
    def getGamePlayers(self):
        #return Player.objects.filter(game=self)
        return self.player_set.all()

    #TODO: i nveiw
    def state(self):
        cells = self.getGameCells()
        gameLog = self.getGameLog()
        players = self.getGamePlayers();
        return 

    def addLog(self, message, player=None):
        log = GameLog(game=self, message=message, player=player).save()
        return log

    def getCurrentPlayer(self):
        current_player = Player.getPlayerById(self.current_player_id)
        return current_player

    def takeAction(self, current_player, action):
        action_key = action.name
        action_value = action.value
        #TODO: bunlara state change e eklemek lazim
        if(action_key == "skip"):
            current_player.skipLeftRound += action_value
            message = "Player " + current_player.name + " skipped " + action_value
        elif(action_key == "drop"):
            current_player.credits -= action_value
            message = "Player " + current_player.name + " has lost " + action_value + " credits"
        elif(action_key == "add"):
            current_player.credits += action_value
            message = "Player " + current_player.name + " got " + action_value + " credits"
        elif(action_key == "pay"):
            paidPlayer = Player.objects.get(pk=action.player_id)
            paidPlayer.credits += action_value
            current_player.credits -= action_value
            message = "Player " + current_player.name + " paid " + action_value + " to Player " +  paidPlayer.name

        log = addLog(message, player = player)
        self.save()
        return log


class Player(models.Model):
    name = models.CharField(max_length=40)
    #game = models.IntegerField(default=0)
    game = models.ForeignKey(Game, null=True, on_delete=models.CASCADE)
    skipLeftRound = models.IntegerField(default=0)
    credits = models.IntegerField(default=100)
    current_cell = models.IntegerField(default=0)

    @staticmethod
    def getPlayerById(player_id):
        return Player.objects.get(player_id)



class Action(models.Model):
    name = models.CharField(max_length=20)
    value =  models.IntegerField(default=0)
    player_id = models.CharField(max_length=20) #TODO: Bunu user pk lari ile uyumlu hale getirmek lazim

class Cell(models.Model):
    cell_index = models.IntegerField(default=0)
    description = models.CharField(max_length=100)
    action = models.ForeignKey(Action, blank=True, null=True, on_delete=models.CASCADE)
    game = models.ForeignKey(Game, blank= False, null=False, on_delete=models.CASCADE)


class Artifact(models.Model):
    name = models.CharField(max_length=20)
    owned = models.BooleanField(default=False)
    price = models.IntegerField(default=0)
    action = models.ForeignKey(Action, blank=True, null=True, on_delete=models.PROTECT)

class GameLog(models.Model):
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    message = models.CharField(max_length=100)
    player = models.ForeignKey(User, null=True, blank=True, on_delete=models.PROTECT)

    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "LOG of Game id: {}, Game name: {}".format(self.game.id, self.game.name)
 """