import csv
from student_agents.basic_agent import YourNameAgent
import pandas as pd
import time


# === CONFIGURACIÓN ===
SIZES = [2, 4]
DIRT_RATES = [0.1, 0.2, 0.4, 0.8]
REPEATS = 10
CSV_PATH = "results.csv"

def run_and_evaluate(size, dirt_rate):
    agent = YourNameAgent()
    if not agent.connect_to_environment(size, size, dirt_rate=dirt_rate):
        print(f"❌ Error al conectar con el entorno ({size}x{size}, dirt={dirt_rate})")
        return None

    performance = agent.run_simulation(verbose=False)
    stats = agent.get_statistics()
    agent.disconnect()

    cleaned = stats.get("successful_sucks", 0)
    actions = stats.get("total_actions", 0)
    total_dirt = stats.get("total_dirt_available", 0)

    print(f"✅ size={size}, dirt={dirt_rate} → cleaned={cleaned}, actions={actions}, perf={performance}")

    return {
        "Tamaño (N×N)": size,
        "Suciedad (%)": dirt_rate,
        "Celdas limpiadas": cleaned,
        "Acciones totales": actions,
        "Suciedad inicial": total_dirt,
        "Rendimiento final": performance
    }

def main():
    rows = []

    for size in SIZES:
        for dirt_rate in DIRT_RATES:
            for i in range(REPEATS):
                try:
                    result = run_and_evaluate(size, dirt_rate)
                    time.sleep(0.5)  # Pequeña pausa para evitar sobrecargar el servidor
                    if result:
                        rows.append(result)
                except Exception as e:
                    print(f"❌ Error en ejecución (size={size}, dirt={dirt_rate}, intento={i+1}): {e}")

    if rows:
        # Usamos ";" para compatibilidad con configuración regional de Excel
        with open(CSV_PATH, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=rows[0].keys(), delimiter=";")
            writer.writeheader()
            writer.writerows(rows)

        print("\n✅ Simulaciones completadas correctamente.")
        print(f"📄 Resultados guardados en: {CSV_PATH}")
    else:
        print("\n⚠️ No se generaron resultados (verificar conexión con servidor o ejecución del agente).")


def generar_resumen(csv_path="results.csv", output_path="summary.csv"):
    """
    Genera un resumen agrupado con promedios de las métricas principales.
    """
    df = pd.read_csv(csv_path, delimiter=";")
    resumen = (
        df.groupby(["Tamaño (N×N)", "Suciedad (%)"])
        .agg({
            "Suciedad inicial": "mean",
            "Celdas limpiadas": "mean",
            "Acciones totales": "mean",
            "Rendimiento final": "mean"
        })
        .reset_index()
    )

    # Renombrar columnas para claridad
    resumen.columns = [
        "Tamaño (N×N)",
        "Suciedad (%)",
        "Promedio celdas limpiadas",
        "Promedio acciones",
        "Suciedad inicial",
        "Promedio rendimiento"
    ]

    resumen.to_csv(output_path, sep=";", index=False)
    print(f"\n📈 Resumen guardado en: {output_path}")
    print(resumen.head(10))

# Al final del archivo:
if __name__ == "__main__":
    main()
    generar_resumen()

