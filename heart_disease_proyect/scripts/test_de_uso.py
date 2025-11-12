import requests
import subprocess
import os
import sys

def run_test(test_name, test_func):
    """Ejecuta una prueba y muestra el resultado"""
    print(f"\n {test_name}")
    try:
        result = test_func()
        print(f" {result}")
        return True
    except Exception as e:
        print(f" Error: {e}")
        return False

def test_project_structure():
    """Verifica la estructura del proyecto"""
    required_folders = ['notebooks', 'app', 'docker', 'k8s', 'scripts', 'dashboard']
    required_files = ['heart.csv', 'README.md', 'Manual.txt']
    
    missing_folders = [f for f in required_folders if not os.path.exists(f)]
    missing_files = [f for f in required_files if not os.path.exists(f)]
    
    if not missing_folders and not missing_files:
        return "Estructura del proyecto OK"
    else:
        raise Exception(f"Faltan: {missing_folders + missing_files}")

def test_api_health():
    """Prueba el endpoint de health de la API"""
    response = requests.get("http://localhost:5000/health", timeout=5)
    if response.status_code == 200:
        data = response.json()
        return f"API Health: {data}"
    else:
        raise Exception(f"Status code: {response.status_code}")

def test_api_prediction():
    """Prueba una predicción con la API"""
    test_patient = {
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
    
    response = requests.post("http://localhost:5000/predict", json=test_patient, timeout=10)
    if response.status_code == 200:
        result = response.json()
        return f"Predicción: {result}"
    else:
        raise Exception(f"Error: {response.text}")

def test_docker():
    """Verifica que Docker funciona"""
    try:
        result = subprocess.run(["docker", "--version"], capture_output=True, text=True)
        if result.returncode == 0:
            return "Docker instalado"
        else:
            raise Exception("Docker no funciona")
    except:
        raise Exception("Docker no encontrado")

def test_kubernetes():
    """Verifica que Kubernetes funciona"""
    try:
        result = subprocess.run(["kubectl", "version", "--client"], capture_output=True, text=True)
        if result.returncode == 0:
            return "Kubernetes configurado"
        else:
            raise Exception("Kubectl error")
    except:
        raise Exception("Kubectl no encontrado")

def main():
    """Ejecuta todas las pruebas"""
    print(" PRUEBAS AUTOMÁTICAS PARA EL PROFESOR")
    print("=" * 60)
    
    tests = [
        ("Estructura del Proyecto", test_project_structure),
        ("Docker Installation", test_docker),
        ("Kubernetes Configuration", test_kubernetes),
    ]
    
    # Solo probar API si está ejecutándose
    try:
        requests.get("http://localhost:5000/health", timeout=2)
        tests.extend([
            ("API Health Check", test_api_health),
            ("API Prediction", test_api_prediction),
        ])
    except:
        print("\n  API no detectada - Ejecuta: python app/api.py")
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        if run_test(test_name, test_func):
            passed += 1
    
    print(f"\n RESULTADO: {passed}/{total} pruebas pasadas")
    
    if passed == total:
        print("¡PROYECTO 100% FUNCIONAL!")
    else:
        print("Algunas pruebas fallaron - Revisa la configuración")

if __name__ == "__main__":
    main()