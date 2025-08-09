from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.core.paginator import Paginator
from django.db.models import Q
import json
import logging

from .models import Prediction, Crop, Disease, Treatment, CropTip
# from .ai_service import predictor
from django.conf import settings

from .ai_service import AIPredictor
from django.views.decorators.csrf import ensure_csrf_cookie

logger = logging.getLogger(__name__)

predictor = AIPredictor()

@ensure_csrf_cookie
def home(request):
    """Home page view"""
    context = {
        'title': 'AgroDoctor - AI-Powered Crop Disease Detection',
        'description': 'Upload images of crop leaves to detect diseases and get treatment recommendations using AI.'
    }
    return render(request, 'doctor/home.html', context)

@require_http_methods(["POST"])
@csrf_exempt
# def predict_disease(request):
#     """Handle image upload and disease prediction"""
#     try:
#         if 'image' not in request.FILES:
#             return JsonResponse({'success': False, 'error': 'No image file provided'}, status=400)

#         image_file = request.FILES['image']

#         # Validate file type
#         allowed_types = ['image/jpeg', 'image/jpg', 'image/png', 'image/gif']
#         if image_file.content_type not in allowed_types:
#             return JsonResponse({'success': False, 'error': 'Invalid file type. Please upload an image (JPEG, PNG, GIF)'}, status=400)

#         # Validate file size (max 10MB)
#         if image_file.size > 10 * 1024 * 1024:
#             return JsonResponse({'success': False, 'error': 'File size too large. Please upload an image smaller than 10MB'}, status=400)

#         # Ensure file pointer is at start
#         if hasattr(image_file, 'seek'):
#             image_file.seek(0)

#         # Run AI prediction
#         result = predict_disease(image_file)
#         treatments = prediction.get_treatment_recommendations(prediction_result['crop'], prediction_result['disease'])

#         # Save to DB
#         prediction = Prediction.objects.create(
#             image=image_file,
#             predicted_crop=result['crop_name'],
#             predicted_disease=result['disease_name'],
#             confidence_score=result['confidence'],
#             crop=result['crop'],
#             disease=result['disease'],
#             treatment=result['treatment']
#         )

#         return JsonResponse({
#             'success': True,
#             'prediction': {
#                 'crop': result['crop_name'],
#                 'disease': result['disease_name'],
#                 'confidence': result['confidence'],
#                 'class_name': result['predicted_label'],
#                 'prediction_id': prediction.id
#             },
#             'treatments': [
#                 {
#                     'title': result['treatment'].title,
#                     'description': result['treatment'].description,
#                     'treatment_type': result['treatment'].treatment_type,
#                     'instructions': result['treatment'].instructions,
#                     'effectiveness': result['treatment'].effectiveness
#                 }
#             ] if result['treatment'] else [],
#         })

#     except Exception as e:
#         logger.error(f"Prediction error: {str(e)}")
#         return JsonResponse({'success': False, 'error': 'An error occurred during prediction. Please try again.'}, status=500)

def predict_disease(request):
    if request.method == 'POST' and request.FILES.get('image'):
        image_file = request.FILES['image']
        result = predictor.predict(image_file)
        treatments = predictor.get_treatment_recommendations(result['crop'], result['disease'])

        # Save prediction result to DB
        Prediction.objects.create(
            image=image_file,
            predicted_crop=result['crop'],
            predicted_disease=result['disease'],
            confidence_score=result['confidence'],
        )

        # Prepare treatment data
        treatment_data = [{
            'title': t.title,
            'description': getattr(t, 'description', ''),  # Safe for missing field
            'treatment_type': getattr(t, 'treatment_type', ''),
            'effectiveness': getattr(t, 'effectiveness', ''),
            'instructions': t.instructions,
            
        } for t in treatments]

        # Send prediction and treatment as response
        return JsonResponse({
            'success': True,
            'prediction': result,
            'treatments': treatment_data
        })

    return JsonResponse({'success': False, 'error': 'No image uploaded'})
    


def prediction_result(request, prediction_id):
    """Display detailed prediction result"""
    try:
        prediction = Prediction.objects.get(id=prediction_id)
        treatments = [prediction.treatment] if prediction.treatment else []
        tips = prediction.crop.tips.all() if prediction.crop else []

        return render(request, 'doctor/prediction_result.html', {
            'prediction': prediction,
            'treatments': treatments,
            'crop_tips': tips,
            'title': f'Prediction Result - {prediction.predicted_crop}'
        })

    except Prediction.DoesNotExist:
        messages.error(request, 'Prediction not found.')
        return redirect('home')
    except Exception as e:
        logger.error(f"Error displaying prediction result: {e}")
        messages.error(request, 'An error occurred while displaying the result.')
        return redirect('home')


@login_required
def dashboard(request):
    """ dashboard showing prediction history"""
    predictions = Prediction.objects.all().order_by('-created_at')

    paginator = Paginator(predictions, 10)
    page_obj = paginator.get_page(request.GET.get('page'))

    total = predictions.count()
    correct = predictions.filter(is_correct=True).count()
    accuracy = (correct / total * 100) if total > 0 else 0

    return render(request, 'doctor/dashboard.html', {
        'page_obj': page_obj,
        'total_predictions': total,
        'correct_predictions': correct,
        'accuracy': round(accuracy, 2),
        'title': 'Dashboard'
    })
    
def crops_list(request):
    """Display list of supported crops"""
    crops = Crop.objects.all().order_by('name')
    
    context = {
        'crops': crops,
        'title': 'Supported Crops'
    }
    
    return render(request, 'doctor/crops_list.html', context)

def crop_detail(request, crop_id):
    """Display detailed information about a specific crop"""
    try:
        crop = Crop.objects.get(id=crop_id)
        diseases = crop.diseases.all()
        tips = crop.tips.all()
        
        context = {
            'crop': crop,
            'diseases': diseases,
            'tips': tips,
            'title': f'{crop.name} - Crop Information'
        }
        
        return render(request, 'doctor/crop_detail.html', context)
        
    except Crop.DoesNotExist:
        messages.error(request, 'Crop not found.')
        return redirect('crops_list')

def diseases_list(request):
    """Display list of diseases"""
    diseases = Disease.objects.select_related('crop').all().order_by('crop__name', 'name')
    
    # Search functionality
    search_query = request.GET.get('search', '')
    if search_query:
        diseases = diseases.filter(
            Q(name__icontains=search_query) |
            Q(crop__name__icontains=search_query) |
            Q(description__icontains=search_query)
        )
    
    # Pagination
    paginator = Paginator(diseases, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'search_query': search_query,
        'title': 'Diseases Database'
    }
    
    return render(request, 'doctor/diseases_list.html', context)

def disease_detail(request, disease_id):
    """Display detailed information about a specific disease"""
    try:
        disease = Disease.objects.select_related('crop').get(id=disease_id)
        treatments = disease.treatments.all()
        
        context = {
            'disease': disease,
            'treatments': treatments,
            'title': f'{disease.crop.name} - {disease.name}'
        }
        
        return render(request, 'doctor/disease_detail.html', context)
        
    except Disease.DoesNotExist:
        messages.error(request, 'Disease not found.')
        return redirect('diseases_list')

def about(request):
    """About page"""
    context = {
        'title': 'About AgroDoctor',
        'description': 'Learn more about our AI-powered crop disease detection system.'
    }
    return render(request, 'doctor/about.html', context)

def contact(request):
    """Contact page"""
    context = {
        'title': 'Contact Us',
        'description': 'Get in touch with the AgroDoctor team.'
    }
    return render(request, 'doctor/contact.html', context)

def classify_plant_image(request):
    """Alternative API endpoint for prediction"""
    if request.method == 'POST' and request.FILES.get('image'):
        try:
            image_file = request.FILES['image']
            result = predictor.predict(image_file)

            # Get treatments
            treatments = predictor.get_treatment_recommendations(result['crop'], result['disease'])

            # Prepare treatment data
            treatment_data = [{
                'title': t.title,
                'description': getattr(t, 'description', ''),  # Safe for missing field
                'treatment_type': getattr(t, 'treatment_type', ''),
                'effectiveness': getattr(t, 'effectiveness', ''),
                'instructions': t.instructions,
            } for t in treatments]

            # Get crop tips
            crop_obj = None
            try:
                crop_obj = Crop.objects.get(name__iexact=result['crop'].strip())
            except Crop.DoesNotExist:
                pass

            crop_tips = []
            if crop_obj:
                crop_tips = [{
                    'title': tip.title,
                    'content': tip.content,
                    'tip_type': tip.tip_type,
                    'season': tip.season
                } for tip in crop_obj.tips.all()]

            return JsonResponse({
                'success': True,
                'prediction': {
                    'crop': result['crop'],
                    'disease': result['disease'],
                    'confidence': result['confidence'],
                    'class_name': result['class_name']
                },
                'treatments': treatment_data,  # This should always be a list
                'crop_tips': crop_tips,
            })
        except Exception as e:
            logger.error(f"Prediction error: {e}")
            return JsonResponse({'success': False, 'error': 'Failed to predict'}, status=500)
    return JsonResponse({'success': False, 'error': 'No image uploaded'}, status=400)