import subprocess
import os, time, shutil
from django.conf import settings


def compile_latex_block_to_file(filepath, updated_latex_path, insertion_marker, latex_block):
    with open(filepath, "r") as f:
        content = f.read()
        modified_content = content.replace(insertion_marker, latex_block)
        with open(updated_latex_path, "w") as f:
            f.write(modified_content)


def compile_latex_to_media(file, folder):
    filename_only = os.path.basename(file) # resume.tex
    filename, _ = os.path.splitext(filename_only)
    
    subprocess.run(
        ["pdflatex", "-interaction=nonstopmode", filename_only],
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

    return f"{settings.MEDIA_URL}media-resume/output/{filename}-{timestamp}.pdf"
    

def compile_experience_to_latex(content):
    latex_path = os.path.join(settings.MEDIA_ROOT, "media-resume", "resume.tex")
    updated_latex_path = os.path.join(settings.MEDIA_ROOT, "media-resume", "updated-resume.tex")
    folder_path = os.path.join(settings.MEDIA_ROOT, "media-resume")

    new_latex_content = ""
    for experience in content:
        print(experience["included"])
        if experience["included"]:
            name = experience["name"]
            organisation = experience["organisation"]
            date = experience["date"]
            descriptions = experience["descriptions"]
            temp = ""
            for desc in descriptions:
                temp += fr"\resumeItem{{{desc}}}"

            new_latex_content += fr"""
            \resumeBiHeading{{{name}}}{{{organisation}}}{{{date}}}
            \resumeItemListStart{{}}
            \vspace{{-7pt}}
            {temp}
            \resumeItemListEnd{{}}

            """
    marker = f"% INSERT__EXPERIENCE_0"
    compile_latex_block_to_file(latex_path, updated_latex_path, marker, new_latex_content)

    pdf_url = compile_latex_to_media(updated_latex_path, folder_path)
    return pdf_url

