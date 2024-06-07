import datetime
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as auth_login , logout
from django.contrib import messages
import pymongo
from dotenv import load_dotenv
import os 

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
    pass

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


