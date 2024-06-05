from django.urls import path
from .views import *

urlpatterns = [
    path('home/',home,name='home'),
    path('course/<slug>',CourseView,name='course'),
    path('become_pro',become_pro,name='become_pro'),
    path('charge/',charge,name='charge'),
]

