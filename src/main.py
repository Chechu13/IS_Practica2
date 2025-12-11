import os
import pandas as pd
# Añadimos la importación de métricas de scikit-learn
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, accuracy_score

# Importamos tus clases
from Lectura import Lectura
from DetectorIncidencia import DetectorIncidencia
from IncidenciaBloqueo import IncidenciaBloqueo
from IncidenciaVoltaje import IncidenciaVoltaje

# ---------------------------------------------------------
# 1. CARGA DE DATOS
# ---------------------------------------------------------
print("--- 1. CARGANDO DATOS ---")
directorio = os.path.dirname(os.path.abspath(__file__))
ruta = os.path.join(directorio, "..", "Data", "Dataset-CV.csv")

try:
    df = Lectura.leerCSV(ruta)
    print(f"Datos cargados: {len(df)} registros totales.")
except FileNotFoundError:
    print("ERROR: No encuentro el archivo Dataset-CV.csv en la carpeta Data.")
    exit()

# ---------------------------------------------------------
# 2. ESCANER FORENSE Y DATA AUGMENTATION
# ---------------------------------------------------------
print("\n--- 2. ESCANEANDO ARCHIVO EN BUSCA DE BLOQUEOS REALES ---")

# Calculamos dónde se cortará el archivo (80%)
punto_corte = int(len(df) * 0.80)

# Buscamos manualmente huecos > 120s
df['diff_check'] = df['tiempo'].diff().dt.total_seconds().fillna(0)
bloqueos_reales = df[df['diff_check'] > 120]

print(f" > Se han encontrado {len(bloqueos_reales)} bloqueos REALES en todo el archivo.")

if len(bloqueos_reales) > 0:
    print("\n   LISTADO DE BLOQUEOS REALES:")
    print(f"   {'Fila':<10} | {'Hora':<20} | {'Duración (s)':<15} | {'¿Dónde cae?'}")
    print("-" * 70)

    hay_bloqueos_en_test = False

    for idx, row in bloqueos_reales.iterrows():
        zona = "ENTRENAMIENTO" if idx < punto_corte else "TEST (Examen)"
        if idx >= punto_corte:
            hay_bloqueos_en_test = True
        print(f"   {idx:<10} | {str(row['tiempo']):<20} | {row['diff_check']:<15} | {zona}")

    print("-" * 70)

print("\n--- 2.1. APLICANDO DATA AUGMENTATION (Necesario para aprendizaje) ---")
fila_didactica = 20000
print(f" > Creando ejemplo de bloqueo en fila {fila_didactica} para que la IA aprenda...")
df.loc[fila_didactica:, 'tiempo'] += pd.Timedelta(seconds=300)

# ---------------------------------------------------------
# 3. DIVISIÓN Y ENTRENAMIENTO
# ---------------------------------------------------------
# Borramos la columna auxiliar del check
df = df.drop(columns=['diff_check'])

# Dividimos en Train/Test
df_train, df_test = train_test_split(df, test_size=0.20, shuffle=False)
print(f"\n--- 3. SPLIT DE DATOS (80% / 20%) ---")
print(f"Entrenamiento: {len(df_train)} filas | Test: {len(df_test)} filas")

cerebro = DetectorIncidencia()

# 4. ENTRENAMIENTO
print("\n--- 4. ENTRENANDO MODELO (Random Forest) ---")
# El método entrenar devuelve los datos necesarios para las métricas
X_test_base, y_test_real = cerebro.entrenar(df_train, df_test) # CAMBIO AQUI
print("Modelo entrenado correctamente.")

# ---------------------------------------------------------
# 5. PREDICCIÓN Y RESULTADOS
# ---------------------------------------------------------
print("\n--- 5. PREDICCIÓN Y MÉTRICAS DE TESTING ---")

# Generamos las predicciones del modelo sobre el conjunto X_test_base
y_pred_metricas = cerebro.modelo.predict(X_test_base)

# Calculamos las incidencias reales y el informe de objetos (Como antes)
lista_incidencias = cerebro.detectar_incidencias(df_test)

# --- REPORTE DE MÉTRICAS ---
print("\n=== REPORTE DE CLASIFICACIÓN (Precisión y F1-Score) ===")
# Los nombres de las clases son 0: Normal, 1: Bloqueo, 2: Voltaje (ver Detector)
# Ponemos la etiqueta 0, 1 y 2 para el reporte
print(classification_report(y_test_real, y_pred_metricas, target_names=['Normal (0)', 'Bloqueo (1)', 'Voltaje (2)']))

# --- REPORTE DE OBJETOS CREADOS ---
contador_bloqueos = 0
contador_voltaje = 0

print(f"\nINFORME DE OBJETOS CREADOS ({len(lista_incidencias)} incidencias totales):")
print("-" * 60)

impresos_voltaje = 0

for incidencia in lista_incidencias:
    if isinstance(incidencia, IncidenciaBloqueo):
        contador_bloqueos += 1
        print(f" -> [¡BLOQUEO DETECTADO!] {incidencia.hora} -> {incidencia.describir_problema()}")

    elif isinstance(incidencia, IncidenciaVoltaje):
        contador_voltaje += 1
        if impresos_voltaje < 3:
            print(f"[VOLTAJE] {incidencia.hora} -> {incidencia.describir_problema()}")
            impresos_voltaje += 1

print("-" * 60)
print("RESUMEN FINAL:")
print(f"  > Incidencias de Bloqueo: {contador_bloqueos}")
print(f"  > Incidencias de Voltaje: {contador_voltaje}")
print("-" * 60)