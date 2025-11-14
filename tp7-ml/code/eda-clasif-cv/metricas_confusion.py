import os

# ============================================================
# TP7B – Funciones de Métricas (Accuracy, Precision, Recall, Specificity)
# ============================================================

def accuracy(TP, TN, FP, FN):
    """
    Accuracy (Exactitud):
    Proporción total de predicciones correctas sobre el total de muestras.
    """
    total = TP + TN + FP + FN
    return (TP + TN) / total if total > 0 else 0


def precision(TP, FP):
    """
    Precision:
    De los elementos clasificados como positivos, cuántos fueron realmente positivos.
    """
    denom = TP + FP
    return TP / denom if denom > 0 else 0


def sensitivity(TP, FN):
    """
    Sensitivity / Recall:
    Proporción de positivos reales correctamente identificados.
    """
    denom = TP + FN
    return TP / denom if denom > 0 else 0


def specificity(TN, FP):
    """
    Specificity:
    Proporción de negativos reales correctamente identificados.
    """
    denom = TN + FP
    return TN / denom if denom > 0 else 0


# ============================================================
# Función para generar el bloque del reporte tp7B-cv.md
# ============================================================

def generar_bloque_metricas_md():
    """
    Devuelve el contenido en formato Markdown con:
    - Fórmulas
    - Explicación conceptual
    - Implementación en Python
    Para incluirlo dentro del archivo tp7B-cv.md.
    """

    md = []
    md.append("## 6. Métricas de evaluación basadas en la matriz de confusión")
    md.append("")
    md.append(
        "A partir de los valores TP (True Positive), TN (True Negative), FP (False Positive) "
        "y FN (False Negative), se calculan las siguientes métricas utilizadas en el TP:"
    )
    md.append("")
    md.append("### Fórmulas")
    md.append("")
    md.append("- **Accuracy** = (TP + TN) / (TP + TN + FP + FN)")
    md.append("- **Precision** = TP / (TP + FP)")
    md.append("- **Sensitivity / Recall** = TP / (TP + FN)")
    md.append("- **Specificity** = TN / (TN + FP)")
    md.append("")
    md.append("### Implementación en Python")
    md.append("```python")
    md.append("def accuracy(TP, TN, FP, FN):")
    md.append("    return (TP + TN) / (TP + TN + FP + FN)")
    md.append("")
    md.append("def precision(TP, FP):")
    md.append("    return TP / (TP + FP) if (TP + FP) > 0 else 0")
    md.append("")
    md.append("def sensitivity(TP, FN):  # Recall")
    md.append("    return TP / (TP + FN) if (TP + FN) > 0 else 0")
    md.append("")
    md.append("def specificity(TN, FP):")
    md.append("    return TN / (TN + FP) if (TN + FP) > 0 else 0")
    md.append("```")
    md.append("")
    md.append(
        "Estas funciones se aplicaron a las matrices de confusión obtenidas para los clasificadores "
        "implementados en los ejercicios 4 (aleatorio) y 5 (clase mayoritaria)."
    )
    md.append("")
    md.append("---")

    return md


# ============================================================
# Escritura del archivo tp7B-cv.md
# (Se agrega al final, NO sobrescribe todo el archivo)
# ============================================================

if __name__ == "__main__":
    ROOT = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))  # /tp7-ml
    REPORT = os.path.join(ROOT, "tp7B-cv.md")

    print(f"📄 Actualizando archivo: {REPORT}")

    try:
        # Si el archivo no existe, se crea.
        if not os.path.exists(REPORT):
            open(REPORT, "w", encoding="utf-8").close()

        # Leer contenido existente
        with open(REPORT, "r", encoding="utf-8") as f:
            original = f.read().strip()

        # Generar bloque de métricas
        bloque = generar_bloque_metricas_md()
        bloque_texto = "\n".join(bloque)

        # Unir con el contenido existente
        nuevo_contenido = original + "\n\n" + bloque_texto

        # Guardar
        with open(REPORT, "w", encoding="utf-8") as f:
            f.write(nuevo_contenido)

        print("✅ Métricas agregadas correctamente a tp7B-cv.md")

    except Exception as e:
        print(f"❌ Error al generar el archivo: {e}")
