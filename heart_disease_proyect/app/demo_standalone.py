# app/demo_standalone.py
import joblib
import pandas as pd
import numpy as np

class HeartDiseasePredictor:
    """Predictor de enfermedad cardíaca sin necesidad de servidor"""
    
    def __init__(self, model_path="app/model_cv.joblib"):
        try:
            self.model = joblib.load(model_path)
            print("Modelo cargado correctamente")
        except Exception as e:
            print(f"Error cargando modelo: {e}")
            raise
    
    def preprocess_input(self, data):
        """Preprocesa datos de entrada"""
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
        
        # Aplicar one-hot encoding
        categorical_cols = ['Sex', 'ChestPainType', 'RestingECG', 'ExerciseAngina', 'ST_Slope']
        df_encoded = pd.get_dummies(df, columns=categorical_cols, drop_first=True)
        
        # Columnas esperadas
        expected_columns = [
            'Age', 'RestingBP', 'Cholesterol', 'FastingBS', 'MaxHR', 'Oldpeak',
            'Sex_M', 'ChestPainType_ATA', 'ChestPainType_NAP', 'ChestPainType_TA',
            'RestingECG_Normal', 'RestingECG_ST', 'ExerciseAngina_Y', 'ST_Slope_Flat', 'ST_Slope_Up'
        ]
        
        # Agregar columnas faltantes
        for col in expected_columns:
            if col not in df_encoded.columns:
                df_encoded[col] = 0
        
        return df_encoded[expected_columns]
    
    def predict(self, patient_data):
        """Realiza predicción para un paciente"""
        try:
            # Preprocesar
            input_data = self.preprocess_input(patient_data)
            
            # Predecir
            probability = self.model.predict_proba(input_data)[0][1]
            prediction = int(probability > 0.5)
            
            # Determinar riesgo
            if probability < 0.3:
                risk_level = "Bajo"
            elif probability < 0.7:
                risk_level = "Moderado"
            else:
                risk_level = "Alto"
            
            return {
                "heart_disease_probability": round(probability, 4),
                "prediction": prediction,
                "risk_level": risk_level,
                "interpretation": "Enfermo" if prediction == 1 else "Sano"
            }
            
        except Exception as e:
            return {"error": str(e)}
    
    def batch_predict(self, patients_data):
        """Predicciones para múltiples pacientes"""
        results = []
        for i, patient in enumerate(patients_data):
            result = self.predict(patient)
            result['patient_id'] = i + 1
            results.append(result)
        return results

# Ejemplo de uso
if __name__ == "__main__":
    print("DEMOSTRACIÓN PREDICCIÓN ENFERMEDAD CARDÍACA")
    
    # Inicializar predictor
    predictor = HeartDiseasePredictor()
    
    # Datos de ejemplo
    test_patients = [
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
    
    # Realizar predicciones
    print("\n REALIZANDO PREDICCIONES...")
    for i, patient in enumerate(test_patients):
        print(f"\n Paciente {i + 1}:")
        result = predictor.predict(patient)
        
        if "error" not in result:
            print(f"    Probabilidad: {result['heart_disease_probability']:.2%}")
            print(f"    Diagnóstico: {result['interpretation']}")
            print(f"    Nivel de riesgo: {result['risk_level']}")
            print(f"    Predicción binaria: {result['prediction']}")
        else:
            print(f"    Error: {result['error']}")
    
    print("Demostración completada!")
    print("Para usar en tu código:")
    print("   from app.demo_standalone import HeartDiseasePredictor")
    print("   predictor = HeartDiseasePredictor()")
    print("   result = predictor.predict(patient_data)")