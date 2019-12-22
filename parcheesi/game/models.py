from datetime import datetime
from django.db import models
from django.contrib.auth.models import User


class Game(models.Model):
    name = models.CharField(max_length=50)
    dice = models.IntegerField(default=3)
    is_cycle_enabled = models.BooleanField(default=False)
    cycle_value = models.IntegerField(default=0)
    credit = models.IntegerField(default=100)
    current_player_id = models.IntegerField(default=0)
    #current_player = models.ForeignKey(Player, related_name='current_player', on_delete=models.PROTECT)
    current_round = models.IntegerField(default=0)
    winner = models.ForeignKey(User, related_name='winner', null=True, blank=True, on_delete=models.PROTECT)

    game_ended = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    termination_condition = models.CharField(max_length=20)
    termination_value = models.IntegerField(default=0)
    ready_player_count = models.IntegerField(default=0,null=True)
    player_count = models.IntegerField(default=0)
    game_status = models.CharField(max_length=30,default="initial game")

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
        return Game.objects.filter(game_ended=False)

    def finishGame(self, winner):
        self.winner = winner
        self.game_ended = True #completeddan degistirdim
        self.game_status = "Game is ended"
        self.save()
    
    def ready(self):
        pass

    def join(self):
        pass

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

        log = self.addLog(message, player = self.getCurrentPlayer())
        self.save()
        return log


class Player(models.Model):
    name = models.CharField(max_length=40)
    #game = models.IntegerField(default=0)
    game = models.ForeignKey(Game, null=True, on_delete=models.CASCADE)
    skipLeftRound = models.IntegerField(default=0)
    credits = models.IntegerField(default=100)
    current_cell = models.IntegerField(default=0)
    user = models.OneToOneField(User, null = True,on_delete=models.CASCADE)

    @staticmethod
    def getPlayerById(player_id):
        return Player.objects.get(player_id)

class ActionName(models.Model):
    name = models.CharField(max_length=20)
    def __str__(self):
        return self.name

class Action(models.Model):
    name = models.ForeignKey(ActionName, on_delete=models.PROTECT)
    value = models.IntegerField(default=0)
    player_id = models.IntegerField(default=0, null=True, blank=True) #TODO: Bunu user pk lari ile uyumlu hale getirmek lazim
    #player_id = models.CharField(max_length=20,null=True, blank=True)
    def __str__(self):
        if self.name == "pay":
            return "Action: {} to the player {}, with value: {}".format(self.name, self.value, self.player_id)
        else:
            return "Action: {}, with value : {}".format(self.name, self.value)     
class Card(models.Model):
    action = models.ForeignKey(Action, on_delete=models.CASCADE)

    def __str__(self):
        return "The card {} has the Action: {}, with value : {}".format(self.pk, self.action.name, self.action.value) 
    
    
class Artifact(models.Model):
    name = models.CharField(max_length=20)
    owned = models.BooleanField(default=False)
    player = models.ForeignKey(Player, on_delete=models.PROTECT, blank=True, null=True)
    price = models.IntegerField(default=0)
    action = models.ForeignKey(Action, blank=True, null=True, on_delete=models.PROTECT)

    def __str__(self):
        if self.owned:
            if self.action is None:
                return "Artifact: {}, with price: {}, owned by {}".format(self.name, self.player, self.price)
            else:
                return "Artifact: {}, with price: {} owned by {}, and has {}".format(self.name, self.player, self.price, self.action)
        else:
            if self.action is None:
                return "Artifact: {}, with price: {} not owned".format(self.name, self.price)
            else:
                return "Artifact: {}, with price: {} not owned, and has {}".format(self.name, self.price, self.action)

class Cell(models.Model):
    cell_index = models.IntegerField(default=0)
    description = models.CharField(max_length=100)
    action = models.ForeignKey(Action, blank=True, null=True, on_delete=models.PROTECT)
    artifact = models.ForeignKey(Artifact, on_delete=models.PROTECT, null=True, blank=True)
    game = models.ForeignKey(Game, blank=False, null=False, on_delete=models.CASCADE)
    def __str__(self):
        return "{} {}".format(self.description,self.cell_index)
    


class GameLog(models.Model):
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    message = models.CharField(max_length=100)
    player = models.ForeignKey(User, null=True, blank=True, on_delete=models.PROTECT)

    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "LOG of Game id: {}, Game name: {}".format(self.game.id, self.game.name)
