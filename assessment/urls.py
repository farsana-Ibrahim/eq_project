from django.urls import path
from . import views

app_name = 'assessment'

urlpatterns = [
    path('', views.landing, name='landing'),
    path('scenario/', views.scenario_view, name='scenario'),
    path('results/', views.results_view, name='results'),
]
