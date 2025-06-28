from django.shortcuts import render
from .models import Profile
from django.http import HttpResponse
from django.template import loader
import io

# import pdfkit
from reportlab.pdfgen import canvas
from io import BytesIO



# Create your views here.
def accept(request):
    if request.method == 'POST':
        name = request.POST.get("name","")
        email = request.POST.get("email","")
        phone = request.POST.get("phone","")
        summary = request.POST.get("summary","")
        degree = request.POST.get("degree","")
        school = request.POST.get("school","")
        university = request.POST.get("university","")
        previous_work= request.POST.get("previous_work","")
        skills = request.POST.get("skills","")
 
        profile = Profile(name=name,email=email,phone=phone,summary=summary,degree=degree,school=school,university=university,previous_work=previous_work,skills=skills)
        profile.save()

    return render(request,'cv_pdf/accept.html')

# def resume(request, id):
#     user_profile = Profile.objects.get(pk=id)
#     template = loader.get_template('cv_pdf/resume.html')
#     html = template.render({'user_profile': user_profile})
#     options = {
#         'page-size':'Letter',
#         'encoding':"UTF-8"
#     }
#     pdf = pdfkit.from_string(html,False,options)
#     response = HttpResponse(pdf, content_type = 'application/pdf')
#     response['Content-Disposition'] = 'attachment'
#     filename = 'resume.pdf'
#     return response

def resume(request, id):
    user_profile = Profile.objects.get(pk=id)

    # Create a file-like buffer to receive PDF data
    buffer = BytesIO()
    p = canvas.Canvas(buffer)

    # Add content to PDF
    p.drawString(100, 800, f"Name: {user_profile.name}")
    p.drawString(100, 780, f"Email: {user_profile.email}")
    p.drawString(100, 760, f"Phone: {user_profile.phone}")
    p.drawString(100, 740, f"Summary: {user_profile.summary}")
    p.drawString(100, 720, f"Degree: {user_profile.degree}")
    p.drawString(100, 700, f"School: {user_profile.school}")
    p.drawString(100, 680, f"University: {user_profile.university}")
    p.drawString(100, 660, f"Previous Work: {user_profile.previous_work}")
    p.drawString(100, 640, f"Skills: {user_profile.skills}")

    # Save the PDF
    p.showPage()
    p.save()

    # Get the value of the BytesIO buffer and return it as a response
    buffer.seek(0)
    return HttpResponse(buffer, content_type='application/pdf')

def profile_list(request):
    profiles = Profile.objects.all()  
    return render(request, 'cv_pdf/list.html', {'profiles': profiles})