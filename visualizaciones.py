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
import pandas as pd

py.offline.init_notebook_mode(connected=True)
from plotly.offline import plot


# -- -------------------------------------------------------------- FUNCION: Grafica de pie -- #
# -- ------------------------------------------------------------------------------------ -- #
# -- Grafica el ranking de las operaciones
def plot_ranking(stats):
    """
    Parameters
    ----------
    stats : Función que calcula estadisticas y ordena las operaciones por mayor inversión
    Returns
    -------
    pie_ranking : Gráfica de pastel que muestra el porcentaje que cada simbolo tuvo en operaciones

    Debugging
    --------
    stats = fn.f_estadisticas_ba(datos)
    """
    ranking = stats['df_2_ranking']
    symbols = ranking['symbol']
    rank = ranking['rank']
    pie_ranking = go.Figure(data=[go.Pie(labels=symbols, values=rank, pull=[0.1, 0.1, 0, 0, 0, 0, 0, 0, 0, 0, 0])])
    pie_ranking.update_layout(title="Ranking de operaciones",
                              font=dict(size=16))
    pie_ranking.show()


# -- -------------------------------------------------------------- FUNCION: Grafica profit y Drawdown/up -- #
# -- ------------------------------------------------------------------------------------ -- #
# -- Grafica que muestra el profit acumulado diario y el drawdown/up
def plot_profit_diario(profit_diario):
    """

    Parameters
    ----------
    profit_diario: Funcion que muestra una tabla con el dia y el profit diario y el acumulado

    Returns
    -------
    tabla con el profit diario acumulado y las lineas de drawdown/up

    Debugging
    --------
    profit_diario = fn.f_profit_diario(datos)
    """
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=profit_diario.values.T[0], y=profit_diario.profit_acm_d, mode='lines',
                             name='Profit diario', line=dict(color='black')))
    # Drawdown
    min_val = profit_diario.profit_acm_d.min()
    chch = profit_diario.loc[profit_diario['profit_acm_d'] == profit_diario.profit_acm_d.min()]
    position = chch.index.tolist()
    lista = profit_diario.loc[0:position[0]]
    max_lista = lista.max()
    max_fecha = lista.loc[lista['profit_acm_d'] == lista.profit_acm_d.max()]
    posicion_inicial = max_fecha.index.tolist()
    max_gg = lista.loc[posicion_inicial[0], 'timestamp']
    max_aa = lista.loc[posicion_inicial[0], 'profit_acm_d']
    min_lista = lista.min()
    min_lista = lista.loc[lista['profit_acm_d'] == lista.profit_acm_d.min()]
    posicion_final = min_lista.index.tolist()
    min_gg = lista.loc[posicion_final[0], 'timestamp']
    min_hh = lista.loc[posicion_final[0], 'profit_acm_d']
    fig.add_shape(
        # Line Horizontal
        type="line",
        x0=max_gg,
        y0=max_aa,
        x1=min_gg,
        y1=min_hh,
        line=dict(
            color="crimson",
            width=4,
            dash="dashdot",
        ),
    )

    ## DRAWUP
    max_val = profit_diario.profit_acm_d.max()
    localizar = profit_diario.loc[profit_diario['profit_acm_d'] == profit_diario.profit_acm_d.max()]
    # Obtenemos su posicion en la tabla
    position_max = localizar.index.tolist()
    # Dependiendo si el maximo esta a la derecha o a la izquierda del minimo se tomara el fragmento de lista asignado
    if position_max > position:
        lista2 = profit_diario.loc[position[0]:]
    else:
        lista2 = profit_diario.loc[0:position_max[0]]
    # Sacamos el maximo y el minimo de esta lista
    max_lista = lista2.max()
    max_fecha2 = lista2.loc[lista2['profit_acm_d'] == lista2.profit_acm_d.max()]
    posision_inicial2 = max_fecha2.index.tolist()
    max_ff = lista2.loc[posision_inicial2[0], 'timestamp']
    max_mm = lista2.loc[posision_inicial2[0], 'profit_acm_d']
    min_lista = lista2.min()
    min_fecha2 = lista2.loc[lista2['profit_acm_d'] == lista2.profit_acm_d.min()]
    posision_final2 = min_fecha2.index.tolist()
    min_ff = lista2.loc[posision_final2[0], 'timestamp']
    min_mm = lista2.loc[posision_final2[0], 'profit_acm_d']

    fig.add_shape(
        # Line Horizontal
        type="line",
        x0=min_ff,
        y0=min_mm,
        x1=max_ff,
        y1=max_mm,
        line=dict(
            color="LightSeaGreen",
            width=4,
            dash="dashdot",
        ),
    )

    fig.update_layout(
        title="Profit, Drawdown, Drawup",
        xaxis_title="Time",
        yaxis_title="Profit acumulado",
    )
    fig.show()


# -- -------------------------------------------------------------- FUNCION: Grafica Disposition Effect -- #
# -- ------------------------------------------------------------------------------------ -- #
# -- Grafica de barras que representa la cantidad de veces que se observó cada principio del disposition effect
def plot_de(ocurrencias):
    """
    
    Parameters
    ----------
    ocurrencias: tabla con los principios del Disposition Effect

    Returns
    -------
    fig: grafica de barras que representa cada uno de los principios
    
    Debugging
    --------
    ocurrencias = fn.f_be_de(datos)
    """
    rr = ocurrencias['Caracteristicas']
    dat = rr.loc[0, :]
    # Si tiene el trader sensibilidad decreciente se mostrará en la barras con un 1 y si no se mostrará con un 0
    if dat['sensibilidad_decreciente'] == 'Sí':
        dat['sensibilidad_decreciente'] = 1
    else:
        dat['sensibilidad_decreciente'] = 0
    fig = go.Figure(
        data=[
            go.Bar(x=rr.columns[1:], y=[dat['status_quo'], dat['aversion_perdida'], dat['sensibilidad_decreciente']])],
        layout=dict(title=dict(text="Disposition Effect"))
    )

    fig.show()
