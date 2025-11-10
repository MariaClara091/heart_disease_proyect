# app/api_flask.py
from flask import Flask, request, jsonify
import pandas as pd
import numpy as np
import joblib
import os

# Crear aplicación Flask
app = Flask(__name__)

# Cargar el modelo entrenado
try:
    model = joblib.load("app/model_cv.joblib")
    print("Modelo cargado correctamente")
except Exception as e:
    print(f"Error cargando el modelo: {e}")
    raise

# Función para validar datos de entrada
def validate_patient_data(data):
    """Valida los datos del paciente"""
    required_fields = [
        'Age', 'Sex', 'ChestPainType', 'RestingBP', 'Cholesterol', 
        'FastingBS', 'RestingECG', 'MaxHR', 'ExerciseAngina', 'Oldpeak', 'ST_Slope'
    ]
    
    # Verificar campos requeridos
    for field in required_fields:
        if field not in data:
            return False, f"Campo requerido faltante: {field}"
    
    # Validaciones básicas de tipos y rangos
    try:
        age = int(data['Age'])
        if not (20 <= age <= 100):
            return False, "Age debe estar entre 20 y 100"
        
        resting_bp = int(data['RestingBP'])
        if not (80 <= resting_bp <= 200):
            return False, "RestingBP debe estar entre 80 y 200"
            
        cholesterol = int(data['Cholesterol'])
        if not (100 <= cholesterol <= 600):
            return False, "Cholesterol debe estar entre 100 y 600"
            
        max_hr = int(data['MaxHR'])
        if not (60 <= max_hr <= 220):
            return False, "MaxHR debe estar entre 60 y 220"
            
        oldpeak = float(data['Oldpeak'])
        if oldpeak < 0 or oldpeak > 10:
            return False, "Oldpeak debe estar entre 0 y 10"
            
    except (ValueError, TypeError) as e:
        return False, f"Error en tipos de datos: {str(e)}"
    
    return True, "Datos válidos"

# Función para preprocesar datos
def preprocess_input(data):
    """Preprocesa los datos de entrada igual que durante el entrenamiento"""
    
    # Crear DataFrame
    input_dict = {
        'Age': [data['Age']],
        'Sex': [data['Sex']],
        'ChestPainType': [data['ChestPainType']],
        'RestingBP': [data['RestingBP']],
        'Cholesterol': [data['Cholesterol']],
        'FastingBS': [data['FastingBS']],
        'RestingECG': [data['RestingECG']],
        'MaxHR': [data['MaxHR']],
        'ExerciseAngina': [data['ExerciseAngina']],
        'Oldpeak': [data['Oldpeak']],
        'ST_Slope': [data['ST_Slope']]
    }
    
    df = pd.DataFrame(input_dict)
    
    # Aplicar one-hot encoding igual que en entrenamiento
    categorical_cols = ['Sex', 'ChestPainType', 'RestingECG', 'ExerciseAngina', 'ST_Slope']
    df_encoded = pd.get_dummies(df, columns=categorical_cols, drop_first=True)
    
    # Asegurar que tengamos todas las columnas esperadas por el modelo
    expected_columns = [
        'Age', 'RestingBP', 'Cholesterol', 'FastingBS', 'MaxHR', 'Oldpeak',
        'Sex_M', 'ChestPainType_ATA', 'ChestPainType_NAP', 'ChestPainType_TA',
        'RestingECG_Normal', 'RestingECG_ST', 'ExerciseAngina_Y', 'ST_Slope_Flat', 'ST_Slope_Up'
    ]
    
    # Agregar columnas faltantes con valor 0
    for col in expected_columns:
        if col not in df_encoded.columns:
            df_encoded[col] = 0
    
    # Reordenar columnas
    df_encoded = df_encoded[expected_columns]
    
    return df_encoded

@app.route('/')
def root():
    """Endpoint de bienvenida"""
    return jsonify({
        "message": "Heart Disease Prediction API (Flask)",
        "version": "1.0.0",
        "endpoints": {
            "health": "/health",
            "predict": "/predict (POST)",
            "model_info": "/model-info"
        }
    })

@app.route('/health', methods=['GET'])
def health_check():
    """Endpoint para verificar el estado de la API"""
    return jsonify({
        "status": "healthy",
        "model_loaded": True,
        "message": "API funcionando correctamente"
    })

@app.route('/model-info', methods=['GET'])
def model_info():
    """Endpoint para obtener información del modelo"""
    return jsonify({
        "model_type": str(type(model.named_steps['clf']).__name__),
        "api_version": "1.0.0",
        "framework": "Flask"
    })

@app.route('/predict', methods=['POST'])
def predict():
    """
    Realiza predicción de enfermedad cardíaca
    
    Espera JSON con:
    - Age: Edad del paciente [años]
    - Sex: Sexo del paciente [M, F]
    - ChestPainType: Tipo de dolor pectoral [ATA, NAP, ASY, TA]
    - RestingBP: Presión arterial en reposo [mm Hg]
    - Cholesterol: Colesterol [mg/dl]
    - FastingBS: Azúcar en ayunas [0, 1]
    - RestingECG: ECG en reposo [Normal, ST, LVH]
    - MaxHR: Frecuencia cardíaca máxima [latidos/minuto]
    - ExerciseAngina: Angina inducida por ejercicio [N, Y]
    - Oldpeak: Depresión del ST [valor numérico]
    - ST_Slope: Pendiente del ST [Up, Flat, Down]
    """
    try:
        # Obtener datos JSON
        data = request.get_json()
        
        if not data:
            return jsonify({"error": "Se esperaba JSON en el cuerpo"}), 400
        
        # Validar datos
        is_valid, validation_message = validate_patient_data(data)
        if not is_valid:
            return jsonify({"error": validation_message}), 400
        
        # Preprocesar datos
        input_data = preprocess_input(data)
        
        # Realizar predicción
        probability = model.predict_proba(input_data)[0][1]
        prediction = int(probability > 0.5)
        
        # Determinar nivel de riesgo
        if probability < 0.3:
            risk_level = "Bajo"
        elif probability < 0.7:
            risk_level = "Moderado"
        else:
            risk_level = "Alto"
        
        return jsonify({
            "heart_disease_probability": round(probability, 4),
            "prediction": prediction,
            "risk_level": risk_level,
            "interpretation": "Enfermo" if prediction == 1 else "Sano"
        })
        
    except Exception as e:
        return jsonify({"error": f"Error en la predicción: {str(e)}"}), 500

# Cliente de prueba integrado
class HeartDiseaseClient:
    """Cliente para probar la API sin dependencias externas"""
    
    def __init__(self, base_url="http://localhost:5000"):
        self.base_url = base_url
        self.test_patients = [
            {
                "Age": 52,
                "Sex": "M",
                "ChestPainType": "ASY",
                "RestingBP": 125,
                "Cholesterol": 212,
                "FastingBS": 0,
                "RestingECG": "Normal",
                "MaxHR": 168,
                "ExerciseAngina": "N",
                "Oldpeak": 1.0,
                "ST_Slope": "Flat"
            },
            {
                "Age": 45,
                "Sex": "F", 
                "ChestPainType": "ATA",
                "RestingBP": 130,
                "Cholesterol": 240,
                "FastingBS": 0,
                "RestingECG": "Normal",
                "MaxHR": 150,
                "ExerciseAngina": "N",
                "Oldpeak": 0.5,
                "ST_Slope": "Up"
            }
        ]
    
    def test_health(self):
        """Prueba el endpoint de health"""
        try:
            import requests
            response = requests.get(f"{self.base_url}/health")
            print("Health Check:", response.json())
            return True
        except Exception as e:
            print(f"Error en health check: {e}")
            return False
    
    def test_prediction(self, patient_index=0):
        """Prueba una predicción"""
        try:
            import requests
            patient_data = self.test_patients[patient_index]
            response = requests.post(f"{self.base_url}/predict", json=patient_data)
            
            if response.status_code == 200:
                result = response.json()
                print("Predicción exitosa:")
                print(f"   Probabilidad: {result['heart_disease_probability']:.2%}")
                print(f"   Predicción: {result['interpretation']}")
                print(f"   Nivel de riesgo: {result['risk_level']}")
                return True
            else:
                print("Error en predicción:", response.json())
                return False
        except Exception as e:
            print(f"Error en predicción: {e}")
            return False

if __name__ == "__main__":
    print("Iniciando Heart Disease Prediction API (Flask)")
    print("Endpoints disponibles:")
    print("   • http://localhost:5000/")
    print("   • http://localhost:5000/health") 
    print("   • http://localhost:5000/predict (POST)")
    print("   • http://localhost:5000/model-info")
    print("\n Para ejecutar: python app/api_flask.py")
    print(" Para probar: python tests/test_flask_api.py")
    
    # Ejecutar servidor
    app.run(host="0.0.0.0", port=5000, debug=True)