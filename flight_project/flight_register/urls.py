from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.flight_form, name='flight_insert'),
    path('<int:id>/', views.flight_form, name='flight_update'),
    path('delete/<int:id>/', views.flight_delete, name='flight_delete'),
    path('list/', views.flight_list, name='flight_list'),
    path('export/', views.flight_export, name='flight_export')
]
