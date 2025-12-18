import numpy as np
from sklearn.ensemble import RandomForestClassifier
from IncidenciaBloqueo import IncidenciaBloqueo
from IncidenciaVoltaje import IncidenciaVoltaje


class DetectorIncidencia:
    def __init__(self):
        self.modelo = RandomForestClassifier(n_estimators=200, random_state=42, class_weight='balanced', min_samples_leaf=1, max_features="sqrt")
        self.cols_voltaje = ['voltageReceiver1_a', 'voltageReceiver2_a', 'voltageReceiver1_b', 'voltageReceiver2_b']

    def _preparar_datos(self, df):
        df = df.copy()

        df['max_diff_voltaje'] = 0.0
        for col in self.cols_voltaje:
            diff_col = df[col].diff().abs().fillna(0)
            df['max_diff_voltaje'] = np.maximum(df['max_diff_voltaje'], diff_col)

        df['diff_tiempo'] = df['tiempo'].diff().dt.total_seconds().fillna(0)

        features = ['status_ALL', 'diff_tiempo', 'max_diff_voltaje'] + self.cols_voltaje
        X = df[features].fillna(0)

        y = np.zeros(len(df))
        mask_voltaje = df['max_diff_voltaje'] >= 0.5
        y[mask_voltaje] = 2
        mask_bloqueo = df['diff_tiempo'] > 120
        y[mask_bloqueo] = 1

        return X, y

    def entrenar(self, df_entrenamiento, df_test):
        X_train, y_train = self._preparar_datos(df_entrenamiento)
        self.modelo.fit(X_train, y_train)

        X_test, y_test = self._preparar_datos(df_test)

        return X_test, y_test

    def detectar_incidencias(self, df_prueba):
        X_proc, y_proc = self._preparar_datos(df_prueba)
        predicciones = self.modelo.predict(X_proc)

        lista_incidencias = []

        for i, pred in enumerate(predicciones):
            if pred == 0:
                continue

            fila = df_prueba.iloc[i]
            hora = fila['tiempo']
            disp_id = fila['id']

            X_row = X_proc.iloc[i]

            if pred == 1:  # Bloqueo
                duracion = X_row['diff_tiempo']
                nueva_incidencia = IncidenciaBloqueo(disp_id, hora, duracion)
                lista_incidencias.append(nueva_incidencia)

            elif pred == 2:  # Voltaje
                voltaje_actual = X_row[self.cols_voltaje[0]]
                diferencia = X_row['max_diff_voltaje']
                nueva_incidencia = IncidenciaVoltaje(disp_id, hora, voltaje_actual, diferencia)
                lista_incidencias.append(nueva_incidencia)

        return lista_incidencias
