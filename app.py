from flask import Flask, request, jsonify
from flask_cors import CORS
import joblib
import numpy as np
import os

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Global variables to store the loaded model and label encoder
model = None
label_encoder = None

def load_model_and_encoder():
    """Load the trained Random Forest model and label encoder using joblib"""
    global model, label_encoder
    
    try:
        # Load the Random Forest model using joblib
        model_path = 'crop_recommendation_model.pkl'
        if not os.path.exists(model_path):
            # Try loading from the model directory if not in root
            model_path = os.path.join('model', 'crop_model.pkl')
            
        model = joblib.load(model_path)
        print(f"✅ Random Forest model loaded successfully from {model_path}!")
        
        # Load the label encoder
        encoder_path = 'label_encoder.pkl'
        if not os.path.exists(encoder_path):
            encoder_path = os.path.join('model', 'label_encoder.pkl')
            
        label_encoder = joblib.load(encoder_path)
        print(f"✅ Label encoder loaded successfully from {encoder_path}!")
        
        return True
        
    except FileNotFoundError as e:
        print(f"❌ Error: {e}")
        return False
    except Exception as e:
        print(f"❌ Error loading models: {str(e)}")
        return False

@app.route('/predict', methods=['POST'])
def predict():
    """Predict crop recommendation based on input features"""
    try:
        # Get JSON data from request
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No JSON data provided'}), 400
        
        # Define required fields (matching the model's 8 features)
        required_fields = ['N', 'P', 'K', 'temperature', 'humidity', 'ph', 'rainfall', 'OM']
        
        # Check if all required fields are present
        missing_fields = [field for field in required_fields if field not in data]
        if missing_fields:
            return jsonify({
                'error': f'Missing required fields: {", ".join(missing_fields)}'
            }), 400
        
        # Extract and validate input values
        try:
            features = [
                float(data['N']),
                float(data['P']),
                float(data['K']),
                float(data['temperature']),
                float(data['humidity']),
                float(data['ph']),
                float(data['rainfall']),
                float(data['OM'])
            ]
        except (ValueError, TypeError) as e:
            return jsonify({
                'error': f'Invalid input values. All fields must be numeric. Error: {str(e)}'
            }), 400
        
        # Validate reasonable ranges for inputs
        if not (0 <= features[0] <= 200):  # N
            return jsonify({'error': 'N (Nitrogen) must be between 0 and 200'}), 400
        if not (0 <= features[1] <= 200):  # P
            return jsonify({'error': 'P (Phosphorus) must be between 0 and 200'}), 400
        if not (0 <= features[2] <= 250):  # K (extended for model range)
            return jsonify({'error': 'K (Potassium) must be between 0 and 250'}), 400
        if not (-50 <= features[3] <= 60):  # temperature
            return jsonify({'error': 'Temperature must be between -50 and 60°C'}), 400
        if not (0 <= features[4] <= 100):  # humidity
            return jsonify({'error': 'Humidity must be between 0 and 100%'}), 400
        if not (0 <= features[5] <= 14):  # ph
            return jsonify({'error': 'pH must be between 0 and 14'}), 400
        if not (0 <= features[6] <= 2000):  # rainfall (extended for model range)
            return jsonify({'error': 'Rainfall must be between 0 and 2000mm'}), 400
        if not (0 <= features[7] <= 15):  # OM
            return jsonify({'error': 'Organic Matter (OM) must be between 0 and 15%'}), 400
        
        # Check if models are loaded
        if model is None or label_encoder is None:
            return jsonify({'error': 'Models not loaded. Please restart the server.'}), 500
        
        # Make prediction
        features_array = np.array(features).reshape(1, -1)
        prediction_encoded = model.predict(features_array)[0]
        
        # Decode the prediction using label encoder
        crop_name = label_encoder.inverse_transform([prediction_encoded])[0]
        
        # Get prediction probability if available
        try:
            probabilities = model.predict_proba(features_array)[0]
            max_prob = max(probabilities)
            confidence = round(max_prob * 100, 2)
            # Build top-3 predictions list
            top_indices = np.argsort(probabilities)[::-1][:3]
            class_labels = label_encoder.inverse_transform(top_indices)
            top_predictions = []
            for idx, label in zip(top_indices, class_labels):
                top_predictions.append({
                    'crop': str(label),
                    'probability': round(float(probabilities[idx]) * 100, 2)
                })
        except Exception:
            confidence = None
            top_predictions = None
        
        return jsonify({
            'best_crop': crop_name,
            'confidence': confidence,
            'message': f'Recommended crop: {crop_name}',
            'top_predictions': top_predictions
        })
        
    except Exception as e:
        return jsonify({'error': f'Internal server error: {str(e)}'}), 500

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'model_loaded': model is not None,
        'label_encoder_loaded': label_encoder is not None
    })

@app.route('/', methods=['GET'])
def home():
    """Home endpoint with API documentation"""
    return jsonify({
        'message': 'Crop Recommendation API',
        'endpoints': {
            '/predict': 'POST - Predict crop recommendation',
            '/health': 'GET - Health check',
            '/': 'GET - API documentation'
        },
        'usage': {
            'method': 'POST',
            'url': '/predict',
            'content_type': 'application/json',
            'body': {
                'N': 'Nitrogen level (0-200)',
                'P': 'Phosphorus level (0-200)',
                'K': 'Potassium level (0-200)',
                'temperature': 'Temperature in Celsius (-50 to 60)',
                'humidity': 'Humidity percentage (0-100)',
                'ph': 'pH level (0-14)',
                'rainfall': 'Rainfall in mm (0-1000)'
            }
        }
    })

if __name__ == '__main__':
    # Load the model and label encoder when starting the app
    if load_model_and_encoder():
        print("🚀 Starting Flask server...")
        print("API Documentation available at: http://localhost:8000/")
        print("Health check available at: http://localhost:8000/health")
        app.run(debug=True, host='0.0.0.0', port=8000)
    else:
        print("❌ Failed to load models. Please check that both pickle files exist.")
