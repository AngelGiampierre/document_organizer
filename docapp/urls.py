from django.urls import path
from . import views

urlpatterns = [
    path('organizer/', views.document_organizer, name='document_organizer'),
]
