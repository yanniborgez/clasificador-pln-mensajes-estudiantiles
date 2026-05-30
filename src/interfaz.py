import csv
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from .modelo_pln import ClasificadorPLN


class AplicacionPLN:
    def __init__(self, ventana):
        self.ventana = ventana
        self.ventana.title("Clasificador PLN de mensajes estudiantiles")
        self.ventana.geometry("1120x720")
        self.ventana.minsize(980, 650)
        self.modelo = ClasificadorPLN()
        self.resultados_lote = []
        self.configurar_estilo()
        self.crear_interfaz()

    def configurar_estilo(self):
        self.estilo = ttk.Style()
        self.estilo.theme_use("clam")
        self.estilo.configure("TFrame", background="#f5f5f5")
        self.estilo.configure("TLabelframe", background="#f5f5f5")
        self.estilo.configure("TLabelframe.Label", background="#f5f5f5", font=("Segoe UI", 10, "bold"))
        self.estilo.configure("TLabel", background="#f5f5f5", font=("Segoe UI", 10))
        self.estilo.configure("TButton", font=("Segoe UI", 10), padding=6)
        self.estilo.configure("Treeview", font=("Segoe UI", 9), rowheight=24)
        self.estilo.configure("Treeview.Heading", font=("Segoe UI", 9, "bold"))

    def crear_interfaz(self):
        contenedor = ttk.Frame(self.ventana, padding=14)
        contenedor.pack(fill="both", expand=True)
        encabezado = ttk.Label(contenedor, text="Sistema de PLN para clasificación y priorización de mensajes estudiantiles", font=("Segoe UI", 15, "bold"))
        encabezado.pack(anchor="w", pady=(0, 8))
        descripcion = ttk.Label(contenedor, text="El sistema aplica limpieza textual, TF-IDF y regresión logística para identificar intención, sentimiento y prioridad de atención.")
        descripcion.pack(anchor="w", pady=(0, 12))
        self.pestanas = ttk.Notebook(contenedor)
        self.pestanas.pack(fill="both", expand=True)
        self.crear_pestana_individual()
        self.crear_pestana_lote()
        self.crear_pestana_evaluacion()
        self.crear_pestana_ayuda()

    def crear_pestana_individual(self):
        marco = ttk.Frame(self.pestanas, padding=12)
        self.pestanas.add(marco, text="Análisis individual")
        panel_entrada = ttk.LabelFrame(marco, text="Mensaje a analizar", padding=10)
        panel_entrada.pack(fill="x")
        self.caja_texto = tk.Text(panel_entrada, height=7, wrap="word", font=("Segoe UI", 10))
        self.caja_texto.pack(fill="x", expand=True)
        self.caja_texto.insert("1.0", "No puedo subir mi tarea a la plataforma y necesito ayuda urgente antes del cierre.")
        botones = ttk.Frame(marco)
        botones.pack(fill="x", pady=10)
        ttk.Button(botones, text="Analizar texto", command=self.analizar_texto).pack(side="left", padx=(0, 8))
        ttk.Button(botones, text="Limpiar", command=self.limpiar_individual).pack(side="left")
        panel_resultado = ttk.LabelFrame(marco, text="Resultado del modelo", padding=10)
        panel_resultado.pack(fill="both", expand=True)
        self.salida_resultado = tk.Text(panel_resultado, height=18, wrap="word", font=("Consolas", 10), state="disabled")
        self.salida_resultado.pack(fill="both", expand=True)

    def crear_pestana_lote(self):
        marco = ttk.Frame(self.pestanas, padding=12)
        self.pestanas.add(marco, text="Análisis por archivo")
        acciones = ttk.Frame(marco)
        acciones.pack(fill="x", pady=(0, 10))
        ttk.Button(acciones, text="Cargar TXT o CSV", command=self.cargar_archivo).pack(side="left", padx=(0, 8))
        ttk.Button(acciones, text="Guardar resultados CSV", command=self.guardar_resultados).pack(side="left", padx=(0, 8))
        ttk.Button(acciones, text="Borrar tabla", command=self.borrar_tabla).pack(side="left")
        columnas = ("texto", "intencion", "sentimiento", "prioridad", "confianza", "accion")
        self.tabla = ttk.Treeview(marco, columns=columnas, show="headings")
        encabezados = {
            "texto": "Texto",
            "intencion": "Intención",
            "sentimiento": "Sentimiento",
            "prioridad": "Prioridad",
            "confianza": "Confianza",
            "accion": "Acción recomendada"
        }
        anchos = {"texto": 310, "intencion": 140, "sentimiento": 105, "prioridad": 90, "confianza": 90, "accion": 320}
        for columna in columnas:
            self.tabla.heading(columna, text=encabezados[columna])
            self.tabla.column(columna, width=anchos[columna], anchor="w")
        barra_y = ttk.Scrollbar(marco, orient="vertical", command=self.tabla.yview)
        barra_x = ttk.Scrollbar(marco, orient="horizontal", command=self.tabla.xview)
        self.tabla.configure(yscrollcommand=barra_y.set, xscrollcommand=barra_x.set)
        self.tabla.pack(side="left", fill="both", expand=True)
        barra_y.pack(side="right", fill="y")
        barra_x.pack(side="bottom", fill="x")

    def crear_pestana_evaluacion(self):
        marco = ttk.Frame(self.pestanas, padding=12)
        self.pestanas.add(marco, text="Evaluación")
        ttk.Button(marco, text="Calcular evaluación", command=self.mostrar_evaluacion).pack(anchor="w", pady=(0, 10))
        self.salida_evaluacion = tk.Text(marco, height=24, wrap="word", font=("Consolas", 10), state="disabled")
        self.salida_evaluacion.pack(fill="both", expand=True)
        self.mostrar_evaluacion()

    def crear_pestana_ayuda(self):
        marco = ttk.Frame(self.pestanas, padding=12)
        self.pestanas.add(marco, text="Ayuda")
        texto = tk.Text(marco, wrap="word", font=("Segoe UI", 10), state="normal")
        texto.pack(fill="both", expand=True)
        contenido = (
            "Uso recomendado:\n\n"
            "1. Escribir o pegar un mensaje estudiantil en la pestaña de análisis individual.\n"
            "2. Presionar Analizar texto para obtener intención, sentimiento, prioridad y acción sugerida.\n"
            "3. Para análisis masivo, cargar un archivo TXT con un mensaje por línea o un CSV con columna texto.\n"
            "4. Guardar resultados en CSV para documentar la evidencia del procesamiento.\n\n"
            "Categorías de intención:\n"
            "apoyo_academico, tramite_administrativo, bienestar_estudiantil, problema_tecnico, felicitacion, queja_servicio y consulta_general.\n\n"
            "El sistema es un prototipo funcional. Sus resultados deben usarse como apoyo inicial y no como decisión automática definitiva."
        )
        texto.insert("1.0", contenido)
        texto.configure(state="disabled")

    def escribir_salida(self, caja, contenido):
        caja.configure(state="normal")
        caja.delete("1.0", "end")
        caja.insert("1.0", contenido)
        caja.configure(state="disabled")

    def analizar_texto(self):
        texto = self.caja_texto.get("1.0", "end").strip()
        try:
            resultado = self.modelo.analizar_texto(texto)
        except Exception as error:
            messagebox.showerror("No se pudo analizar", str(error))
            return
        contenido = self.formatear_resultado(resultado)
        self.escribir_salida(self.salida_resultado, contenido)

    def formatear_resultado(self, resultado):
        return (
            f"Intención detectada: {resultado['intencion']}\n"
            f"Confianza de intención: {resultado['confianza_intencion']:.2%}\n"
            f"Sentimiento detectado: {resultado['sentimiento']}\n"
            f"Confianza de sentimiento: {resultado['confianza_sentimiento']:.2%}\n"
            f"Prioridad sugerida: {resultado['prioridad']}\n\n"
            f"Acción recomendada:\n{resultado['accion_recomendada']}\n\n"
            f"Texto normalizado:\n{resultado['texto_normalizado']}\n\n"
            f"Tokens útiles:\n{', '.join(resultado['tokens'])}\n\n"
            f"Palabras relevantes para la decisión:\n{', '.join(resultado['palabras_relevantes'])}\n\n"
            f"Total de palabras útiles: {resultado['total_palabras']}\n"
            f"Palabras únicas: {resultado['palabras_unicas']}"
        )

    def limpiar_individual(self):
        self.caja_texto.delete("1.0", "end")
        self.escribir_salida(self.salida_resultado, "")

    def cargar_archivo(self):
        ruta = filedialog.askopenfilename(filetypes=[("Archivos de texto o CSV", "*.txt *.csv"), ("Todos los archivos", "*.*")])
        if not ruta:
            return
        try:
            textos = self.leer_textos(ruta)
            self.resultados_lote = self.modelo.analizar_lote(textos)
            self.actualizar_tabla()
            messagebox.showinfo("Análisis terminado", f"Se analizaron {len(self.resultados_lote)} mensajes.")
        except Exception as error:
            messagebox.showerror("Error al cargar", str(error))

    def leer_textos(self, ruta):
        if ruta.lower().endswith(".csv"):
            with open(ruta, "r", encoding="utf-8-sig", newline="") as archivo:
                lector = csv.DictReader(archivo)
                if lector.fieldnames and "texto" in lector.fieldnames:
                    return [fila.get("texto", "") for fila in lector]
            with open(ruta, "r", encoding="utf-8-sig", newline="") as archivo:
                lector_simple = csv.reader(archivo)
                return [fila[0] for fila in lector_simple if fila]
        with open(ruta, "r", encoding="utf-8") as archivo:
            return [linea.strip() for linea in archivo if linea.strip()]

    def actualizar_tabla(self):
        self.borrar_tabla()
        for resultado in self.resultados_lote:
            confianza = f"{resultado['confianza_intencion']:.2%}"
            texto = resultado["texto"][:95] + ("..." if len(resultado["texto"]) > 95 else "")
            self.tabla.insert("", "end", values=(texto, resultado["intencion"], resultado["sentimiento"], resultado["prioridad"], confianza, resultado["accion_recomendada"]))

    def guardar_resultados(self):
        if not self.resultados_lote:
            messagebox.showwarning("Sin resultados", "Primero carga y analiza un archivo.")
            return
        ruta = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV", "*.csv")])
        if not ruta:
            return
        campos = ["texto", "intencion", "sentimiento", "prioridad", "confianza_intencion", "confianza_sentimiento", "accion_recomendada"]
        with open(ruta, "w", encoding="utf-8-sig", newline="") as archivo:
            escritor = csv.DictWriter(archivo, fieldnames=campos)
            escritor.writeheader()
            for resultado in self.resultados_lote:
                escritor.writerow({campo: resultado[campo] for campo in campos})
        messagebox.showinfo("Archivo guardado", "Los resultados se guardaron correctamente.")

    def borrar_tabla(self):
        for elemento in self.tabla.get_children():
            self.tabla.delete(elemento)

    def mostrar_evaluacion(self):
        metricas = self.modelo.evaluar_modelo()
        contenido = (
            "Evaluación interna del prototipo\n\n"
            f"Registros de entrenamiento: {metricas['registros_entrenamiento']}\n"
            f"Clases de intención: {', '.join(metricas['clases_intencion'])}\n"
            f"Clases de sentimiento: {', '.join(metricas['clases_sentimiento'])}\n\n"
            "Clasificación de intención con validación funcional interna\n"
            f"Accuracy interna: {metricas['accuracy_intencion']:.2%}\n"
            f"F1 macro interno: {metricas['f1_intencion']:.2%}\n\n"
            "Clasificación de sentimiento con validación funcional interna\n"
            f"Accuracy interna: {metricas['accuracy_sentimiento']:.2%}\n"
            f"F1 macro interno: {metricas['f1_sentimiento']:.2%}\n\n"
            "Interpretación:\n"
            "La validación funcional interna verifica que el prototipo procese correctamente los ejemplos incluidos. "
            "El F1 macro es relevante porque compara el rendimiento entre clases sin favorecer únicamente a la clase mayoritaria. "
            "En una implementación real, el conjunto de entrenamiento debe ampliarse con mensajes reales anonimizados y validación externa."
        )
        self.escribir_salida(self.salida_evaluacion, contenido)


def iniciar_aplicacion():
    ventana = tk.Tk()
    AplicacionPLN(ventana)
    ventana.mainloop()
