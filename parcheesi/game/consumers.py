import asyncio
import json
from django.contrib.auth import get_user_model
from channels.consumer import SyncConsumer, AsyncConsumer
from channels.generic.websocket import WebsocketConsumer
from channels.db import database_sync_to_async

from .models import *

User = get_user_model()

class GameConsumer(SyncConsumer):

	players = {}
	def websocket_connect(self, event):
		# when the socket connects
		print("connected", event)
		self.send({
			"type": "websocket.accept"
		})

	def websocket_receive(self, event):

		print("websocket receive", event)

		message_data = json.loads(event['text'])

		if(message_data['msg'] == "socket_open"):
			GameConsumer.players[message_data["user_id"]] = self

		sendMes = message_data['msg'] + " from websocket_receive"
		sendMes = json.dumps(sendMes)
		self.send({
			"type": "websocket.send",
			"text": sendMes
		})

	def websocket_disconnect(self, event): #TODO: player silinebilir burada
		print("disconnected", event)

	@classmethod
	def broadcast(cls, msg):
		for player in GameConsumer.players:
			GameConsumer.players[player].send({
				"type": "websocket.send",
				#"text": event['message']
				"text": json.dumps(msg)
			})