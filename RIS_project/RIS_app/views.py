import datetime
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as auth_login , logout
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm

# Create your views here.
def home(request):
    name = request.user.username if request.user.is_authenticated else None
    # print("NAME= ",name)
    x = datetime.datetime.now()
    # print(x)
    date_today = x.strftime("%a %d, %b %Y %I:%M%p")
    return render(request, 'home.html', {'username':name, 'date_today':date_today })

def add_new_patient(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        age = request.POST.get('age')
        email = request.POST.get('email')
        gender = request.POST.get('gender')
        prescribing_doctor = request.POST.get('dr')
        prescribed_xray = request.POST.get('xray')

        print(name)
        print(age)
        print(email)
        print(gender)
        print(prescribing_doctor)
        print(prescribed_xray)


        return redirect('home-page')

    return render(request, 'add_new_patient.html')
    

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


