from django.contrib import admin
from .models import Crop, Disease, Treatment, Prediction, CropTip

@admin.register(Crop)
class CropAdmin(admin.ModelAdmin):
    list_display = ['name', 'scientific_name', 'created_at']
    search_fields = ['name', 'scientific_name']
    list_filter = ['created_at']
    ordering = ['name']

@admin.register(Disease)
class DiseaseAdmin(admin.ModelAdmin):
    list_display = ['name', 'crop', 'created_at']
    list_filter = ['crop', 'created_at']
    search_fields = ['name', 'crop__name']
    ordering = ['crop__name', 'name']

@admin.register(Treatment)
class TreatmentAdmin(admin.ModelAdmin):
    list_display = ['title', 'disease', 'instructions', 'created_at']
    list_filter = ['instructions','disease__crop', 'created_at']
    search_fields = ['title', 'disease__name', 'description']
    ordering = ['disease__crop__name', 'disease__name', 'title']

@admin.register(Prediction)
class PredictionAdmin(admin.ModelAdmin):
    list_display = ['predicted_crop', 'predicted_disease', 'confidence_score', 'created_at']
    list_filter = ['predicted_crop', 'confidence_score', 'is_correct', 'created_at']
    search_fields = ['predicted_crop', 'predicted_disease']
    readonly_fields = ['image', 'predicted_crop', 'predicted_disease', 'confidence_score', 'created_at']
    ordering = ['-created_at']

@admin.register(CropTip)
class CropTipAdmin(admin.ModelAdmin):
    list_display = ['title', 'crop', 'tip_type', 'season', 'created_at']
    list_filter = ['crop', 'tip_type', 'season', 'created_at']
    search_fields = ['title', 'crop__name', 'content']
    ordering = ['crop__name', 'tip_type', 'title']
