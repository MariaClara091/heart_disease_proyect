# Heart Disease Prediction - MLOps Pipeline
# Autores: María Clara Ávila, Mateo José Giraldo y David Alejandro Ibáñez
Proyecto completo de Machine Learning que implementa un pipeline de MLOps para predecir enfermedades cardíacas, desde el modelado hasta el despliegue en producción.

## Etapas del Proyecto

### ETAPA 1: Preprocesamiento y Detección de Data Leakage
- **Archivo**: `notebooks/1_model_leakage_demo.ipynb`
- **Objetivo**: Demostrar el impacto del data leakage vs flujo correcto
- **Modelos comparados**: SVC, LogisticRegression, RandomForest, KNeighbors, GradientBoosting
- **Métricas**: AUC, Accuracy, ranking comparativo

### ETAPA 2: Modelado con Validación Segura  
- **Archivo**: `notebooks/2_model_pipeline_cv.ipynb`
- **Objetivo**: Implementación correcta con Pipeline y GridSearchCV
- **Características**: División estratificada antes del escalado
- **Evaluación**: Matriz de confusión, curva ROC, validación cruzada

### ETAPA 3: Despliegue con Flask y Docker
- **API**: `app/api_flask.py` - Endpoints REST para predicciones
- **Docker**: `docker/Dockerfile` - Contenerización de la aplicación
- **Modelo**: `app/model.joblib` - Modelo entrenado para producción

### ETAPA 4: Despliegue en Kubernetes Local
- **Archivos**: `k8s/deployment.yaml`, `k8s/service.yaml`
- **Configuración**: 2 réplicas, LoadBalancer, recursos optimizados
- **Endpoint**: `http://localhost/health`

### ETAPA 5: Integración Continua con GitHub Actions
- **Archivo**: `.github/workflows/ci.yml`
- **Funcionalidad**: Tests automáticos y build de Docker en push
- **Jobs**: Test de modelo, build de imagen, verificaciones de seguridad

### ETAPA 6: Monitoreo de Deriva de Datos
- **Archivo**: `notebooks/3_data_drift_monitoring.ipynb`
- **Objetivo**: Detectar cambios en la distribución de datos
- **Métricas**: Análisis de deriva por feature, performance comparativo

## Quick Start

### Ejecución Local
```bash
# Instalar dependencias
pip install -r docker/requirements.txt

# Ejecutar API local
python app/api_flask.py

## 🔌 API Endpoints

### Health Check
```cmd
# En Anaconda Prompt (Windows):
curl http://localhost:5000/health

# O si no tienes curl:

python -c "import requests; print(requests.get('http://localhost:5000/health').json())"
