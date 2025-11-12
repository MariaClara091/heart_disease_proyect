# tests/test_flask_api.py
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from app.api import HeartDiseaseClient

def run_tests():
    """Ejecuta pruebas de la API Flask"""
    print("EJECUTANDO PRUEBAS DE LA API FLASK")
    print("=" * 50)
    
    client = HeartDiseaseClient()
    
    # Prueba health check
    print("\n1. Probando Health Check...")
    health_ok = client.test_health()
    
    # Prueba predicciones
    print("\n2. Probando Predicciones...")
    for i in range(2):
        print(f"\n   Paciente {i + 1}:")
        prediction_ok = client.test_prediction(i)
    

    print("RESUMEN DE PRUEBAS:")
    print("   Para ejecutar la API: python app/api.py")
    print("   Luego ejecuta este test: python tests/test_api.py")

if __name__ == "__main__":
    run_tests()