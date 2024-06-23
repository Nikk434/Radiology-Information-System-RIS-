import datetime
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as auth_login , logout
from django.contrib import messages
import pymongo
from pymongo import MongoClient
from gridfs import GridFS
from dotenv import load_dotenv
import os 
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from .forms import DocumentForm
# from .models import Document
from docx import Document
import json
from django.urls import reverse
from django.contrib.auth.decorators import login_required


load_dotenv('D:\DJANGO\.env')

# Create your views here.
@login_required
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

@login_required
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
        print(type(patient_detials))
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

        # query_params = f"?name={name}&age={age}&address={address}&email={email}&gender={gender}&dr={prescribing_doctor}&xray={prescribed_xray}&date_today={date_today}"
        # return redirect(reverse('upload') + query_params)
        return redirect('home-page')
        
    return render(request, 'add_new_patient.html')
    
@login_required
def add_report_xray(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        age = request.POST.get('age')
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
                'Patient DOB': age,
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
            try:
                doc = Document(template_path)
                for paragraph in doc.paragraphs:
                    for key, value in replacements.items():
                        if f'[{key}]' in paragraph.text:  # Ensure the placeholder format is correct
                            paragraph.text = paragraph.text.replace(f'[{key}]', value)
                            print(f"Replaced [{key}] with {value}")

                doc.save(output_path)
                print(f"Document saved to {output_path}")
            except Exception as e:
                print(f"An error occurred: {e}")
        
        template_path = 'D:\DJANGO\\report_template.docx'  # Use raw string to handle backslashes
        output_path = 'D:\DJANGO\RIS\Reports\\report.docx'  # Path where the filled document will be saved

    # Get user     
        user_info = get_user_inpu()

    # Replace placeholders and save the document
        replace_placeholders(template_path, output_path, user_info)

        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            print("X-ray uploaded successfully")
        else:
            print("Form is not valid")

        query_params = {
            'name': name,
            'age': age,
            'address': request.POST.get('address'),
            'email': request.POST.get('email'),
            'gender': gender,
            'dr': referringPhysicianName,
            'xray': typeOfExamination,
            'date_today': request.session.get('date_today'),
        }
        url = reverse('upload') + '?' + '&'.join([f"{key}={value}" for key, value in query_params.items()])
        return redirect(url)

    else:
        form = DocumentForm()
    return redirect('home-page')

@login_required
def upload(request):
    if request.method == 'POST':
        load_dotenv('D:/DJANGO/.env')

        username = os.getenv("MONGODB_USERNAME")
        password = os.getenv("MONGODB_PASSWORD")
        cluster_url = os.getenv("MONGODB_CLUSTER_URL")

        # Construct the MongoDB URI for MongoDB Atlas
        mongo_uri = f"mongodb+srv://{username}:{password}@{cluster_url}/?retryWrites=true&w=majority"

        client = pymongo.MongoClient(mongo_uri)

        # Select the database and collection
        db = client["RISPATIENT"]
        collection = db["patient_data"]

        fs = GridFS(db)

        report_path = "D:/DJANGO/RIS/Reports/report.docx"
        image_path = "D:/DJANGO/RIS/Radiology-Information-System-RIS-/RIS_project/media/x_ray/xray.png"

        name = request.GET.get('name')
        age = request.GET.get('age')
        address = request.GET.get('address')
        email = request.GET.get('email')
        gender = request.GET.get('gender')
        prescribing_doctor = request.GET.get('dr')
        prescribed_xray = request.GET.get('xray')
        date_today = request.GET.get('date_today')

        patient_details = {
            "date": date_today,
            "name": name,
            "age": age,
            "address": address,
            "email": email,
            "gender": gender,
            "prescribing_doctor": prescribing_doctor,
            "prescribed_xray": prescribed_xray,
        }

        # Upload the report file
        with open(report_path, 'rb') as file:
            stored_file = fs.put(file, filename='report.docx')


        if stored_file:
            print(f"Report file uploaded successfully with id: {stored_file}")
            # Add report file metadata to patient details
            patient_details["report_file_id"] = stored_file
            patient_details["report_file_name"] = "report.docx"

        # Upload the image file
        with open(image_path, "rb") as image_file:
            stored_img = fs.put(image_file, filename="xray.png")


        if stored_img:
            print(f"Image file uploaded successfully with id: {stored_img}")
            # Add image file metadata to patient details
            patient_details["image_file_id"] = stored_img
            patient_details["image_file_name"] = "xray.png"

        # Insert patient details into MongoDB collection
        result = collection.insert_one(patient_details)

        if result.inserted_id:
            print(f"Patient details inserted successfully with id: {result.inserted_id}")
        else:
            print("Failed to insert patient details")

    return redirect('home-page')

@login_required
def search_for(request):
    load_dotenv('D:/DJANGO/.env')

    # Retrieve MongoDB connection details from environment variables
    username = os.getenv("MONGODB_USERNAME")
    password = os.getenv("MONGODB_PASSWORD")
    cluster_url = os.getenv("MONGODB_CLUSTER_URL")

    # Construct the MongoDB URI for MongoDB Atlas
    mongo_uri = f"mongodb+srv://{username}:{password}@{cluster_url}/?retryWrites=true&w=majority"

    # Connect to MongoDB Atlas cluster
    client = pymongo.MongoClient(mongo_uri)

    # Select the database and collection
    db = client["RISPATIENT"]
    collection = db["patient_data"]

    # Ensure a text index is created on the fields you want to search
    collection.create_index([("name", "text"), ("email", "text"), ("address", "text")])

    # Initialize an empty list to store search results
    result_list = []

    if request.method == 'POST':
        # Retrieve the search text from the form
        search_text = request.POST.get('search_input', '')

        # Construct the query using text search
        query = {"$text": {"$search": search_text}}

        # Find documents that match the query
        results = collection.find(query)

        for result in results:
            result_list.append(result)
        
        stored_file = result["report_file_id"]
        stored_img = result["image_file_id"]
        
        def download(file_id, filename):
            fs = GridFS(db)
            file_document = fs.find_one({"_id": file_id})
            if file_document:
                save_directory = "D:/DJANGO/mongo_downloads"
                os.makedirs(save_directory, exist_ok=True)
                save_path = os.path.join(save_directory, filename)
                with open(save_path, 'wb') as file_stream:
                    file_stream.write(file_document.read())
                print(f"File downloaded successfully: {save_path}")
            else:
                print("Not found")

        download(stored_file, "report.docx")
        download(stored_img, "xray.png")

    return render(request, 'search_for.html', {'results': result_list})

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
        return redirect('login')
    return render(request, 'register.html', {})

def logout_view(request):
    logout(request)
    return redirect('login')

def login(request):
    if request.user.is_authenticated:
        return redirect('home-page')
    
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


