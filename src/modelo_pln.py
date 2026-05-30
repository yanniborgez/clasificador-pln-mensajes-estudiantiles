from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import accuracy_score, f1_score
from sklearn.naive_bayes import ComplementNB
from sklearn.pipeline import Pipeline, FeatureUnion
from .datos_entrenamiento import DATOS_ENTRENAMIENTO
from .procesamiento_texto import preparar_para_modelo, extraer_estadisticas, tokenizar, normalizar_texto


class ClasificadorPLN:
    def __init__(self):
        self.textos = [fila["texto"] for fila in DATOS_ENTRENAMIENTO]
        self.intenciones = [fila["intencion"] for fila in DATOS_ENTRENAMIENTO]
        self.sentimientos = [fila["sentimiento"] for fila in DATOS_ENTRENAMIENTO]
        self.claves_intencion = {
            "apoyo_academico": {"actividad", "tarea", "asesoria", "tutoria", "proyecto", "reporte", "regresion", "clase", "dudas", "explicar", "retroalimentacion", "examen", "machine", "modelo"},
            "tramite_administrativo": {"constancia", "calificacion", "reinscripcion", "inscripcion", "control", "escolar", "datos", "horario", "historial", "comprobante", "pago", "tramitar", "validar"},
            "bienestar_estudiantil": {"estresado", "estres", "ansiedad", "dormir", "agotado", "concentrarme", "psicologico", "mental", "familiares", "motivacion", "bienestar", "salud", "orientacion"},
            "problema_tecnico": {"plataforma", "sistema", "error", "enlace", "videollamada", "archivo", "instalar", "python", "computadora", "contrasena", "usuario", "aula", "virtual", "subir", "descargar", "entrar", "cargar", "abrir", "acceso"},
            "felicitacion": {"excelente", "agradezco", "clara", "claro", "organizado", "amable", "rapida", "profesional", "gusto", "resolvio", "util", "reconozco", "bien"},
            "queja_servicio": {"lento", "molesta", "confusa", "insatisfecho", "tardaron", "cerrada", "coincide", "desorganizacion", "retraso", "retraso", "afecto", "nadie", "servicio"},
            "consulta_general": {"quisiera", "donde", "saber", "confirmar", "formato", "salon", "pregunta", "duracion", "liga", "quien", "fecha", "calendario", "proxima"}
        }
        self.claves_sentimiento = {
            "positivo": {"excelente", "agradezco", "claro", "clara", "amable", "rapida", "profesional", "gusto", "util", "bien", "correctamente", "aprendimos", "ayudo"},
            "negativo": {"no", "nunca", "error", "lento", "molesta", "confusa", "estresado", "ansiedad", "agotado", "tardaron", "reprobe", "problemas", "retraso", "cerrada", "mal", "perdiendo", "no puedo", "no carga", "no aparece", "nadie responde"}
        }
        self.modelo_intencion = self.crear_modelo()
        self.modelo_sentimiento = self.crear_modelo()
        self.modelo_intencion.fit(self.textos, self.intenciones)
        self.modelo_sentimiento.fit(self.textos, self.sentimientos)

    def crear_modelo(self):
        return Pipeline([
            ("vectorizador", FeatureUnion([
                ("palabras", TfidfVectorizer(preprocessor=preparar_para_modelo, ngram_range=(1, 2), min_df=1, sublinear_tf=True)),
                ("caracteres", TfidfVectorizer(preprocessor=preparar_para_modelo, analyzer="char_wb", ngram_range=(3, 5), min_df=1, sublinear_tf=True))
            ])),
            ("clasificador", ComplementNB(alpha=0.35))
        ])

    def obtener_confianza(self, modelo, texto, etiqueta):
        probabilidades = modelo.predict_proba([texto])[0]
        clases = list(modelo.classes_)
        return float(probabilidades[clases.index(etiqueta)])

    def clasificar_por_claves(self, texto, catalogo):
        tokens = set(tokenizar(texto))
        texto_normalizado = normalizar_texto(texto)
        puntajes = {}
        for etiqueta, claves in catalogo.items():
            puntaje = 0
            for clave in claves:
                clave_normalizada = normalizar_texto(clave)
                if " " in clave_normalizada and clave_normalizada in texto_normalizado:
                    puntaje += 2
                elif clave_normalizada in tokens:
                    puntaje += 1
            puntajes[etiqueta] = puntaje
        etiqueta = max(puntajes, key=puntajes.get)
        puntaje = puntajes[etiqueta]
        if puntaje == 0:
            return None, 0
        return etiqueta, puntaje

    def elegir_intencion(self, texto):
        intencion_modelo = self.modelo_intencion.predict([texto])[0]
        confianza_modelo = self.obtener_confianza(self.modelo_intencion, texto, intencion_modelo)
        intencion_claves, puntaje = self.clasificar_por_claves(texto, self.claves_intencion)
        if intencion_claves and (puntaje >= 2 or confianza_modelo < 0.62):
            confianza = min(0.96, max(confianza_modelo, 0.56 + puntaje * 0.10))
            return intencion_claves, confianza
        return intencion_modelo, confianza_modelo

    def elegir_sentimiento(self, texto):
        sentimiento_modelo = self.modelo_sentimiento.predict([texto])[0]
        confianza_modelo = self.obtener_confianza(self.modelo_sentimiento, texto, sentimiento_modelo)
        sentimiento_claves, puntaje = self.clasificar_por_claves(texto, self.claves_sentimiento)
        if sentimiento_claves and (puntaje >= 1 or confianza_modelo < 0.65):
            confianza = min(0.95, max(confianza_modelo, 0.60 + puntaje * 0.12))
            return sentimiento_claves, confianza
        return sentimiento_modelo, confianza_modelo

    def calcular_prioridad(self, texto, intencion, sentimiento):
        tokens = set(tokenizar(texto))
        claves_urgentes = {"urgente", "reprobe", "ansiedad", "estresado", "agotado", "perdiendo", "afecto", "error", "cerrado", "cerrada", "tarde", "retraso", "hoy"}
        claves_criticas = {"bienestar_estudiantil", "problema_tecnico", "queja_servicio"}
        coincidencias = tokens.intersection(claves_urgentes)
        if intencion == "bienestar_estudiantil" and sentimiento == "negativo":
            return "alta"
        if coincidencias and (sentimiento == "negativo" or intencion in claves_criticas):
            return "alta"
        if sentimiento == "negativo" or intencion in {"tramite_administrativo", "problema_tecnico", "apoyo_academico"}:
            return "media"
        return "baja"

    def recomendar_accion(self, intencion, sentimiento, prioridad):
        acciones = {
            "apoyo_academico": "Canalizar a asesoría académica o revisión de dudas.",
            "tramite_administrativo": "Enviar a control escolar o mesa administrativa.",
            "bienestar_estudiantil": "Sugerir contacto de bienestar y atención humana prioritaria.",
            "problema_tecnico": "Levantar ticket de soporte técnico con evidencia del error.",
            "felicitacion": "Registrar como retroalimentación positiva.",
            "queja_servicio": "Revisar el caso, responder formalmente y documentar seguimiento.",
            "consulta_general": "Responder con información puntual o enlace institucional."
        }
        accion = acciones.get(intencion, "Revisar manualmente el mensaje.")
        if prioridad == "alta":
            return "Atención prioritaria. " + accion
        if sentimiento == "negativo":
            return "Atención de seguimiento. " + accion
        return accion

    def obtener_palabras_relevantes(self, texto, intencion):
        vectorizador = self.modelo_intencion.named_steps["vectorizador"]
        clasificador = self.modelo_intencion.named_steps["clasificador"]
        matriz = vectorizador.transform([texto])
        clases = list(clasificador.classes_)
        indice_clase = clases.index(intencion)
        coeficientes = clasificador.feature_log_prob_[indice_clase]
        nombres = vectorizador.get_feature_names_out()
        valores = matriz.toarray()[0]
        aportes = []
        for indice, valor in enumerate(valores):
            if valor > 0:
                aportes.append((nombres[indice], valor * coeficientes[indice]))
        aportes.sort(key=lambda elemento: elemento[1], reverse=True)
        palabras = [palabra.replace("palabras__", "") for palabra, valor in aportes if valor > 0 and palabra.startswith("palabras__")]
        if palabras:
            return palabras[:6]
        return tokenizar(texto)[:6]

    def analizar_texto(self, texto):
        texto = str(texto).strip()
        if not texto:
            raise ValueError("El texto está vacío.")
        intencion, confianza_intencion = self.elegir_intencion(texto)
        sentimiento, confianza_sentimiento = self.elegir_sentimiento(texto)
        prioridad = self.calcular_prioridad(texto, intencion, sentimiento)
        estadisticas = extraer_estadisticas(texto)
        return {
            "texto": texto,
            "texto_normalizado": estadisticas["texto_normalizado"],
            "tokens": estadisticas["tokens"],
            "total_palabras": estadisticas["total_palabras"],
            "palabras_unicas": estadisticas["palabras_unicas"],
            "intencion": intencion,
            "sentimiento": sentimiento,
            "prioridad": prioridad,
            "confianza_intencion": round(confianza_intencion, 4),
            "confianza_sentimiento": round(confianza_sentimiento, 4),
            "palabras_relevantes": self.obtener_palabras_relevantes(texto, intencion),
            "accion_recomendada": self.recomendar_accion(intencion, sentimiento, prioridad)
        }

    def analizar_lote(self, textos):
        resultados = []
        for texto in textos:
            texto = str(texto).strip()
            if texto:
                resultados.append(self.analizar_texto(texto))
        return resultados

    def evaluar_modelo(self):
        predicciones_intencion = [self.analizar_texto(texto)["intencion"] for texto in self.textos]
        predicciones_sentimiento = [self.analizar_texto(texto)["sentimiento"] for texto in self.textos]
        return {
            "registros_entrenamiento": len(self.textos),
            "clases_intencion": sorted(set(self.intenciones)),
            "clases_sentimiento": sorted(set(self.sentimientos)),
            "accuracy_intencion": round(float(accuracy_score(self.intenciones, predicciones_intencion)), 4),
            "f1_intencion": round(float(f1_score(self.intenciones, predicciones_intencion, average="macro")), 4),
            "accuracy_sentimiento": round(float(accuracy_score(self.sentimientos, predicciones_sentimiento)), 4),
            "f1_sentimiento": round(float(f1_score(self.sentimientos, predicciones_sentimiento, average="macro")), 4),
            "pliegues_intencion": "validación funcional interna",
            "pliegues_sentimiento": "validación funcional interna"
        }
