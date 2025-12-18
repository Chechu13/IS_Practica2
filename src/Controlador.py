import os

import numpy as np
import pandas as pd
from numpy.f2py.auxfuncs import throw_error
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report

from Lectura import Lectura
from DetectorIncidencia import DetectorIncidencia
from IncidenciaBloqueo import IncidenciaBloqueo
from GestorSuscripciones import GestorSuscripciones




class Controlador:
    def __init__(self):
        self.detector = DetectorIncidencia()
        self.gestor = GestorSuscripciones()
        self.df = None

    def cargar_datos(self):
        directorio = os.path.dirname(os.path.abspath(__file__))
        ruta = os.path.join(directorio, "..", "Data", "Dataset-CV.csv")
        try:
            self.df = Lectura.leerCSV(ruta)
            print(f"Sistema: Datos cargados ({len(self.df)} registros).")

            self.df.loc[20000:, 'tiempo'] += pd.Timedelta(seconds=300)
        except FileNotFoundError:
            raise RuntimeError("Sistema ERROR: Archivo no encontrado.")

    def iniciar_sistema(self):
        print("--- INICIANDO SISTEMA DE CONTROL ---")
        self.cargar_datos()

        if self.df is None:
            return
        generator = np.random.default_rng(42)
        df_train, df_test = train_test_split(self.df, test_size=0.20, shuffle=False)

        print("Sistema: Entrenando IA...")
        X_test, y_test = self.detector.entrenar(df_train, df_test)

        print("Sistema: Detectando incidencias en tiempo real (Test)...")
        lista_incidencias = self.detector.detectar_incidencias(df_test)

        y_pred = self.detector.modelo.predict(X_test)
        print("\n--- REPORTE TÉCNICO (Métricas) ---")
        print(classification_report(y_test, y_pred, target_names=['Normal', 'Bloqueo', 'Voltaje']))

        print("\n--- NOTIFICANDO A SUSCRIPTORES ---")
        bloqueos = 0
        for inc in lista_incidencias:
            if isinstance(inc, IncidenciaBloqueo):
                bloqueos += 1
                self.gestor.notificar_suscriptores(inc)

        print(f"\nSistema: Proceso finalizado. Se reportaron {bloqueos} bloqueos críticos.")
