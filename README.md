# 🌱 AgroDoctor - AI-Powered Crop Disease Detection

AgroDoctor is an intelligent web application that uses advanced machine learning to detect plant diseases from uploaded images. Built with Django and TensorFlow, it provides instant disease identification, treatment recommendations, and care tips for 14+ crop types.

## 🚀 Features

### 🤖 AI-Powered Detection
- **Advanced Deep Learning**: State-of-the-art CNN model trained on thousands of plant images
- **High Accuracy**: 95%+ accuracy in disease detection across multiple crop types
- **Real-time Analysis**: Instant results with confidence scores
- **Multi-class Classification**: Detects 38+ different diseases and conditions

### 🌾 Supported Crops
- **Apple** - Apple scab, Black rot, Cedar apple rust
- **Blueberry** - Healthy monitoring
- **Cherry** - Powdery mildew detection
- **Corn (Maize)** - Leaf spot, Common rust, Northern leaf blight
- **Grape** - Black rot, Esca, Leaf blight
- **Orange** - Citrus greening (Huanglongbing)
- **Peach** - Bacterial spot detection
- **Pepper (Bell)** - Bacterial spot monitoring
- **Potato** - Early blight, Late blight
- **Raspberry** - Health monitoring
- **Soybean** - Health monitoring
- **Squash** - Powdery mildew
- **Strawberry** - Leaf scorch
- **Tomato** - Multiple diseases including blight, mold, viruses

### 💡 Smart Recommendations
- **Treatment Plans**: Detailed treatment instructions for each detected disease
- **Care Tips**: Seasonal care recommendations for healthy crop maintenance
- **Prevention Strategies**: Proactive measures to prevent disease spread


### 📱 User-Friendly Interface
- **Drag & Drop Upload**: Easy image upload with preview
- **Responsive Design**: Works on desktop, tablet, and mobile
- **Real-time Feedback**: Loading states and progress indicators
- **Detailed Results**: Comprehensive analysis with confidence scores

## 🛠️ Technology Stack

### Backend
- **Django** - Web framework
- **TensorFlow** - Machine learning framework
- **Pillow** - Image processing
- **NumPy** - Numerical computations

### Frontend
- **HTML5/CSS3** - Structure and styling
- **JavaScript** - Interactive functionality
- **Tailwind CSS** - Utility-first CSS framework
- **Font Awesome** - Icons

### AI/ML
- **Convolutional Neural Network (CNN)** - Disease classification
- **Transfer Learning** - Pre-trained model adaptation
- **Image Preprocessing** - 256x256 resize and normalization

## 📋 Prerequisites

Before running AgroDoctor, ensure you have:

- **Python 3.8+**
- **pip** (Python package installer)
- **Git** (for cloning the repository)
- **Virtual environment** (recommended)

## 🚀 Installation

### 1. Clone the Repository
```bash
git clone https://github.com/yourusername/agrodoctor.git
cd agrodoctor
```

### 2. Create Virtual Environment
```bash
python -m venv venv

# On Windows
venv\Scripts\activate

# On macOS/Linux
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Set Up Environment Variables
Create a `.env` file in the project root:
```env
DEBUG=True
SECRET_KEY=your-secret-key-here
ALLOWED_HOSTS=localhost,127.0.0.1
```

### 5. Run Database Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### 6. Create Superuser (Optional)
```bash
python manage.py createsuperuser
```

### 7. Run the Development Server
```bash
python manage.py runserver
```

Visit `http://127.0.0.1:8000` to access the application.



## 🎯 Usage

### 1. Upload Image
- Navigate to the home page
- Click "Choose File" or drag & drop an image
- Supported formats: JPEG, PNG, GIF
- Maximum file size: 10MB

### 2. Analyze Disease
- Click "Analyze Image" button
- Wait for AI processing (typically 2-5 seconds)
- View results with confidence scores

### 3. Review Results
- **Crop Type**: Identified plant species
- **Disease**: Detected disease or condition
- **Confidence**: AI confidence percentage
- **Treatments**: Recommended treatment plans
- **Care Tips**: General crop care advice

## 🔧 Configuration

### Model Configuration
The AI model is configured in `doctor/ai_service.py`:
- **Model Path**: `plant_model_v5-beta.h5`
- **Input Size**: 256x256 pixels
- **Confidence Threshold**: 60%



## 🧪 Testing

### Run Tests
```bash
python manage.py test
```

### Manual Testing
1. Upload healthy plant images
2. Upload diseased plant images
3. Test with different crop types
4. Verify treatment recommendations

## 📊 Performance

### Model Performance
- **Accuracy**: 95%+ on test dataset
- **Inference Time**: <5 seconds per image
- **Memory Usage**: ~500MB RAM
- **Supported Formats**: JPEG, PNG, GIF

### System Requirements
- **CPU**: 2+ cores recommended
- **RAM**: 4GB minimum, 8GB recommended
- **Storage**: 1GB free space
- **GPU**: Optional (CUDA support for faster inference)

## 🤝 Contributing

We welcome contributions! Please follow these steps:

1. **Fork** the repository
2. **Create** a feature branch (`git checkout -b feature/amazing-feature`)
3. **Commit** your changes (`git commit -m 'Add amazing feature'`)
4. **Push** to the branch (`git push origin feature/amazing-feature`)
5. **Open** a Pull Request

### Development Guidelines
- Follow PEP 8 style guidelines
- Add tests for new features
- Update documentation as needed
- Ensure all tests pass before submitting

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **PlantVillage Dataset** - Training data source
- **TensorFlow Team** - Machine learning framework
- **Django Community** - Web framework
- **Open Source Contributors** - Various libraries and tools

## 📞 Support

### Issues
If you encounter any problems:
1. Check the [Issues](https://github.com/yourusername/agrodoctor/issues) page
2. Create a new issue with detailed description
3. Include error logs and system information


## 🔮 Roadmap

### Upcoming Features
- [ ] **Mobile App** - Native iOS/Android applications
- [ ] **Offline Mode** - Local model inference
- [ ] **Multi-language Support** - Internationalization
- [ ] **Advanced Analytics** - Detailed crop health reports
- [ ] **Weather Integration** - Disease risk assessment
- [ ] **Community Features** - User forums and sharing

