# scripts/test_ci_locally.py
import os
import subprocess
import sys

def run_ci_checks():
    """Ejecuta verificaciones similares a GitHub Actions localmente"""
    print("EJECUTANDO VERIFICACIONES CI LOCALES")
    
    checks_passed = True
    
    # 1. Verificar dataset
    print("\n1.  VERIFICANDO DATASET...")
    if os.path.exists("heart.csv"):
        try:
            import pandas as pd
            df = pd.read_csv("heart.csv")
            print(f"    Dataset encontrado - Shape: {df.shape}")
        except Exception as e:
            print(f"    Error leyendo dataset: {e}")
            checks_passed = False
    else:
        print("    Dataset no encontrado")
        checks_passed = False
    
    # 2. Verificar modelo
    print("\n2. VERIFICANDO MODELO...")
    if os.path.exists("app/model.joblib"):
        try:
            import joblib
            model = joblib.load("app/model.joblib")
            print(f"    Modelo cargado - Tipo: {type(model)}")
            
            # Verificar que puede predecir
            if hasattr(model, 'predict'):
                print("    Modelo puede hacer predicciones")
            else:
                print("     Modelo no tiene método predict")
                
        except Exception as e:
            print(f"    Error cargando modelo: {e}")
            checks_passed = False
    else:
        print("    Modelo no encontrado")
        checks_passed = False
    
    # 3. Verificar requirements
    print("\n3. VERIFICANDO DEPENDENCIAS...")
    if os.path.exists("docker/requirements.txt"):
        print("    requirements.txt encontrado")
        with open("docker/requirements.txt", "r") as f:
            print(f"   Dependencias: {len(f.readlines())} paquetes")
    else:
        print("    requirements.txt no encontrado")
        checks_passed = False
    
    # scripts/test_ci_locally.py (parte corregida)

    # 4. Verificar sintaxis Python
    print("\n4. VERIFICANDO SINTÁXIS...")
    python_files = ["app/api.py"]  # Solo verificar api_flask.py por ahora
    for file in python_files:
        if os.path.exists(file):
            try:
            # Usar encoding utf-8 explícitamente
                with open(file, "r", encoding="utf-8") as f:
                    compile(f.read(), file, 'exec')
                print(f"    {file} - Sintaxis correcta")
            except SyntaxError as e:
                print(f"    {file} - Error sintaxis: {e}")
                checks_passed = False
            except UnicodeDecodeError as e:
                print(f"     {file} - Problema de codificación: {e}")
            # Intentar con diferentes codificaciones
            try:
                with open(file, "r", encoding="latin-1") as f:
                    compile(f.read(), file, 'exec')
                print(f"    {file} - Sintaxis correcta (con latin-1)")
            except:
                print(f"    {file} - No se pudo leer el archivo")
                checks_passed = False
    # Resultado
    if checks_passed:
        print(" TODAS LAS VERIFICACIONES PASARON - Listo para CI/CD")
        print(" Ahora puedes hacer push a GitHub para ejecutar GitHub Actions")
    else:
        print(" ALGUNAS VERIFICACIONES FALLARON - Revisa los errores")
    
    return checks_passed

if __name__ == "__main__":
    success = run_ci_checks()
    sys.exit(0 if success else 1)