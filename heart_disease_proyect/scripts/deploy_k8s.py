# scripts/deploy_k8s.py
import subprocess
import time
import os

def run_cmd(command, desc):
    print(f" {desc}")
    print(f"   Comando: {command}")
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            print("    Éxito")
            if result.stdout:
                print(f"   Salida: {result.stdout.strip()}")
            return True
        else:
            print(f"    Error: {result.stderr}")
            return False
    except Exception as e:
        print(f"    Excepción: {e}")
        return False


# 1. Verificar Kubernetes
print("1. Verificando Kubernetes...")
if not run_cmd("kubectl get nodes", "Estado de nodos"):
    print(" Kubernetes no está listo")
    exit(1)

# 2. Aplicar configuración
print("\n2. Desplegando aplicación...")
if not run_cmd("kubectl apply -f k8s/", "Aplicando recursos Kubernetes"):
    exit(1)

# 3. Esperar
print("\n3. Esperando a que los pods estén listos...")
time.sleep(20)

# 4. Verificar estado
print("\n4. Verificando despliegue...")
run_cmd("kubectl get deployments", "Deployments")
run_cmd("kubectl get services", "Services") 
run_cmd("kubectl get pods", "Pods")

print(" Comandos útiles:")
print("   kubectl logs -f deployment/heart-model-deployment")
print("   kubectl get all")
print("   minikube service heart-service --url  (si usas Minikube)")