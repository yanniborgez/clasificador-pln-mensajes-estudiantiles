import re
import unicodedata
from collections import Counter

PALABRAS_VACIAS = {
    "a", "al", "algo", "ante", "antes", "como", "con", "contra", "cual", "cuando",
    "de", "del", "desde", "donde", "durante", "e", "el", "ella", "ellas", "ellos",
    "en", "entre", "era", "eran", "eres", "es", "esa", "esas", "ese", "eso", "esos",
    "esta", "estaba", "estado", "estan", "estar", "este", "esto", "estos", "fue", "ha",
    "han", "hasta", "hay", "la", "las", "le", "les", "lo", "los", "mas", "me", "mi",
    "mis", "muy", "no", "nos", "o", "para", "pero", "por", "porque", "que", "se", "si",
    "sin", "sobre", "su", "sus", "tambien", "te", "tiene", "tienen", "tu", "un", "una",
    "uno", "unos", "y", "ya", "yo"
}


def quitar_acentos(texto):
    texto_normalizado = unicodedata.normalize("NFD", texto)
    return "".join(caracter for caracter in texto_normalizado if unicodedata.category(caracter) != "Mn")


def normalizar_texto(texto):
    texto = str(texto).lower().strip()
    texto = quitar_acentos(texto)
    texto = re.sub(r"https?://\S+|www\.\S+", " ", texto)
    texto = re.sub(r"\b[\w\.-]+@[\w\.-]+\.\w+\b", " ", texto)
    texto = re.sub(r"[^a-záéíóúüñ0-9\s]", " ", texto)
    texto = re.sub(r"\s+", " ", texto).strip()
    return texto


def tokenizar(texto):
    texto = normalizar_texto(texto)
    tokens = [palabra for palabra in texto.split() if palabra not in PALABRAS_VACIAS and len(palabra) > 1]
    return tokens


def preparar_para_modelo(texto):
    return " ".join(tokenizar(texto))


def extraer_estadisticas(texto):
    tokens = tokenizar(texto)
    frecuencia = Counter(tokens)
    return {
        "texto_normalizado": normalizar_texto(texto),
        "tokens": tokens,
        "total_palabras": len(tokens),
        "palabras_unicas": len(set(tokens)),
        "total_caracteres": len(str(texto)),
        "palabras_frecuentes": frecuencia.most_common(8)
    }
