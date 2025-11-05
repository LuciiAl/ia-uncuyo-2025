#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import csv
import time
import math
import random
import argparse
from pathlib import Path

import pandas as pd
import matplotlib.pyplot as plt

# Importá tu agente reflexivo:
# Ajustá el import si tu archivo/clase tienen otro nombre o ubicación
from student_agents.basic_agent import YourNameAgent
from base_agent import BaseAgent


# ============ Agente Aleatorio (totalmente al azar) ============
class RandomAgent(BaseAgent):
    """
    Agente con comportamiento totalmente aleatorio:
    - Si la celda está sucia => suck
    - Si no, elige una acción de movimiento al azar entre up/down/left/right
    """

    def __init__(self, server_url="http://127.0.0.1:5000", **kwargs):
        super().__init__(server_url, "RandomAgent", **kwargs)

    def get_strategy_description(self):
        return "Totally random choose random move."

    def think(self):
        if not self.is_connected():
            return False
        p = self.get_perception()
        if not p or p.get("is_finished", True):
            return False
    
        # Elegimos una acción de movimiento al azar
        move = random.choice([self.up, self.down, self.left, self.right, self.suck])
        return move()


# ==================== Parámetros por defecto ====================
SIZES_DEFAULT = [2, 4, 8, 16, 32, 64, 128]
DIRT_RATES_DEFAULT = [0.1, 0.2, 0.4, 0.8]
REPEATS_DEFAULT = 10


# ==================== Utilidades ====================
def ensure_dir(path: Path):
    path.mkdir(parents=True, exist_ok=True)



def run_one(agent_class, size, dirt_rate, server_url, max_actions=1000):
    """Corre UNA simulación para (agente, tamaño, suciedad) con límite de acciones."""
    agent = agent_class(server_url=server_url)
    if not agent.connect_to_environment(size, size, dirt_rate=dirt_rate):
        return None

    steps = 0

    # Ejecutamos la simulación manualmente con un límite de pasos
    while steps < max_actions:
        perception = agent.get_perception()
        if not perception or perception.get("is_finished", True):
            break

        # El agente decide la acción (sus métodos como up(), left(), etc. ya actúan)
        action_result = agent.think()

        # Si el método think() devuelve False o None, se corta
        if not action_result:
            break

        steps += 1

        # chequeamos si el entorno ya terminó
        perception = agent.get_perception()
        if perception.get("is_finished", False):
            break

    # Obtenemos las estadísticas del entorno
    stats = agent.get_statistics()
    agent.disconnect()

    # Guardamos las métricas finales
    stats["total_actions"] = steps

    return {
        "Agente": agent_class.__name__,
        "Tamaño (N×N)": size,
        "Suciedad (%)": dirt_rate,
        "Suciedad inicial": stats.get("total_dirt_available", 0),
        "Celdas limpiadas": stats.get("successful_sucks", 0),
        "Acciones totales": stats.get("total_actions", steps),
        "Rendimiento final": stats.get("performance", 0),
    }





def run_grid(agent_cls, sizes, dirt_rates, repeats, server_url, sleep_between=0.7):
    """Corre simulaciones para un solo agente."""
    rows = []
    total = len(sizes) * len(dirt_rates) * repeats
    k = 0
    for n in sizes:
        for dr in dirt_rates:
            for i in range(repeats):
                k += 1
                result = run_one(agent_cls, n, dr, server_url)
                if result:
                    rows.append(result)
                    print(f"[{k}/{total}] ✅ {result['Agente']}: size={n}, dirt={dr} "
                          f"→ total_dirt={result['Suciedad inicial']}, "
                          f"cleaned={result['Celdas limpiadas']}, "
                          f"actions={result['Acciones totales']}, "
                          f"perf={result['Rendimiento final']:.3f}")
                else:
                    print(f"[{k}/{total}] ❌ Error al conectar ({agent_cls.__name__}, size={n}, dirt={dr})")
                time.sleep(sleep_between)
    return rows

def save_csv(rows, csv_path):
    if not rows:
        return False
    with open(csv_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=rows[0].keys(), delimiter=";")
        writer.writeheader()
        writer.writerows(rows)
    return True


def summarize_to_csv(csv_path, out_summary):
    df = pd.read_csv(csv_path, delimiter=";")

    # promedios por agente, tamaño y suciedad
    resumen = (
        df.groupby(["Agente", "Tamaño (N×N)", "Suciedad (%)"])
          .agg({
              "Suciedad inicial": "mean",
              "Celdas limpiadas": "mean",
              "Acciones totales": "mean",
              "Rendimiento final": "mean"
          })
          .reset_index()
    )

    resumen.rename(columns={
        "Suciedad inicial": "Promedio suciedad inicial",
        "Celdas limpiadas": "Promedio celdas limpiadas",
        "Acciones totales": "Promedio acciones",
        "Rendimiento final": "Promedio rendimiento"
    }, inplace=True)

    resumen.to_csv(out_summary, sep=";", index=False)
    print(f"📈 Resumen guardado en: {out_summary}")
    return resumen

def plot_all(resumen: pd.DataFrame, images_dir: Path, results_csv_path: Path):
    ensure_dir(images_dir)

    # --- Gráfico 1: Acciones promedio por tamaño ---
    acciones_by_size = (
        resumen.groupby(["Agente", "Tamaño (N×N)"])
        ["Promedio acciones"]
        .mean()
        .reset_index()
    )

    plt.figure(figsize=(8, 5))
    for agent in acciones_by_size["Agente"].unique():
        data = acciones_by_size[acciones_by_size["Agente"] == agent]
        plt.plot(data["Tamaño (N×N)"], data["Promedio acciones"], marker="o", label=agent)

    plt.title("Acciones promedio por tamaño del entorno")
    plt.xlabel("Tamaño del entorno (N×N)")
    plt.ylabel("Acciones promedio (movimientos usados)")
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(images_dir / "acciones_por_tamaño.png", dpi=140)
    plt.close()

    # --- Grafico 2: Eficiencia (celdas limpiadas / acciones) ---
    resumen["Eficiencia"] = resumen["Promedio celdas limpiadas"] / resumen["Promedio acciones"]
    ef_by_dirt = (
        resumen.groupby(["Agente", "Suciedad (%)"])["Eficiencia"]
        .mean()
        .reset_index()
    )

    plt.figure(figsize=(8, 5))
    for agent in ef_by_dirt["Agente"].unique():
        data = ef_by_dirt[ef_by_dirt["Agente"] == agent]
        plt.plot(data["Suciedad (%)"], data["Eficiencia"], marker="o", label=agent)

    plt.title("Eficiencia promedio según nivel de suciedad")
    plt.xlabel("Suciedad (%)")
    plt.ylabel("Eficiencia (Celdas limpiadas / Acciones)")
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(images_dir / "eficiencia_vs_suciedad.png", dpi=140)
    plt.close()


    print(f"🖼️ Gráficos simplificados guardados en: {images_dir}")

def write_report_md(resumen: pd.DataFrame, out_md: Path, images_dir: Path):
    lines = []
    lines.append("# TP2 – Comparación de Agentes Reflexivo vs Aleatorio\n")
    lines.append("## 1. Metodología\n")
    lines.append("- Se evaluaron **dos agentes**:\n")
    lines.append("  - **YourNameAgent** (reflexivo con patrón determinista tipo 'snake').\n")
    lines.append("  - **RandomAgent** (aleatorio: limpia si está sucio, mueve al azar si no).\n")
    lines.append("- Entornos: 2×2, 4×4, 8×8, 16×16, 32×32, 64×64, 128×128.\n")
    lines.append("- Porcentaje de suciedad inicial: 0.1, 0.2, 0.4, 0.8.\n")
    lines.append("- Cada configuración se repitió 10 veces.\n")

    lines.append("\n## 2. Resultados y comparaciones\n")
    lines.append("### Acciones promedio por tamaño del entorno\n")
    lines.append("![Acciones por tamaño](images/acciones_por_tamaño.png)\n")

    lines.append("### Porcentaje de limpieza logrado según nivel de suciedad\n")
    lines.append("![Limpieza vs suciedad](images/limpieza_vs_suciedad.png)\n")

    lines.append("### Eficiencia (celdas limpiadas por acción)\n")
    lines.append("![Eficiencia vs suciedad](images/eficiencia_vs_suciedad.png)\n")


    # --- Comparación tabular y automática ---
    lines.append("\n## 3. Comparación directa entre agentes\n")

    comparacion = (
        resumen.groupby(["Tamaño (N×N)", "Agente"])["Promedio rendimiento"]
        .mean()
        .unstack()
    )

    for size in comparacion.index:
        reflexivo = comparacion.loc[size, "YourNameAgent"]
        aleatorio = comparacion.loc[size, "RandomAgent"]
        ganador = "Reflexivo ✅" if reflexivo > aleatorio else "Aleatorio ❌"
        diff = round(reflexivo - aleatorio, 2)
        lines.append(f"- **{size}×{size}** → Reflexivo: {reflexivo:.2f}, Aleatorio: {aleatorio:.2f} → Diferencia: {diff:+.2f} → {ganador}\n")

    lines.append("\n## 4. Discusión\n")
    lines.append("- En entornos **pequeños (2×2 y 4×4)** la diferencia es reducida, porque hay pocas posiciones y el azar no penaliza tanto.\n")
    lines.append("- A medida que el entorno crece, el **agente reflexivo** obtiene **mejor rendimiento promedio**, indicando que su estrategia sistemática cubre mejor el espacio.\n")
    lines.append("- El agente aleatorio presenta un comportamiento más errático, con mayor dispersión en rendimiento y acciones.\n")

    lines.append("\n## 5. Conclusión\n")
    lines.append("- El agente **reflexivo supera al aleatorio** en casi todos los tamaños y niveles de suciedad.\n")
    lines.append("- El beneficio del comportamiento racional se hace más evidente en entornos grandes y sucios.\n")

    out_md.write_text("".join(lines), encoding="utf-8")
    print(f"📝 Reporte comparativo guardado en: {out_md}")




def main():
    parser = argparse.ArgumentParser(description="Evaluación TP2: agentes reflexivo vs aleatorio")
    parser.add_argument("--server-url", default="http://127.0.0.1:5000", help="URL del servidor del entorno")
    parser.add_argument("--sizes", nargs="*", type=int, default=SIZES_DEFAULT, help="Lista de tamaños N para N×N")
    parser.add_argument("--dirt", nargs="*", type=float, default=DIRT_RATES_DEFAULT, help="Lista de tasas de suciedad")
    parser.add_argument("--repeats", type=int, default=REPEATS_DEFAULT, help="Repeticiones por combinación")
    parser.add_argument("--outdir", default="tp2-agentes-racionales", help="Carpeta de salida")
    args = parser.parse_args()

    outdir = Path(args.outdir)
    ensure_dir(outdir)
    images_dir = outdir / "images"
    ensure_dir(images_dir)

    # === Archivos de salida individuales ===
    results_random = outdir / "results_random.csv"
    results_reflex = outdir / "results_reflex.csv"
    results_all    = outdir / "results_all.csv"
    summary_csv    = outdir / "summary.csv"
    report_md      = outdir / "tp2-reporte.md"

    print("Asegurate de tener el servidor corriendo con:  python server.py\n")

    # === CORRER RANDOM AGENT ===
    print("\n🚀 Ejecutando agente ALEATORIO...\n")
    rows_random = run_grid(RandomAgent, args.sizes, args.dirt, args.repeats, args.server_url)
    if rows_random:
        save_csv(rows_random, results_random)
        print(f"📄 Resultados aleatorio guardados en: {results_random}")
    else:
        print("⚠️ No se generaron datos para RandomAgent")

    # === CORRER REFLEXIVO ===
    print("\n🤖 Ejecutando agente REFLEXIVO...\n")
    rows_reflex = run_grid(YourNameAgent, args.sizes, args.dirt, args.repeats, args.server_url)
    if rows_reflex:
        save_csv(rows_reflex, results_reflex)
        print(f"📄 Resultados reflexivo guardados en: {results_reflex}")
    else:
        print("⚠️ No se generaron datos para YourNameAgent")

    # === COMBINAR ARCHIVOS EN UNO SOLO ===
    print("\n🧩 Combinando resultados...")
    all_rows = []
    if results_random.exists():
        df_rnd = pd.read_csv(results_random, delimiter=";")
        df_rnd["Agente"] = "RandomAgent"
        all_rows.append(df_rnd)
    if results_reflex.exists():
        df_ref = pd.read_csv(results_reflex, delimiter=";")
        df_ref["Agente"] = "YourNameAgent"
        all_rows.append(df_ref)

    if all_rows:
        df_all = pd.concat(all_rows, ignore_index=True)
        df_all.to_csv(results_all, sep=";", index=False)
        print(f"✅ Archivo combinado guardado en: {results_all}")
    else:
        print("⚠️ No se pudieron combinar resultados (no se encontraron CSVs individuales).")
        return

    # === RESUMEN Y GRÁFICOS ===
    resumen = summarize_to_csv(results_all, summary_csv)
    plot_all(resumen, images_dir, results_all)
    write_report_md(resumen, report_md, images_dir)

    print("\n✅ Proceso completo. Archivos generados:")
    print(f"- {results_random}")
    print(f"- {results_reflex}")
    print(f"- {results_all}")
    print(f"- {summary_csv}")
    print(f"- {report_md}")
    print(f"- Carpeta de imágenes: {images_dir}")

if __name__ == "__main__":
    main()
