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
        from .models import MinorExperience
        data = await self.get_experiences()
        print(data)
        # this method sends a json to the browser, telling it to use the url to render the pdf file to the front-end
        await self.send(text_data=json.dumps({
            "event": "pdf_ready",
            "url": event["url"]
        }))

    async def send_panel_data(self, event): 
        from django.forms.models import model_to_dict
        minor_experiences = await self.get_experiences()

        experiences_data = []
        for experience in minor_experiences:
            experience_dict = model_to_dict(experience)
            
            descriptions = await self.get_descriptions(experience_dict["id"])
            experience_dict["descriptions"] = [desc.content for desc in descriptions]
            experiences_data.append(experience_dict)
        
        print(experiences_data)

        # this method sends a json to the browser, telling it to use the url to render the pdf file to the front-end
        await self.send(text_data=json.dumps({
            "event": "reset_panel",
            "minor_experiences_data": experiences_data, 
        }))

    # db query like objects. is sync, and since we call it in the async methid send_pdf_ready, we have to convert it to async first
    @database_sync_to_async
    def get_experiences(self):
        from .models import MinorExperience
        return list(MinorExperience.objects.all())
    
    @database_sync_to_async
    def get_descriptions(self, object_id):
        from .models import Description
        return list(Description.objects.filter(experience_id=object_id))
