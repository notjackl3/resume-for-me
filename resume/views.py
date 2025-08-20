from django.shortcuts import render
from django.conf import settings
from django.shortcuts import render, redirect
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from .models import MinorExperience, Description
from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from . import utils

def index(request):
    context = {'MEDIA_URL': settings.MEDIA_URL}
    return render(request, 'index.html', context)


def reset_pdf(request):
    try:
        minor_experiences = list(MinorExperience.objects.values())    

        for experience in minor_experiences:
            descriptions = Description.objects.filter(experience_id=experience["id"])
            experience["descriptions"] = []
            for desc in descriptions:
                experience["descriptions"].append(desc.content)  

        channel_layer = get_channel_layer()
        # pdf_preview_group is the group name, many users can join this group to receive the same updates
        async_to_sync(channel_layer.group_send)(
            "pdf_preview_group",
            {"type": "send_pdf_ready", "url": utils.compile_experience_to_latex(minor_experiences)} # this must matches the method name in consumers.py
        )
        return JsonResponse({"success": True})
    except:
        return JsonResponse({"success": False}, status=400)
    

def reset_panel(request):
    try:
        channel_layer = get_channel_layer()
        # pdf_preview_group is the group name, many users can join this group to receive the same updates
        async_to_sync(channel_layer.group_send)(
            "pdf_preview_group", 
            {"type": "send_panel_data"} # this must matches the method name in consumers.py
        ) 
        return JsonResponse({"success": True})
    except:
        return JsonResponse({"success": False}, status=400)


def add_experience(request):
    if request.method == "POST":
        name = request.POST.get("name")
        date = request.POST.get("date")
        location = request.POST.get("location")
        organisation = request.POST.get("organisation")
        descriptions = request.POST.getlist("descriptions[]")  # list of strings

        work_exp = MinorExperience.objects.create(
            name=name,
            date=date,
            location=location,
            organisation=organisation
        )

        for desc_text in descriptions:
            if desc_text.strip():  # skip empty descriptions
                Description.objects.create(
                    experience=work_exp,
                    content=desc_text
                )
        
        reset_pdf(request)

        return JsonResponse({"success": True})
    return JsonResponse({"success": False}, status=400)


class ManageView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        try: 
            query_type = request.query_params.get("type")
            if query_type == "minor-experience":
                name = request.data.get("name")
                date = request.data.get("date")
                location = request.data.get("location")
                organisation = request.data.get("organisation")
                descriptions = request.data.getlist("descriptions[]")  # list of strings

                minor_exp = MinorExperience.objects.create(
                    name=name,
                    date=date,
                    location=location,
                    organisation=organisation
                )

                for desc_text in descriptions:
                    if desc_text.strip():  # skip empty descriptions
                        Description.objects.create(
                            experience=minor_exp,
                            content=desc_text
                )
                return JsonResponse({"success": True})
        except:
            return JsonResponse({"success": False}, status=400)

    def delete(self, request):
        object_id = request.query_params.get("object-id")
        try:
            query_type = request.query_params.get("type")
            if query_type == "minor-experience":
                object_delete = MinorExperience.objects.get(id=object_id)
                object_delete.delete()
            return JsonResponse({"success": True})
        except:
            return JsonResponse({"success": False}, status=400)
        
    def patch(self, request):
        object_id = request.query_params.get("object-id")
        try:
            query_type = request.query_params.get("type")
            if query_type == "minor-experience":
                object_edit = MinorExperience.objects.get(id=object_id)

                object_edit.name = request.data.get("name")
                object_edit.organisation = request.data.get("organisation")
                object_edit.date = request.data.get("date")
                object_edit.location = request.data.get("location") 
                object_edit.save()
 
                descriptions = request.data.get("descriptions")
                for desc in descriptions:
                    desc_edit = Description.objects.get(id=int(desc[0]))
                    desc_edit.content = desc[1]
                    desc_edit.save()

                print("edit request data:", request.data)
            return JsonResponse({"success": True})
        except:
            return JsonResponse({"success": False}, status=400)
        

class ManagePDF(APIView):
    permission_classes = [AllowAny]

    def patch(self, request):
        object_id = request.query_params.get("object-id")
        try:
            query_type = request.query_params.get("type")
            action = request.query_params.get("action")
            if query_type == "minor-experience":
                if action == "add":
                    object_edit = MinorExperience.objects.get(id=object_id)
                    object_edit.included = True
                    object_edit.save()
                elif action == "remove":
                    object_edit = MinorExperience.objects.get(id=object_id)
                    object_edit.included = False
                    object_edit.save()
                else:
                    print("Experience was not edited")
            return JsonResponse({"success": True})
        except:
            return JsonResponse({"success": False}, status=400)

