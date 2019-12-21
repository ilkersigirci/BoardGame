from django.db import models
from django.contrib.auth.models import User
from datetime import datetime

# Create your models here.
class Game(models.Model):
	name =  models.CharField(max_length=50)
	dice =  models.IntegerField(default=3)
	cycles = models.IntegerField(default=1)
	credit = models.IntegerField(default=100)
	current_player = models.ForeignKey(User, related_name='current_player')
	cuurent_round = models.IntegerField(default=0)
    winner = models.ForeignKey(User, related_name='winner', null=True, blank=True)

    gameEnded = models.DateTimeField(null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

	def __str__(self):
    	return "Game id: {}, Game name: {}".format(self.pk, self.name)

	@staticmethod
	def getGameById(id):
    	try:
			return Game.objects.get(pk=id)
		except Game.DoesNotExist:
			print("Requested game doesn't exist")
			pass

    @staticmethod
    def listGames():
        return Game.objects.filter(gameEnded=None)

	def finishGame(self, winner):
		self.winner = winner
		self.completed = datetime.now()
		self.save()

	def getGameCells(self):
		return Cell.objects.filter(game=self)

	def getGameLog(self):
        return GameLog.objects.filter(game=self)

	#TODO:
	def sendGameLog(self):
		cells = self.getGameCells()
    	gameLog = self.getGameLog();
    	message = {game: self}

	def addLog(self, message, user=None):
    	log = GameLog(game=self, message=message, player=user).save()
		return log

class Cell(models.Model):
    cell_index = models.IntegerField(default=0)
    description = models.CharField(max_length=100)
    action = models.ForeignKey(Action, blank=True, null=True, on_delete=models.CASCADE )
	game = models.ForeignKey(Game, blank= False, null=False, on_delete=models.CASCADE)


class Action(models.models):
    name = models.CharField(max_length=20)
    value =  models.IntegerField(default=0)
    player_id
class Artifact(models.models):
    name = models.CharField(max_length=20)
    owned = models.BooleanField(default=False)
    price = models.IntegerField(default=0)
    action = models.ForeignKey(Action, blank=True, null=True, on_delete=models.CASCADE )

class GameLog(models.model):
	game = models.ForeignKey(Game)
	message = models.CharField(max_length=100)
	player = models.ForeignKey(User, null=True, blank=True)

	created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

	def __str__(self):
    	return "LOG of Game id: {}, Game name: {}".format(self.game.id, self.game.name)