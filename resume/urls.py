from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name="home"),
    path('add-experience/', views.ManageView.as_view(), name="add_experience"),
    path('delete-experience/', views.ManageView.as_view(), name="delete_experience"),
    path('edit-pdf/', views.ManagePDF.as_view(), name="edit_pdf"),
    path('edit-experience/', views.ManageView.as_view(), name="edit_experience"),
    path('prepare-pdf/', views.reset_pdf, name="prepare_pdf"),
    path('reset-panel/', views.reset_panel, name="reset_panel"),
    path('include/', views.add_experience, name="include"),
    path('exclude/', views.add_experience, name="exclude"),
]