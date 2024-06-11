import datetime
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as auth_login , logout
from django.contrib import messages
import pymongo
from dotenv import load_dotenv
import os 
from docx import Document


load_dotenv('D:\DJANGO\.env')

# Create your views here.
def home(request):
    name = request.user.username if request.user.is_authenticated else None
    x = datetime.datetime.now()
    date_today = x.strftime("%a %d, %b %Y")
    time_today = x.strftime("%I:%M%p") 
    request.session['date_today'] = date_today

    username = os.getenv("MONGODB_USERNAME")
    password = os.getenv("MONGODB_PASSWORD")
    cluster_url = os.getenv("MONGODB_CLUSTER_URL")

    # Construct the MongoDB URI
    mongo_uri = f"mongodb+srv://{username}:{password}@{cluster_url}/?retryWrites=true&w=majority"
    client = pymongo.MongoClient(mongo_uri)        

    db = client["RISPATIENT"]
    collection = db["patient_data"]

    # Fetch data that matches today's date
    data = list(collection.find({"date": date_today}))

    return render(request, 'home.html', {'username': name, 'date_today': date_today, 'time_today':time_today, 'data': data})

def add_new_patient(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        age = request.POST.get('age')
        address = request.POST.get('address')
        email = request.POST.get('email')
        gender = request.POST.get('gender')
        prescribing_doctor = request.POST.get('dr')
        prescribed_xray = request.POST.get('xray')
        date_today = request.session.get('date_today')

        patient_detials = {
            "date":date_today,
            "name":name,
            "age":age,
            "address":address,
            "email":email,
            "gender":gender,
            "prescribing_doctor":prescribing_doctor,
            "prescribed_xray":prescribed_xray
        }

        username = os.getenv("MONGODB_USERNAME")
        password = os.getenv("MONGODB_PASSWORD")
        cluster_url = os.getenv("MONGODB_CLUSTER_URL")

    # Construct the MongoDB URI
        mongo_uri = f"mongodb+srv://{username}:{password}@{cluster_url}/?retryWrites=true&w=majority"
        client = pymongo.MongoClient(mongo_uri)        

        db = client["RISPATIENT"]
        collection = db["patient_data"]

    # Insert the document into the collection
        collection.insert_one(patient_detials)
        print("Content stored in MongoDB successfully.")
        
        return redirect('home-page')

    return render(request, 'add_new_patient.html')
    
def add_report_xray(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        age = request.POST.get('Patient DOB')
        gender = request.POST.get('gender')
        date = request.POST.get('exam_date')
        referringPhysicianName = request.POST.get('referringPhysicianName')
        contactInformation = request.POST.get('contactInformation')
        typeOfExamination = request.POST.get('typeOfExamination')
        bodyPartExamined = request.POST.get('bodyPartExamined')
        clinicalIndication = request.POST.get('clinicalIndication')
        xrayMachineModel = request.POST.get('xrayMachineModel')
        exposureParameters = request.POST.get('exposureParameters')
        radiographerName = request.POST.get('radiographerName')
        findings = request.POST.get('findings')
        impression = request.POST.get('impression')
        recommendations = request.POST.get('recommendations')
        radiologistName = request.POST.get('radiologistName')
        dateOfReport = request.POST.get('dateOfReport')

        def get_user_inpu():
            patient_info = {
                'Patient Name': name,
                'Patient age': age,
                'Patient Gender': gender,
                'Examination Date': date,
                'Referring Physician Name': referringPhysicianName,
                'Contact Information': contactInformation,
                'Type of X-Ray': typeOfExamination,
                'Body Part': bodyPartExamined,
                'Clinical Indication/Reason for Exam': clinicalIndication,
                'Model': xrayMachineModel,
                'Exposure Parameters': exposureParameters,
                'Name':radiographerName,
                'findings': findings,
                'Impression': impression,
                'Recommendations': recommendations,
                'Radiologist Name': radiologistName,
                'Date of Report': dateOfReport
            }
            return patient_info    
        
        def replace_placeholders(template_path, output_path, replacements):
            doc = Document(template_path)
            for paragraph in doc.paragraphs:
                for key, value in replacements.items():
                    if key in paragraph.text:
                        paragraph.text = paragraph.text.replace(f'[{key}]', value)
            doc.save(output_path)
        
        template_path = 'D:\DJANGO\\report_template.docx'  # Path to your template
        output_path = 'report.docx'  # Path where the filled document will be saved

    # Get user     
        user_info = get_user_inpu()

    # Replace placeholders and save the document
        replace_placeholders(template_path, output_path, user_info)

        print(f"Document saved as {output_path}")

    return redirect('home-page')


def register(request):
    if request.user.is_authenticated:
        return redirect('home-page')
    
    if request.method == 'POST':
        name = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        # password check        
        if len(password)<8:
            messages.error(request,"Password must be atleast 8 charecters")
            return redirect('register')
        # user check
        get_users = User.objects.filter(username=name)
        if get_users:
            messages.error(request,"User already exist !")
            return redirect('register')


        new_user = User.objects.create_user(username=name, email=email, password=password)
        new_user.save()
        messages.success(request, "Registration suceessful! Log in now ")
        # return render(request, 'todoapp/login.html', {})
        return redirect('login')

    return render(request, 'register.html', {})

def login(request):
    # if request.user.is_authenticated:
    #     return redirect('home-page')
    
    if request.method =='POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        check_user = authenticate(username=username, password = password)
        if check_user is not None:
            auth_login(request, check_user)
            return redirect('home-page')
        else:
            messages.error(request, "User does not exist")
            return redirect('login')
    
    return render(request, 'login.html',{})


