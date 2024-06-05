from django.urls import path
from .views import *

urlpatterns = [
    path('',home,name='home'),
    path('course/<slug>',CourseView,name='course'),
    path('become_pro',become_pro,name='become_pro'),
    path('charge/',charge,name='charge'),
    path('login/',Login,name='login'),
    path('register/',register,name='register'),
    path('logout',Logout,name='logout')
]

