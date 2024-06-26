from django.urls import path
from. import views

urlpatterns = [
    path('', views.home, name='home-page'),  
    path('login/', views.login, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register, name='register'),
    path('add_new_patient/', views.add_new_patient, name='add_new_patient'),
    path('add_report_xray/', views.add_report_xray, name='add_report_xray'),
    path('upload/', views.upload, name='upload'),
    path('search_for/', views.search_for, name='search_for'),
]