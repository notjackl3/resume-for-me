import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async


class PDFPreviewConsumer(AsyncWebsocketConsumer):
    # connect() is runs when the first websocket connection is made
    async def connect(self):
        await self.channel_layer.group_add("pdf_preview_group", self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard("pdf_preview_group", self.channel_name)

    # this method is called when the other part of django (latex processor) sends a message to this consumer via channel layer
    async def send_pdf_ready(self, event):
        from .models import WorkExperience
        data = await self.get_experiences()
        print(data)
        # this method sends a json to the browser, telling it to use the url to render the pdf file to the front-end
        await self.send(text_data=json.dumps({
            "event": "pdf_ready",
            "url": event["url"]
        }))

    # db query like objects. is sync, and since we call it in the async methid send_pdf_ready, we have to convert it to async first
    @database_sync_to_async
    def get_experiences(self):
        from .models import WorkExperience
        return list(WorkExperience.objects.all())
