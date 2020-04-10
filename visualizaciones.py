# -- ------------------------------------------------------------------------------------ -- #
# -- proyecto: Microestructura y Sistemas de Trading - Laboratorio 2 - Behavioral Finance
# -- archivo: datos.py - datos generales para uso en el proyecto
# -- mantiene: Tamara Mtz.
# -- repositorio: https://github.com/tamaramtz/LAB_2_TVM.git
# -- ------------------------------------------------------------------------------------ -- #

import matplotlib.pyplot as plt
import funciones as fn
import plotly.graph_objects as go
import plotly as py

py.offline.init_notebook_mode(connected=True)
from plotly.offline import plot
import pandas as pd


def plot_ranking(estadisticas):
    """
    Parameters
    ----------
    estadisticas : función : Función utilizada para calcular el ranking de asertividad de divisas
    Returns
    -------
    graph : gráfica de pastel con plotly mostrando el porcentaje que representa la asertividad del total de pares usados
    """
    estadisticas = fn.f_estadisticas_ba(datos)
    df_ranking = pd.DataFrame(estadisticas['df_2_ranking'])
    df_1_ranking = df_ranking.reset_index()
    df_ranking = df_1_ranking.rename(columns={"index": "pares", "rank": "rank"})

    labels = df_ranking['pares']
    values = df_ranking['rank']
    pie_rank = go.Figure(data=[
        go.Pie(labels=labels, values=values, pull=[0.2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
               title='Asertividad de pares')])
    pie_rank.update_layout(title="Ranking de asertividad de pares", font=dict(size=16))
    pie_rank.show()
