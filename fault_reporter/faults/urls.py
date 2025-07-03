from django.urls import path
from . import views

urlpatterns = [
    path('', views.fault_list, name='fault_list'),
    path('delete/<int:fault_id>/', views.delete_fault, name='delete_fault'),
    path('generate_pdf/', views.generate_pdf, name='generate_pdf'),
]