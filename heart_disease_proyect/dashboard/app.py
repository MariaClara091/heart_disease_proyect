# dashboard/app.py
from flask import Flask, render_template, jsonify
import pandas as pd
import joblib
import os
import json

app = Flask(__name__)

# Cargar datos y modelo
def load_project_data():
    """Carga los datos y resultados del proyecto"""
    try:
        # Datos básicos
        df = pd.read_csv("../heart.csv")
        model = joblib.load("../app/model.joblib")
        
        # Resultados de modelos (simulados o cargados de archivos)
        model_results = [
            {"name": "GradientBoosting", "auc": 0.9372, "accuracy": 0.8913, "rank": 1},
            {"name": "KNeighbors", "auc": 0.9333, "accuracy": 0.8804, "rank": 2},
            {"name": "LogisticRegression", "auc": 0.9320, "accuracy": 0.8859, "rank": 3},
            {"name": "RandomForest", "auc": 0.9320, "accuracy": 0.8587, "rank": 4},
            {"name": "SVC", "auc": 0.9311, "accuracy": 0.8641, "rank": 5}
        ]
        
        # Información del dataset
        dataset_info = {
            "rows": len(df),
            "columns": len(df.columns),
            "target_distribution": df['HeartDisease'].value_counts().to_dict(),
            "numeric_features": df.select_dtypes(include=['number']).columns.tolist(),
            "categorical_features": df.select_dtypes(include=['object']).columns.tolist()
        }
        
        # Etapas del proyecto
        project_stages = [
            {"name": "ETAPA 1", "status": "✅ COMPLETADA", "description": "Data Leakage y Múltiples Modelos", "file": "notebooks/1_model_leakage_demo.ipynb"},
            {"name": "ETAPA 2", "status": "✅ COMPLETADA", "description": "Pipeline con Validación Cruzada", "file": "notebooks/2_model_pipeline_cv.ipynb"},
            {"name": "ETAPA 3", "status": "✅ COMPLETADA", "description": "API Flask y Docker", "file": "app/api_flask.py"},
            {"name": "ETAPA 4", "status": "✅ COMPLETADA", "description": "Kubernetes Local", "file": "k8s/deployment.yaml"},
            {"name": "ETAPA 5", "status": "✅ COMPLETADA", "description": "GitHub Actions CI/CD", "file": ".github/workflows/ci.yml"},
            {"name": "ETAPA 6", "status": "✅ COMPLETADA", "description": "Monitoreo de Deriva", "file": "notebooks/3_data_drift_monitoring.ipynb"}
        ]
        
        return {
            "dataset_info": dataset_info,
            "model_results": model_results,
            "project_stages": project_stages,
            "model_type": str(type(model).__name__)
        }
        
    except Exception as e:
        print(f"Error loading data: {e}")
        return {}

@app.route('/')
def index():
    """Página principal del dashboard"""
    project_data = load_project_data()
    return render_template('index.html', **project_data)

@app.route('/api/project-data')
def api_project_data():
    """API endpoint para datos del proyecto"""
    return jsonify(load_project_data())

@app.route('/api/dataset-sample')
def api_dataset_sample():
    """API endpoint para muestra del dataset"""
    try:
        df = pd.read_csv("../heart.csv")
        sample = df.head(10).to_dict('records')
        return jsonify({"sample": sample, "columns": df.columns.tolist()})
    except Exception as e:
        return jsonify({"error": str(e)})

if __name__ == '__main__':
    # Crear carpeta de templates si no existe
    os.makedirs('dashboard/templates', exist_ok=True)
    app.run(host='0.0.0.0', port=5001, debug=True)