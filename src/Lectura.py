import pandas as pd
import numpy as np


class Lectura:
    def __init__(self, hora, valorBinario, voltaje):
        self.hora = hora
        self.valorBinario = valorBinario
        self.voltaje = voltaje

    @staticmethod
    def leerCSV(ruta_archivo):
        df = pd.read_csv(ruta_archivo, sep=';')

        df['group_id'] = np.arange(len(df)) // 6

        df_pivot = df.pivot_table(index='group_id',
                                  columns=['canal', 'medida'],
                                  values='valor',
                                  aggfunc='first')

        df_pivot.columns = [f'{col[1]}_{col[0]}' for col in df_pivot.columns]

        tiempo_real = df.groupby('group_id')['tiempo'].first()
        df_pivot['tiempo'] = pd.to_datetime(tiempo_real, dayfirst=True)

        df_pivot['id'] = df.groupby('group_id')['id'].first()

        cols = ['tiempo', 'id'] + [c for c in df_pivot.columns if c not in ['tiempo', 'id']]
        df_final = df_pivot[cols].reset_index(drop=True)

        return df_final

    def detectarTren(self):
        return self.valorBinario == 0