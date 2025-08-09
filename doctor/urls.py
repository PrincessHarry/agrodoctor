from django.urls import path
from . import views
from .views import classify_plant_image

app_name = 'doctor'

urlpatterns = [
    # Main pages
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    
    # Prediction functionality
    path('predict/', views.predict_disease, name='predict_disease'),
    path('result/<int:prediction_id>/', views.prediction_result, name='prediction_result'),
    
    # User dashboard
    path('dashboard/', views.dashboard, name='dashboard'),
    
    # Crops
    path('crops/', views.crops_list, name='crops_list'),
    path('crops/<int:crop_id>/', views.crop_detail, name='crop_detail'),
    
    # Diseases
    path('diseases/', views.diseases_list, name='diseases_list'),
    path('diseases/<int:disease_id>/', views.disease_detail, name='disease_detail'),

    # Plant classification
    path('classify/', classify_plant_image, name='classify_plant_image'),
] 