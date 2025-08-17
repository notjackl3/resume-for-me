from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name="home"),
    path('/add-experience/', views.add_experience, name="add_experience"),
    path('/prepare_pdf/', views.prepare_pdf, name="prepare_pdf"),
]