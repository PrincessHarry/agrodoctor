from django.core.files.uploadedfile import InMemoryUploadedFile
from PIL import Image
import numpy as np
import tensorflow as tf
import os

from .models import Disease, Treatment, Crop

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

class AIPredictor:
    def __init__(self):
        self.model_path = os.path.join(BASE_DIR, 'plant_model_v5-beta.h5')
        
        # Define the class names as dictionary (matching Gradio code)
        self.class_names = {
            0: 'Apple___Apple_scab',
            1: 'Apple___Black_rot',
            2: 'Apple___Cedar_apple_rust',
            3: 'Apple___healthy',
            4: 'Not a plant',
            5: 'Blueberry___healthy',
            6: 'Cherry___Powdery_mildew',
            7: 'Cherry___healthy',
            8: 'Corn___Cercospora_leaf_spot Gray_leaf_spot',
            9: 'Corn___Common_rust',
            10: 'Corn___Northern_Leaf_Blight',
            11: 'Corn___healthy',
            12: 'Grape___Black_rot',
            13: 'Grape___Esca_(Black_Measles)',
            14: 'Grape___Leaf_blight_(Isariopsis_Leaf_Spot)',
            15: 'Grape___healthy',
            16: 'Orange___Haunglongbing_(Citrus_greening)',
            17: 'Peach___Bacterial_spot',
            18: 'Peach___healthy',
            19: 'Pepper,_bell___Bacterial_spot',
            20: 'Pepper,_bell___healthy',
            21: 'Potato___Early_blight',
            22: 'Potato___Late_blight',
            23: 'Potato___healthy',
            24: 'Raspberry___healthy',
            25: 'Soybean___healthy',
            26: 'Squash___Powdery_mildew',
            27: 'Strawberry___Leaf_scorch',
            28: 'Strawberry___healthy',
            29: 'Tomato___Bacterial_spot',
            30: 'Tomato___Early_blight',
            31: 'Tomato___Late_blight',
            32: 'Tomato___Leaf_Mold',
            33: 'Tomato___Septoria_leaf_spot',
            34: 'Tomato___Spider_mites Two-spotted_spider_mite',
            35: 'Tomato___Target_Spot',
            36: 'Tomato___Tomato_Yellow_Leaf_Curl_Virus',
            37: 'Tomato___Tomato_mosaic_virus',
            38: 'Tomato___healthy'
        }
        
        # Treatment recommendations dictionary
        self.keras_treatments = {
            'Apple___Apple_scab': "Remove fallen leaves and prune infected branches. Apply fungicides containing captan or myclobutanil.",
            'Apple___Black_rot': "Prune out dead branches. Spray copper-based fungicide during early fruit development.",
            'Apple___Cedar_apple_rust': "Remove nearby juniper trees. Apply fungicides before bud break.",
            'Apple___healthy': "No action required. The plant is healthy.",
            'Blueberry___healthy': "No action required. The plant is healthy.",
            'Cherry___Powdery_mildew': "Apply sulfur-based fungicide. Ensure good air circulation around the plant.",
            'Cherry___healthy': "No action required. The plant is healthy.",
            'Corn___Cercospora_leaf_spot Gray_leaf_spot': "Rotate crops to avoid build-up of pathogens. Use resistant hybrids and apply foliar fungicides.",
            'Corn___Common_rust': "Plant rust-resistant hybrids. Apply fungicides at the first sign of rust.",
            'Corn___Northern_Leaf_Blight': "Use resistant varieties and apply fungicides when lesions are observed.",
            'Corn___healthy': "No action required. The plant is healthy.",
            'Grape___Black_rot': "Remove and destroy infected leaves and fruits. Apply fungicides containing myclobutanil or captan.",
            'Grape___Esca_(Black_Measles)': "Prune and destroy infected wood. Apply fungicides during the growing season.",
            'Grape___Leaf_blight_(Isariopsis_Leaf_Spot)': "Maintain good air circulation. Spray protective fungicides like mancozeb.",
            'Grape___healthy': "No action required. The plant is healthy.",
            'Orange___Haunglongbing_(Citrus_greening)': "Remove and destroy infected trees. Control psyllid vectors with insecticides.",
            'Peach___Bacterial_spot': "Apply copper-based bactericides. Use resistant varieties and avoid overhead irrigation.",
            'Peach___healthy': "No action required. The plant is healthy.",
            'Pepper,_bell___Bacterial_spot': "Apply copper-based sprays. Use certified seeds and avoid overhead irrigation.",
            'Pepper,_bell___healthy': "No action required. The plant is healthy.",
            'Potato___Early_blight': "Use certified seeds and apply preventative fungicides like chlorothalonil.",
            'Potato___Late_blight': "Plant disease-free tubers and use fungicides containing metalaxyl.",
            'Potato___healthy': "No action required. The plant is healthy.",
            'Raspberry___healthy': "No action required. The plant is healthy.",
            'Soybean___healthy': "No action required. The plant is healthy.",
            'Squash___Powdery_mildew': "Use sulfur-based fungicides and ensure good ventilation.",
            'Strawberry___Leaf_scorch': "Remove infected leaves. Apply fungicides containing myclobutanil.",
            'Strawberry___healthy': "No action required. The plant is healthy.",
            'Tomato___Bacterial_spot': "Apply copper-based sprays. Avoid overhead watering.",
            'Tomato___Early_blight': "Prune infected leaves and apply fungicides containing chlorothalonil or mancozeb.",
            'Tomato___Late_blight': "Remove infected plants. Apply fungicides containing chlorothalonil or metalaxyl.",
            'Tomato___Leaf_Mold': "Ensure good ventilation and apply fungicides like mancozeb.",
            'Tomato___Septoria_leaf_spot': "Remove infected leaves and apply fungicides containing chlorothalonil.",
            'Tomato___Spider_mites Two-spotted_spider_mite': "Spray insecticidal soap or neem oil. Maintain humidity levels.",
            'Tomato___Target_Spot': "Use resistant varieties. Apply fungicides containing chlorothalonil.",
            'Tomato___Tomato_Yellow_Leaf_Curl_Virus': "Remove infected plants. Use resistant varieties and control whitefly vectors.",
            'Tomato___Tomato_mosaic_virus': "Remove infected plants and disinfect tools. Use resistant seed varieties.",
            'Tomato___healthy': "No action required. The plant is healthy.",
            'Unknown': "No specific treatment available."
        }
        
        self.model = tf.keras.models.load_model(self.model_path)

    def preprocess_image(self, image: InMemoryUploadedFile):
        # Convert to numpy array and resize to 256x256 (matching Gradio preprocessing)
        img = Image.open(image).convert('RGB')
        img_array = np.array(img)
        img_array = tf.image.resize(img_array, [256, 256])
        img_array = tf.expand_dims(img_array, 0) / 255.0
        return img_array

    def predict(self, image: InMemoryUploadedFile):
        processed_image = self.preprocess_image(image)
        predictions = self.model.predict(processed_image)
        predicted_class_idx = tf.argmax(predictions[0], axis=-1).numpy()
        confidence = float(np.max(predictions[0]))
        
        # Get predicted label from dictionary
        predicted_label = self.class_names.get(predicted_class_idx, "Unknown")
        
        # Check confidence threshold (like in Gradio)
        if confidence < 0.60:
            class_name = "Uncertain / Not in dataset"
            crop, disease = "Unknown", "Unknown"
        else:
            class_name = predicted_label
            # Split class_name into crop and disease
            if "___" in class_name:
                crop, disease = class_name.split("___", 1)
            else:
                crop, disease = class_name, ""

        return {
            "class_name": class_name,
            "crop": crop,
            "disease": disease,
            "confidence": round(confidence * 100, 2)
        }

    def get_treatment_recommendations(self, crop, disease):
        # Use the treatment dictionary from Gradio code
        class_name = f"{crop}___{disease}" if crop and disease else "Unknown"
        treatment_text = self.keras_treatments.get(class_name, "No specific treatment available.")
        
        # Return as a list with one treatment object (for compatibility with existing code)
        return [type('Treatment', (), {
            'title': f"Treatment for {crop} - {disease}",
            'instructions': treatment_text,
            'description': treatment_text,
            'treatment_type': 'General',
            'effectiveness': 'Medium'
        })()]