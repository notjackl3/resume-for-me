from django.shortcuts import render
from django.conf import settings
from django.shortcuts import render, redirect
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from .models import WorkExperience, Description
from django.http import JsonResponse
import os, time, shutil
import subprocess


def index(request):
    return render(request, 'index.html', {
        'MEDIA_URL': settings.MEDIA_URL
})


def insert_latex_block(filepath, updated_latex_path, insertion_marker, latex_block):
    with open(filepath, 'r') as f:
        content = f.read()

        # print("content of base latex", content)

        print("original content: ", content)
        print("inserting market", insertion_marker)
        print("latex block", latex_block)

        modified_content = content.replace(insertion_marker, latex_block)

        print("modified content: ", modified_content)

        with open(updated_latex_path, 'w') as f:
            f.write(modified_content)


def compile_latex_to_media(file, folder):
    filename_only = os.path.basename(file) # resume.tex
    filename, _ = os.path.splitext(filename_only)
    
    subprocess.run(
        ['pdflatex', '-interaction=nonstopmode', filename_only],
        cwd=folder,
        capture_output=True,
        text=True
    )

    generated_pdf = os.path.join(folder, f"{filename}.pdf")
    dest_folder = os.path.join(settings.MEDIA_ROOT, "media-resume", "output")

    os.makedirs(dest_folder, exist_ok=True)

    # avoid caching collision between each file
    timestamp = int(time.time())
    dest_file = os.path.join(dest_folder, f"{filename}-{timestamp}.pdf")

    shutil.move(generated_pdf, dest_file)

    url = f"{settings.MEDIA_URL}media-resume/output/{filename}-{timestamp}.pdf"
    return dest_file, url
    

def compile_experience_to_latex(content):
    latex_path = os.path.join(settings.MEDIA_ROOT, "media-resume", "resume.tex")
    updated_latex_path = os.path.join(settings.MEDIA_ROOT, "media-resume", "updated-resume.tex")
    folder_path = os.path.join(settings.MEDIA_ROOT, "media-resume")

    for index, experience in enumerate(content):
        print("adding in", experience)
        name = experience["name"]
        organisation = experience["organisation"]
        date = experience["date"]
        descriptions = experience["descriptions"]
        description1 = descriptions[0]

        new_latex_content = fr"""
        \resumeBiHeading{{{name}}}{{{organisation}}}{{{date}}}
        \resumeItemListStart{{}}
        \vspace{{-7pt}}
        \resumeItem{{{description1}}}
        \resumeItemListEnd{{}}
        """
        marker = f"% INSERT__EXPERIENCE_{index}"
        print("replacing", marker)
        insert_latex_block(latex_path, updated_latex_path, marker, new_latex_content)

    with open(latex_path, "r") as file:
        pdf_file_path, pdf_url = compile_latex_to_media(updated_latex_path, folder_path)

        with open(pdf_file_path, "rb") as file2:
            pdf_bytes = file2.read()
            print(f"PDF size: {len(pdf_bytes)} bytes")

        print(f"PDF available at: {pdf_url}")
        return pdf_url
        

    # experiences = WorkExperience.objects.all()
    # for experience in experiences:
    #     print("name", experience.name)
    #     print("date", experience.date)


def prepare_pdf(request):
    print("prepare pdf")
    try:
        content = [{"name": "Workshop Lead", 
                    "date": "July 2025 -- August 2025",
                    "location": "Toronto, Canada",
                    "organisation": "Ignition Hacks V6",
                    "descriptions": ["Present Mapbox content"]}]
        url = compile_experience_to_latex(content)

        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            # pdf_preview_group is the group name, many users can join this group to receive the same updates
            "pdf_preview_group",
            {
                # this must matches the method name in consumers.py
                "type": "send_pdf_ready",
                "url": url
            }
        )
        return JsonResponse({"success": True})
    except:
        return JsonResponse({"success": False}, status=400)


def compile_pdf(request):
    print("compiling pdf")
    try:
        prepare_pdf()
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

        work_exp = WorkExperience.objects.create(
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
        
        compile_pdf(request)
        return JsonResponse({"success": True})
    return JsonResponse({"success": False}, status=400)