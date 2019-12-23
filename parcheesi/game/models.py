from datetime import datetime
from django.db import models
from django.contrib.auth.models import User
import random

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
    cell_count = models.IntegerField(default=0)

    def __str__(self):
        return "Game id: {}, Game name: {}".format(self.pk, self.name)

    """ def createGame(self):
        new_cell = self.cell_set.create(...)
        return """

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

    def getGameCells(self):
        #return Cell.objects.filter(game=self)
        return self.cell_set.all()

    def getGameLog(self):
        #return GameLog.objects.filter(game=self)
        return self.gamelog_set.all() #TODO: gamelog yazisini nasil olacak tekrardan bakmak lazim
        #reverseList = self.gamelog_set.all()
        #return reverseList.sort(reverse=True)

    def getGamePlayers(self):
        #return Player.objects.filter(game=self)
        return self.player_set.all()

    def addLog(self, message, player=None):
        log = GameLog(game=self, message=message, player=player).save()
        return log

    #FIXME: calismiyor -> we don't know why
    def getCurrentPlayer(self):
        current_player = Player.objects.get(pk=self.current_player_id)
        return current_player

    def takeAction(self, current_player, action):
        action_key = action.name.name
        action_value = action.value
        message = "Empty Take Action Message with key: " + action_key + "value: " + str(action_value)
        if(action_key == "skip"):
            current_player.skip_left_round += action_value
            message = "Player " + current_player.name + " skipped " + str(action_value)
            #log = self.addLog(message , current_player)
   
        elif(action_key == "drop"):
            current_player.credits -= action_value
            message = "Player " + current_player.name + " has lost " + str(action_value) + " credits"
            #log = self.addLog(message , current_player)

        elif(action_key == "add"):
            current_player.credits += action_value
            message = "Player " + current_player.name + " got " + str(action_value) + " credits"
            #log = self.addLog(message , current_player)

        
        elif(action_key == "pay"):
            paid_player = Player.objects.get(pk=action.player_id)
            paid_player.credits += action_value
            current_player.credits -= action_value            
            paid_player.save()
            message = "Player " + current_player.name + " paid " + str(action_value) + " to Player " +  paid_player.name
            #log = self.addLog(message , current_player)
        
        elif(action_key == "jumpA"):
            current_player.current_cell = action_value
            message = "Player " + current_player.name + " jump absolute " + str(action_value) + " and his current cell is " + str(current_player.current_cell)
            #log = self.addLog(message , current_player)

        elif(action_key == "jumpR"):
            current_player.current_cell += action_value

            
            if self.is_cycle_enabled == True:
                if current_player.current_cell >= self.cell_count:
                    current_player.current_cell %= self.cell_count
                    current_player.cycle_count += 1
                elif current_player.current_cell <0:
                    current_player.current_cell %= self.cell_count
                    current_player.cycle_count -= 1
            elif current_player.current_cell >= self.cell_count:
                current_player.current_cell = self.cell_count-1
            message = "Player " + current_player.name + " jump relative " + str(action_value) + " and his current cell is " + str(current_player.current_cell)
            #log = self.addLog(message , current_player)

        
        elif(action_key == "drawcard"):
            picked_card = random.choice(Card.objects.all())
            picked_action = picked_card.action
            message = "Player " + current_player.name + " drawed  the card: " + str(action_value) 
            #log = self.addLog(message , current_player)
            self.takeAction(current_player, picked_action)
        
        
        current_player.save()
        self.save()
        
        self.isGameEnded(current_player)

        log = self.addLog(message, player = self.getCurrentPlayer())
        
    def isGameEnded(self,player):
        if(self.termination_condition == "round"):
            if player.cycle_count >= self.termination_value:
                self.game_ended = True
                self.game_status = "game is ended"
        elif(self.termination_condition == "finish"):
            if player.cycle_count >= self.termination_value-1:
                self.game_ended = True
                self.game_status = "game is ended"
        elif(self.termination_condition == "firstbroke"):
            if player.cycle_count <= self.termination_value:
                self.game_ended = True
                self.game_status = "game is ended"
        elif(self.termination_condition == "firstcollect"):
            if player.cycle_count >= self.termination_value:
                self.game_ended = True
                self.game_status = "game is ended"
        self.save()
        

class Player(models.Model):
    name = models.CharField(max_length=40)
    #game = models.IntegerField(default=0)
    game = models.ForeignKey(Game, null=True, on_delete=models.CASCADE)
    skip_left_round = models.IntegerField(default=0)
    credits = models.IntegerField(default=100)
    current_cell = models.IntegerField(default=0)
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    is_ready = models.BooleanField(default=False)
    next_available_move = models.CharField(default="roll", max_length=20)
    artifact_count = models.IntegerField(default=0)
    cycle_count = models.IntegerField(default=0)
    
    @staticmethod
    def getPlayerById(player_id):
        return Player.objects.get(pk=player_id)
    def __str__(self):
        return self.name
    

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
        if self.action is None:
            if self.artifact is None:
                return "{}. {}".format(self.cell_index, self.description)
            else:
                return "{}. {}, {}".format(self.cell_index, self.description, self.artifact)    
            return "{}. {}".format(self.cell_index, self.description)
        else:
            if self.artifact is None:
                return "{}. {}, {}".format(self.cell_index, self.description,self.action)
            else:
                return "{}. {}, {}, {}".format(self.cell_index, self.description, self.action, self.artifact)    
            return "{}. {}".format(self.cell_index, self.description)
        return "{} {}".format(self.description, self.cell_index)
    


class GameLog(models.Model):
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    message = models.CharField(max_length=100)
    player = models.ForeignKey(Player, null=True, blank=True, on_delete=models.PROTECT)

    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.player.name + "'s move: " + self.message
        #return "LOG of Game id: {}, Game name: {}".format(self.game.id, self.game.name)
