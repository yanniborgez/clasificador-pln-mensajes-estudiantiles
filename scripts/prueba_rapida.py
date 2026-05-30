import os
import sys

raiz = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if raiz not in sys.path:
    sys.path.insert(0, raiz)

from src.modelo_pln import ClasificadorPLN

modelo = ClasificadorPLN()
resultado = modelo.analizar_texto("No puedo entrar a la plataforma y necesito entregar mi tarea hoy")
print(resultado["intencion"])
print(resultado["sentimiento"])
print(resultado["prioridad"])
print(resultado["accion_recomendada"])
