from django.db import models
# from django.contrib.auth.models import User
from django.utils import timezone

class Crop(models.Model):
    """Model to store crop information"""
    name = models.CharField(max_length=100)
    scientific_name = models.CharField(max_length=200, blank=True)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='crops/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']

class Disease(models.Model):
    """Model to store disease information"""
    name = models.CharField(max_length=200)
    crop = models.ForeignKey(Crop, on_delete=models.CASCADE, related_name='diseases')
    # description = models.TextField()
    # symptoms = models.TextField()
    # causes = models.TextField(blank=True)
    # severity = models.CharField(max_length=20, choices=[
    #     ('low', 'Low'),
    #     ('medium', 'Medium'),
    #     ('high', 'High'),
    #     ('critical', 'Critical'),
    # ], default='medium')
    # image = models.ImageField(upload_to='diseases/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.crop.name} - {self.name}"

    class Meta:
        ordering = ['crop__name', 'name']

class Treatment(models.Model):
    """Model to store treatment recommendations"""
    disease = models.ForeignKey(Disease, on_delete=models.CASCADE, related_name='treatments')
    title = models.CharField(max_length=200)
    # description = models.TextField()
    # treatment_type = models.CharField(max_length=50, choices=[
    #     ('chemical', 'Chemical'),
    #     ('organic', 'Organic'),
    #     ('cultural', 'Cultural'),
    #     ('biological', 'Biological'),
    # ])
    instructions = models.TextField()
    # precautions = models.TextField(blank=True)
    # effectiveness = models.CharField(max_length=20, choices=[
    #     ('low', 'Low'),
    #     ('medium', 'Medium'),
    #     ('high', 'High'),
    # ], default='medium')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.disease} - {self.title}"

    class Meta:
        ordering = ['disease__crop__name', 'disease__name', 'title']

class Prediction(models.Model):
    """Model to store prediction results"""
    # user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    image = models.ImageField(upload_to='predictions/', null=True, blank=True)
    
    predicted_crop = models.CharField(max_length=100)
    predicted_disease = models.CharField(max_length=200)
    confidence_score = models.FloatField()

    crop = models.ForeignKey(Crop, on_delete=models.SET_NULL, null=True, blank=True)
    disease = models.ForeignKey(Disease, on_delete=models.SET_NULL, null=True, blank=True)
    treatment = models.ForeignKey(Treatment, on_delete=models.SET_NULL, null=True, blank=True)

    actual_crop = models.CharField(max_length=100, blank=True)
    actual_disease = models.CharField(max_length=200, blank=True)
    is_correct = models.BooleanField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.predicted_crop} - {self.predicted_disease} ({self.confidence_score:.2f}%)"

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Prediction Result"
        verbose_name_plural = "Prediction Results"


class CropTip(models.Model):
    """Model to store general crop care tips"""
    crop = models.ForeignKey(Crop, on_delete=models.CASCADE, related_name='tips')
    title = models.CharField(max_length=200)
    content = models.TextField()
    tip_type = models.CharField(max_length=50, choices=[
        ('watering', 'Watering'),
        ('fertilizing', 'Fertilizing'),
        ('pruning', 'Pruning'),
        ('pest_control', 'Pest Control'),
        ('soil_management', 'Soil Management'),
        ('general', 'General Care'),
    ])
    season = models.CharField(max_length=20, choices=[
        ('spring', 'Spring'),
        ('summer', 'Summer'),
        ('autumn', 'Autumn'),
        ('winter', 'Winter'),
        ('all', 'All Year'),
    ], default='all')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.crop.name} - {self.title}"

    class Meta:
        ordering = ['crop__name', 'tip_type', 'title']
