import os

# ============================================================
# CONFIGURACIÓN
# ============================================================
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))  # .../tp7-ml
REPORT = os.path.join(ROOT, "tp7B-cv.md")

# ============================================================
# FUNCIONES DE MÉTRICAS SEGÚN LA IMAGEN
# ============================================================

def accuracy(TP, TN, FP, FN):
    """Exactitud global del modelo"""
    return (TP + TN) / (TP + TN + FP + FN)

def precision(TP, FP):
    """Proporción de positivos predichos que fueron correctos"""
    return TP / (TP + FP) if (TP + FP) > 0 else 0

def sensitivity(TP, FN):
    """Sensibilidad o recall: proporción de positivos reales correctamente identificados"""
    return TP / (TP + FN) if (TP + FN) > 0 else 0

def specificity(TN, FP):
    """Especificidad: proporción de negativos reales correctamente identificados"""
    return TN / (TN + FP) if (TN + FP) > 0 else 0

# ============================================================
# BLOQUE PARA INCLUIR EN tp7B-cv.md
# ============================================================
md = []
md.append("# TP7B – Validación Cruzada y Métricas")
md.append("")
md.append("## 6. Cálculo de métricas a partir de la matriz de confusión")
md.append("")
md.append("Las siguientes funciones permiten calcular las métricas de evaluación de un modelo de clasificación según la matriz de confusión (TP, TN, FP, FN), siguiendo las fórmulas de la figura de referencia:")
md.append("")
md.append("```python")
md.append("def accuracy(TP, TN, FP, FN):")
md.append("    return (TP + TN) / (TP + TN + FP + FN)")
md.append("")
md.append("def precision(TP, FP):")
md.append("    return TP / (TP + FP) if (TP + FP) > 0 else 0")
md.append("")
md.append("def sensitivity(TP, FN):  # también llamada Recall")
md.append("    return TP / (TP + FN) if (TP + FN) > 0 else 0")
md.append("")
md.append("def specificity(TN, FP):")
md.append("    return TN / (TN + FP) if (TN + FP) > 0 else 0")
md.append("```")
md.append("")
md.append("Estas funciones se utilizan para evaluar los clasificadores generados en los ejercicios (4) y (5), aplicando directamente los valores de TP, TN, FP y FN obtenidos de sus respectivas matrices de confusión.")
md.append("")
md.append("---")
md.append("*Archivo generado automáticamente por metricas_confusion.py.*")

# Guardar el archivo Markdown
with open(REPORT, "w", encoding="utf-8") as f:
    f.write("\n".join(md))

print(f"✅ Archivo generado: {REPORT}")
