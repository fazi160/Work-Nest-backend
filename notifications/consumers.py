from channels.generic.websocket import AsyncWebsocketConsumer

class NotificationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        print("WebSocket connected")
        await self.accept()

    async def disconnect(self, close_code):
        pass  # Handle disconnection if needed

    async def send_notification(self, event):
        message = event['message']
        await self.send(text_data=json.dumps({'message': message}))
