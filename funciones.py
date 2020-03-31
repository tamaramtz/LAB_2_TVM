# -- ------------------------------------------------------------------------------------ -- #
# -- proyecto: Microestructura y Sistemas de Trading - Laboratorio 2 - Behavioral Finance
# -- archivo: datos.py - datos generales para uso en el proyecto
# -- mantiene: Tamara Mtz.
# -- repositorio: https://github.com/tamaramtz/LAB_2_TVM.git
# -- ------------------------------------------------------------------------------------ -- #
import pandas as pd
import numpy as np
import datetime as dt
from datetime import timedelta

# -- -------------------------------------------------------------- FUNCION: Leer archivo -- #
# -- ------------------------------------------------------------------------------------ -- #
# -- Leer un archivo externo en Excel

def f_leer_archivo(param_archivo):
    '''

    Parameters
    ----------
    param_archivo : str : nombre de archivo a leer
    Returns
    -------
    df_data : pd.DataFrame : con informacion contenida en archivo leido
    Debugging
    ---------
    param_archivo = 'archivo_tradeview_1.xlsx'

    '''

    # Leer archivo de datos y guardarlo en un DataFrame
    df_data = pd.read_excel('archivos/' + param_archivo, sheet_name='Hoja1')

    # Cnvertir en minusculas el nombre de las columnas
    df_data.columns = [list(df_data.columns)[i].lower()
                       for i in range(0, len(df_data.columns))]
    # Asegurar que ciertas son del tipo numerico
    numcols = ['s/l', 't/p', 'commission', 'openprice', 'closeprice', 'profit', 'size', 'swap',
              'taxes', 'order']

    df_data[numcols] = df_data[numcols].apply(pd.to_numeric)

    #print(df_data)
    return df_data
# -- ------------------------------------------------------ FUNCION: Pips por instrumento -- #
# -- calcular el tamaño de los pips por instrumento

def f_pip_size(param_ins):
    """
       Parameters
       ----------
       param_ins : str : nombre de instrumento
       Returns
       -------
       Debugging
       -------
       param_ins = 'usdjpy'
       """

    # encontrar y eliminar un guion bajo
    # inst = param_ins.replace('_', '')

    # transformar a minusculas
    inst = param_ins.lower()

    # lista de pips por instrumento
    pips_inst = {'usdjpy': 100, 'gbpjpy': 100, 'eurjpy': 100, 'cadjpy': 100,
                 'chfjpy': 100,
                 'eurusd': 10000, 'gbpusd': 10000, 'usdcad': 10000, 'usdmxn': 10000,
                 'audusd': 10000, 'nzdusd': 10000,
                 'usdchf': 10000,
                 'eurgbp': 10000, 'eurchf': 10000, 'eurnzd': 10000, 'euraud': 10000,
                 'gbpnzd': 10000, 'gbpchf': 10000, 'gbpaud': 10000,
                 'audnzd': 10000, 'nzdcad': 10000, 'audcad': 10000,
                 'xauusd': 10, 'xagusd': 10, 'btcusd': 1}

    return pips_inst[inst]

# -- ------------------------------------ FUNCION: Columnas de transformaciones de tiempo -- #
# -- ------------------------------------------------------------------------------------ -- #
# -- calcular la diferencia entre el tiempo open y close

def f_columnas_tiempos(param_data):
    """
    Parameters
    ----------
    :param param_data: dataframe conteniendo por lo menos las columnas 'closetime' y 'opentime'

    Returns
    -------
    :return param_data: dataframe ingresado mas columna 'time' que es la diferencia entre close y open

    Debugging
    --------
    param_data = datos
    """
    # Convertir las columnas de closetime y opentime con to_datetime
    param_data['closetime'] = pd.to_datetime(param_data['closetime'])
    param_data['opentime'] = pd.to_datetime(param_data['opentime'])

    # Tiempo transcurrido de una operación
    param_data['tiempo'] = [(param_data.loc[i, 'closetime'] - param_data.loc[i, 'opentime']).delta / 1e9
                            for i in range(0, len(param_data['closetime']))]

    return param_data


# -- -------------------------------------- FUNCION: Columnas de transformaciones de pips -- #
# -- ------------------------------------------------------------------------------------ -- #
# -- calcular la cantidad de pips resultantes por cada operación

def f_columnas_pips(param_data):
    """

    Parameters
    ----------
    param_data:  dataframe conteniendo por lo menos las columnas 'closetime' y 'opentime'

    Returns
    -------
    param_data:

    debugging
    ---------
    param_data = datos
    """
    param_data['pip_size'] = 0
    #for i in range(0, len(param_data['type'])):
        #print(i)
        #print(param_data.loc[i, 'symbol'])
        #(closeprice - openprice)*multiplicador
        #param_data['pip_size'] = np.zeros(len(param_data['type']))
        #param_data['pip_size'] = (param_data[param_data['type'] == 'sell']['openprice'] - \
                                 #param_data[param_data['type'] == 'sell']['closeprice']) * \
                                 #f_pip_size(param_data.loc[i, 'symbol'])
        #param_data['pip_size'][param_data['type'] == 'buy'] = (param_data[param_data['type'] == 'buy']['closeprice'] - \
                               #param_data[param_data['type'] == 'buy']['openprice']) * \
                                                              #f_pip_size(param_data.loc[i, 'symbol'])

    param_data['pips'] = [(param_data.loc[i, 'closeprice'] - param_data.loc[i, 'openprice']) *
                             f_pip_size(param_data.loc[i, 'symbol']) if param_data.loc[i, 'type'] == 'buy'
                          else (param_data.loc[i, 'openprice'] - param_data.loc[i, 'closeprice']) *
                               f_pip_size(param_data.loc[i, 'symbol']) for i in param_data.index]
    param_data['pips_acum'] = param_data['pips'].cumsum()
    param_data['profit_acm'] = param_data['profit'].cumsum()

    return param_data

# -- -------------------------------------------------------------- FUNCION: Diccionario de estadisticas -- #
# -- ------------------------------------------------------------------------------------ -- #
# -- Un diccionario, dos tablas
def f_estadisticas_ba(param_data):
    """

    Parameters
    ----------
    param_data

    Returns
    -------
    dataFrame
    """
    # Creamos DataFrame
    df_ba = pd.DataFrame(index=['Ops totales', 'Ganadoras', 'Ganadoras_c', 'Ganadoras_v', 'Perdedoras', 'Perdedoras_c',
                                'Perdedoras_v', 'Media (Profit)', 'Media (Pips)', 'r_efectividad', 'r_proporcion',
                                'r_efectividad_c', 'r_efectividad_v'], columns=['valor', 'descripcion'])
    df_ba.index.name = "medida"
    # Se llena el DataFrame
    df_ba.loc['Ops totales', ['valor', 'descripcion']] = [len(param_data['order']), 'Operaciones totales']
    df_ba.loc['Ganadoras', ['valor', 'descripcion']] = [len(param_data[param_data['pips'] >= 0]),
                                                        'Operaciones ganadoras']
    df_ba.loc['Ganadoras_c', ['valor', 'descripcion']] = [len(param_data[(param_data['type'] == 'buy') &
                                                                         (param_data['pips'] >= 0)]),
                                                          'Operaciones ganadoras de compra']
    df_ba.loc['Ganadoras_v', ['valor', 'descripcion']] = [len(param_data[(param_data['type'] == 'sell') &
                                                                         (param_data['pips'] >= 0)]),
                                                          'Operaciones ganadoras de venta']
    df_ba.loc['Perdedoras', ['valor', 'descripcion']] = [len(param_data[param_data['pips'] < 0]),
                                                         'Operaciones perdedoras']
    df_ba.loc['Perdedoras_c', ['valor', 'descripcion']] = [len(param_data[(param_data['type'] == 'buy') &
                                                                          (param_data['pips'] <= 0)]),
                                                           'Operaciones perdedoras de compra']
    df_ba.loc['Perdedoras_v', ['valor', 'descripcion']] = [len(param_data[(param_data['type'] == 'sell') &
                                                                          (param_data['pips'] <= 0)]),
                                                           'Operaciones perdedoras de venta']
    df_ba.loc['Media (Profit)', ['valor', 'descripcion']] = [param_data['profit'].median(),
                                                             'Mediana de profit de operaciones']
    df_ba.loc['Media (Pips)', ['valor', 'descripcion']] = [np.trunc(param_data['pips'].median()),
                                                           'Mediana de pips de operaciones']
    df_ba.loc['r_efectividad', ['valor', 'descripcion']] = [np.round(len(param_data[param_data['pips'] >= 0]) /
                                                            len(param_data['order']), 2),
                                                            'Ganadoras Totales/Operaciones Totales']
    df_ba.loc['r_proporcion', ['valor', 'descripcion']] = [np.round(len(param_data[param_data['pips'] >= 0]) /
                                                           len(param_data[param_data['pips'] < 0]), 2),
                                                           'Perdedoras Totales/Ganadoras Totales']
    df_ba.loc['r_efectividad_c', ['valor', 'descripcion']] = [np.round(len(param_data[(param_data['type'] == 'buy') &
                                                                             (param_data['pips'] >= 0)]) /
                                                              len(param_data['order']), 2),
                                                              'Ganadoras Totales/Operaciones Totales']
    df_ba.loc['r_efectividad_v', ['valor', 'descripcion']] = [np.round(len(param_data[(param_data['type'] == 'sell') &
                                                                             (param_data['pips'] >= 0)]) /
                                                              len(param_data['order']), 2),
                                                              'Ganadoras Totales/Operaciones Totales']

    # Obtenemos los instrumentos en donde se invirtio
    symbols = np.unique(param_data.symbol)

    # Creamos DataFrame
    df_r = pd.DataFrame(columns=['rank'])
    df_r.index.name = "symbol"

    # Se dividen las ganadoras entre la cantidad de operaciones
    rank = [len(param_data[param_data.profit > 0][param_data.symbol == i]) / len(param_data[param_data.symbol == i])
            for i in symbols]
    # Se mete dentro del DataFrame
    df_r['rank'] = rank
    df_r['symbol'] = symbols
    # Ordenamos los valores de forma descendente
    df_r.sort_values(by='rank', ascending=False)
    # Se regresa en forma de diccionario
    return {'df_1_tabla': df_ba, 'df_2_ranking': df_r}

# -- -------------------------------------------------------------- FUNCION: Capital acumulado -- #
# -- ------------------------------------------------------------------------------------ -- #
# -- Columna con el profit acumulado

def f_capital_acm(param_data):
    """

    Parameters
    ----------
    param_data:  dataframe del historico de operaciones

    Returns
    -------
    param_data: con clumna del profit acumulado teniendo en cuenta los 5000 con los que se inicio la cuenta
    """
    # Se crea una coluna llena de ceros
    param_data['capital_acm'] = 0
    # Se suma al profit acumuludo los 5000 con los que se inició
    param_data['capital_acm'] = param_data['profit_acm'] + 5000

    return param_data

# -- -------------------------------------------------------------- FUNCION: Tabla de profit diario -- #
# -- ------------------------------------------------------------------------------------ -- #
# -- Una tambla con el dia y el profit diario y el acumulado

def f_profit_diario(param_data):
    """

    Parameters
    ----------
    param_data:  dataframe del historico de operaciones

    Returns
    -------
    tabla con profit diario y profit diario acumulado

    """
    df_pr = pd.DataFrame(columns=['timestamp','profit_d', 'profit_acm_d'])

    df_pr['timestamp'] = pd.date_range(param_data.closetime.min(), param_data.closetime.max(), freq='D').date
    df_pr['profit_d'] =

    return df_pr
# -- ---------------------------------------------------- FUNCION: Estadisticas financieras -- #
# -- ------------------------------------------------------------------------------------ -- #
# -- Una tabla con diferentes métricas de atribución


def f_estadisticas_mad(param_data):
    """

    Parameters
    ----------
    param_data: dataframe del historico de operaciones
    rf: tasa libre de riesgo

    Returns
    -------
    df_mad: dataframe Medidas de Atribución al Desempeño

    """
    # Rendimientos logaritmicos
    rendto = np.log(param_data.capital_acm/param_data.capital_acm.shift(1)).iloc[1:]
    # Promedio de los rendimientos logaritmicos semanales
    rend_log = np.mean(rendto)
    # Desviación estándar de los rendimientos
    desvest = rendto.std()
    rf = 0.08/300
    # mar = .3/300

    df_mad = pd.DataFrame(
        index=['sharpe', 'sortino_c', 'sortino_v', 'drawdown_capi_c', 'drawdown_capi_u', 'information_r'],
        columns=['valor', 'descripcion'])
    df_mad.index.name = "medida"

    df_mad.loc['sharpe', ['valor', 'descripcion']] = [(rend_log-rf)/desvest, 'Sharpe Ratio']
    df_mad.loc['sortino_c', ['valor', 'descripcion']] = [(rend_log - rf) / \
                                                        rendto[rendto >= 0].std() * np.sqrt(300),
                                                         'Sortino Ratio para Posiciones  de Compra']
    df_mad.loc['sortino_v', ['valor', 'descripcion']] = [(rend_log - rf) / \
                                                        rendto[rendto < 0].std() * np.sqrt(300),
                                                         'Sortino Ratio para Posiciones  de Venta']

    return(df_mad)












