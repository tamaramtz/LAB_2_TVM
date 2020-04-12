# -- ------------------------------------------------------------------------------------ -- #
# -- proyecto: Microestructura y Sistemas de Trading - Laboratorio 2 - Behavioral Finance
# -- archivo: datos.py - datos generales para uso en el proyecto
# -- mantiene: Tamara Mtz.
# -- repositorio: https://github.com/tamaramtz/LAB_2_TVM.git
# -- ------------------------------------------------------------------------------------ -- #
import pandas as pd
import numpy as np
import datetime as date
from datetime import timedelta

# Importar el modulo data del paquete pandas_datareader. La comunidad lo importa con el nombre de web
pd.core.common.is_list_like = pd.api.types.is_list_like
import pandas_datareader.data as web
import datos as dt
from oandapyV20 import API
import oandapyV20.endpoints.instruments as instruments


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
                 'xauusd': 10, 'xagusd': 10, 'btcusd': 1, 'usdhkd': 10000, 'cadhkd': 10000}

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
    df_2_ranking = pd.DataFrame(columns=['rank'])
    df_2_ranking.index.name = "symbol"

    # Se dividen las ganadoras entre la cantidad de operaciones
    rank = [len(param_data[param_data.profit > 0][param_data.symbol == i]) / len(param_data[param_data.symbol == i])
            for i in symbols]
    # Se mete dentro del DataFrame
    df_2_ranking['rank'] = rank
    df_2_ranking['symbol'] = symbols
    # Ordenamos los valores de forma descendente
    df_2_ranking = df_2_ranking.sort_values(by='rank', ascending=False)
    # Se regresa en forma de diccionario
    return {'df_1_tabla': df_ba, 'df_2_ranking': df_2_ranking}


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
# -- Una tabla con el dia y el profit diario y el acumulado

def f_profit_diario(param_data):
    """

    Parameters
    ----------
    param_data:  dataframe del historico de operaciones

    Returns
    -------
    tabla con profit diario y profit diario acumulado

    """
    # Se crea el DataFrame
    df_pr = pd.DataFrame(columns=['timestamp', 'profit_d', 'profit_acm_d'])
    # Sacamos la fecha inicial y final y el rango entre estas
    diario = pd.date_range(param_data.closetime.min(), param_data.closetime.max()).date
    # Llenamos la columna con las fechas
    df_pr['timestamp'] = diario
    # Inicializamos esta columna con ceros
    df_pr['profit_d'] = 0
    # Creamos una particion que solo tome los 10 primeros lugares
    y = slice(0, 10, 1)
    # Lo aplicamos a las fechas
    df_pr['timestamp'] = [str(i)[y] for i in diario]

    param_data['closetime'] = [str(i)[y] for i in param_data.closetime]
    # Sumamos los profit de un dia en todos los dias
    profit = np.round(param_data.groupby('closetime')['profit'].sum(), 2)
    # Llenamos la columna de profit diario confomre a las fechas en timestamp
    for i in range(len(df_pr['timestamp'])):
        for j in range(len(profit)):
            if df_pr['timestamp'][i] == profit.index[j]:
                df_pr['profit_d'][i] = profit[j]
    # Vamos sumando conforme pasan los dias el profit diario
    df_pr['profit_acm_d'] = df_pr['profit_d'].cumsum() + 5000

    return df_pr


# -- ---------------------------------------------------- FUNCION: descargar precios de cierre-- #
# -- ------------------------------------------------------------------------------------ -- #
# -- Descarga precios  de cierre ajustado de Yahoo

def get_adj_closes(tickers, start_date=None, end_date=None):
    # Fecha inicio por defecto (start_date='2010-01-01') y fecha fin por defecto (end_date=today)
    # Descargamos DataFrame con todos los datos
    closes = web.DataReader(name=tickers, data_source='yahoo', start=start_date, end=end_date)
    # Solo necesitamos los precios ajustados en el cierre
    closes = closes['Adj Close']
    # Se ordenan los índices de manera ascendente
    closes.sort_index(inplace=True)
    return closes


# -- ---------------------------------------------------- FUNCION: descargar precio de cierre-- #
# -- ------------------------------------------------------------------------------------ -- #
# -- Descarga el precio de cierre de un intrumento en una fecha en partiular

def f_precio(instrumento, fecha):
    """
    Parameters
    ---------
    instrumento: nombre del instrumento
    fecha : fecha del dia del precio

    Returns
    ---------
    pric: precio del intrumento en una fecha exacta
    """
    # API que se obtiene de OANDA
    token = API(environment="practice", access_token=dt.OA_Ak)
    # Convertimos a fecha
    fecha = fecha.strftime('%Y-%m-%dT%H:%M:%S')
    # Definimos los parametros necesarios
    parameters = {"count": 1, "granularity": 'M1', "price": "M", "dailyAlignment": 16, "from": fecha}
    # Definir instrumento
    instrument = instruments.InstrumentsCandles(instrument=instrumento, params=parameters)
    # Descargarlo de OANDA
    response = token.request(instrument)
    # En velas
    prices = response.get("candles")
    # Regresar el openprice
    pric = float(prices[0]['mid']['o'])
    return pric


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
    # Obtener los rendimientos diarios
    df_prof = f_profit_diario(param_data)
    # Rendimientos logaritmicos
    rendto = np.log(df_prof.profit_acm_d / df_prof.profit_acm_d.shift(1)).iloc[1:]
    # Rendimientos logaritmicos de las operaciones de compra
    compra = param_data[param_data['type'] == 'buy']
    pr_com = f_profit_diario(compra)
    rend_com = np.log(pr_com.profit_acm_d / pr_com.profit_acm_d.shift(1)).iloc[1:]
    # Rendimientos logaritmicos de las operaciones de venta
    venta = param_data[param_data['type'] == 'sell']
    pr_ven = f_profit_diario(venta)
    rend_ven = np.log(pr_ven.profit_acm_d / pr_ven.profit_acm_d.shift(1)).iloc[1:]
    # Promedio de los rendimientos logaritmicos semanales
    rend_log = np.mean(rendto)
    # Desviación estándar de los rendimientos
    desvest = rendto.std()
    rf = 0.08 / 300
    mar = .3 / 300

    df_mad = pd.DataFrame(
        index=['sharpe', 'sortino_c', 'sortino_v', 'drawdown_capi', 'drawup_capi', 'information_r'],
        columns=['valor', 'descripcion'])
    df_mad.index.name = "medida"

    df_mad.loc['sharpe', ['valor', 'descripcion']] = [(rend_log - rf) / desvest, 'Sharpe Ratio']
    df_mad.loc['sortino_c', ['valor', 'descripcion']] = [(rend_com.mean() - mar) / \
                                                         rend_com[rend_com < mar].std(),
                                                         'Sortino Ratio para Posiciones  de Compra']
    df_mad.loc['sortino_v', ['valor', 'descripcion']] = [(rend_ven.mean() - mar) / \
                                                         rend_ven[rend_ven < mar].std(),
                                                         'Sortino Ratio para Posiciones  de Venta']
    ## DRAWDOWN
    # Sacamos el minimo profit
    min_val = df_prof.profit_acm_d.min()
    # Obtenemos los datos de este minimo
    chch = df_prof.loc[df_prof['profit_acm_d'] == df_prof.profit_acm_d.min()]
    # Convertimos a lista el index
    position = chch.index.tolist()
    # Tomamos todas las operaciones que estaban antes del minimo
    lista = df_prof.loc[0:position[0]]
    # Sacamos de esta lista el maximo y el minimo
    max_lista = lista.max()
    max_fecha = lista.loc[lista['profit_acm_d'] == lista.profit_acm_d.max()]
    posicion_inicial = max_fecha.index.tolist()
    max_gg = lista.loc[posicion_inicial[0], 'timestamp']
    min_lista = lista.min()
    min_lista = lista.loc[lista['profit_acm_d'] == lista.profit_acm_d.min()]
    posicion_final = min_lista.index.tolist()
    min_gg = lista.loc[posicion_final[0], 'timestamp']
    # Sacamos la diferencia entre el maximo profit y el minimo de esa lista
    total = max_lista['profit_acm_d'] - min_val
    # Ponemos en una lista la fecha de inicio y final del drawdown junto con la diferencia de rendimientos
    drawdown = list([max_gg, min_gg, total])
    df_mad.loc['drawdown_capi', ['valor', 'descripcion']] = [[drawdown], 'DrawDown de Capital']

    ## DRAWUP
    # Sacamos el maximo valor de los profits acumulados
    max_val = df_prof.profit_acm_d.max()
    localizar = df_prof.loc[df_prof['profit_acm_d'] == df_prof.profit_acm_d.max()]
    # Obtenemos su posicion en la tabla
    position_max = localizar.index.tolist()
    # Dependiendo si el maximo esta a la derecha o a la izquierda del minimo se tomara el fragmento de lista asignado
    if position_max > position:
        lista2 = df_prof.loc[position[0]:]
    else:
        lista2 = df_prof.loc[0:position_max[0]]
    # Sacamos el maximo y el minimo de esta lista
    max_lista = lista2.max()
    max_fecha2 = lista2.loc[lista2['profit_acm_d'] == lista2.profit_acm_d.max()]
    posision_inicial2 = max_fecha2.index.tolist()
    max_ff = lista2.loc[posision_inicial2[0], 'timestamp']
    min_lista = lista2.min()
    min_fecha2 = lista2.loc[lista2['profit_acm_d'] == lista2.profit_acm_d.min()]
    posision_final2 = min_fecha2.index.tolist()
    min_ff = lista2.loc[posision_final2[0], 'timestamp']
    # Sacamos la diferencia entre el maximo profit y el minimo de esa lista
    total2 = max_lista['profit_acm_d'] - min_val
    # Ponemos en una lista la fecha de inicio y final del drawdown junto con la diferencia de rendimientos
    drawup = list([min_ff, max_ff, total2])
    df_mad.loc['drawup_capi', ['valor', 'descripcion']] = [[drawup], 'DrawUp de Capital']

    ## INFORMATION
    # Creamos una particion que solo tome los primeros 10 caracteres
    y = slice(0, 10, 1)
    # Se lo aplicamos a las fechas minima y maxima para sacar el inicio y el final del rango de fechas
    start = param_data['closetime'].min()[y]
    end = param_data['closetime'].max()[y]
    # Obtenemos los precios de S&P500 en las mimsa fechas que definimos antes
    closes = pd.DataFrame(get_adj_closes(tickers='^GSPC', start_date=start, end_date=end))
    # Sacamos el rendimieto de los precios descargados
    closes['rend_sp'] = np.log(closes / closes.shift(1)).iloc[1:]
    # Sacamos el rango de fechas que esta en el index y lo metemos en una columna
    fech = closes.index
    closes['Date'] = fech
    # Tomar solo el dia sin las horas
    closes['timestamp'] = [str(i)[y] for i in fech]
    # Merge para que las fechas sean las mismas
    berge = closes.merge(pd.DataFrame(df_prof), on='timestamp')
    # Remplazar el nan con un 0
    berge['rend_sp'][0] = 0
    # Promedio de los rendimientos
    prom_rend = berge['rend_sp'].mean()
    # Volvemos a sacar los rendimietos de las operaciones
    berge['rend_d_log'] = np.log(berge.profit_acm_d / berge.profit_acm_d.shift(1)).iloc[1:]
    # Remplazar el nan con un 0
    berge['rend_d_log'][0] = 0
    # Promedio de los rendimientos
    rend_p_mean = berge['rend_d_log'].mean()
    # Sacamos la diferencia de cada rendimiento de la operacion y del indice
    berge['dif'] = berge['rend_d_log'] - berge['rend_sp']

    df_mad.loc['information_r', ['valor', 'descripcion']] = [(rend_p_mean - prom_rend) / berge.dif.std(),
                                                             'Information Ratio']
    return df_mad


# -- ---------------------------------------------------- FUNCION: Disposition Effect -- #
# -- ------------------------------------------------------------------------------------ -- #
# -- Función para obtener evidencia sobre la presencia de sesgos cognitivos en un trader

def f_be_de(param_data):
    """

    Parameters
    ----------
    param_data: DataFarame con los historicos de las operaciones

    Returns
    -------
    Diccionario con las ocurrencias
    """
    # Operaciones en el cierre
    close = param_data.closetime
    # Operaciones en el open
    open_price = param_data.opentime
    # Tabla de los historicos con solo las ganadoras
    ganadoras = param_data[param_data.profit > 0]
    ganadoras.reset_index(inplace=True, drop=True)
    # Operaciones ganadoras en el cierre
    clo_p = ganadoras.closetime
    # Operaciones ganadoras en el open
    open_n = ganadoras.opentime

    # Encontrar las veces en que se pudo cumplir el sesgo
    ocurrencias = [[param_data.iloc[i, :] for i in range(len(param_data)) if open_price[i] < ganadoras['opentime'][j]
                    and close[i] > ganadoras['closetime'][j] or
                    ganadoras['opentime'][j] < open_price[i] < ganadoras['closetime'][j] < close[i]]
                   for j in range(len(ganadoras))]
    # Concatenar la ganadora con las que estaban abiertas y se deja la primera a la ganadora que es ancla
    concatenadas = [pd.concat([ganadoras.iloc[i, :], pd.concat(ocurrencias[i], axis=1)],
                              axis=1, sort=False, ignore_index=True).T
                    for i in range(len(ocurrencias)) if ocurrencias[i]]

    # Obtener los simbolos de las operaciones pero con el formato que la funcion require
    symbol = [[concatenadas[j]['symbol'][i].upper()[:3] + '_' + concatenadas[j]['symbol'][i].upper()[3:]
               for i in range(len(concatenadas[j]) - 1)] for j in range(len(concatenadas))]

    # Obtener los precios de los simbolos en el precio de cierre del ancla
    prec_close = [[f_precio((symbol[j][i + 1]), concatenadas[j]['closetime'][0])
                   for i in range(len(symbol[j]) - 1)] for j in range(len(symbol))]

    # Volvemos a concatenar estos precios en concatenadas
    conc_precios = [pd.concat([concatenadas[i], pd.concat([pd.DataFrame([0], columns=['priceclose']),
                                                           pd.DataFrame(prec_close[i], columns=['priceclose'])],
                                                          sort=False, ignore_index=True)], axis=1, sort=False)
                    for i in range(len(concatenadas))]
    ocur = []
    bb = 0
    # Se calcula el profit de cada operacion
    for i in range(len(conc_precios)):
        conc_precios[i]['Perdida flotate'] = (conc_precios[i]['priceclose'] - conc_precios[i]['openprice']) * \
                                             (conc_precios[i]['profit'] /
                                              (conc_precios[i]['closeprice'] - conc_precios[i]['openprice']))
    # Crear los diccionarios verficiando si la perdidas flotantes si fueron perdidas
    profits = []
    index = []
    for j in range(len(prec_close)):
        for i in range(len(prec_close[j])):
            if prec_close[j][i] < concatenadas[j]['openprice'][i + 1] and concatenadas[j]['type'][i + 1] == 'buy' \
                    or prec_close[j][i] > concatenadas[j]['openprice'][i + 1] \
                    and concatenadas[j]['type'][i + 1] == 'sell':
                profits.append((conc_precios[j]['Perdida flotate'][i + 1]))
                index.append(i + 1)
        if profits:
            bb += 1
            ind = profits.index(min(profits))
            x = round((conc_precios[j]['priceclose'][index[ind]] -
                       concatenadas[j]['openprice'][index[ind]]) *
                      ((concatenadas[j]['profit'][index[ind]]) /
                       (concatenadas[j]['closeprice'][index[ind]] -
                        concatenadas[j]['openprice'][index[ind]])), 2)
            ocur.append({'ocurrencia %d' % bb:
                             {'timestamp': concatenadas[j]['closetime'][0],
                              'operaciones':
                                  {'ganadora':
                                       {'instrumento': concatenadas[j]['symbol'][0],
                                        'sentido': concatenadas[j]['type'][0],
                                        'volumen': concatenadas[j]['size'][0],
                                        'capital_ganadora': concatenadas[j]['profit'][0],
                                        'capital_acm': concatenadas[j]['capital_acm'][0]},
                                   'perdedora':
                                       {'instrumento': concatenadas[j]['symbol'][index[ind]],
                                        'sentido': concatenadas[j]['type'][index[ind]],
                                        'volumen': concatenadas[j]['size'][index[ind]],
                                        'profit': concatenadas[j]['profit'][index[ind]],
                                        'capital_perdedora': x}},

                              'ratio_cp_capital_acm': round(abs(x / concatenadas[j]['capital_acm'][0]) * 100, 2),
                              'ratio_cg_capital_acm': round(abs(concatenadas[j]['profit'][0] /
                                                                concatenadas[j]['capital_acm'][0]) * 100, 2),
                              'ratio_cp_cg': round(abs(x / concatenadas[j]['profit'][0]), 2)}})

    # Calclar el ratio capital_ganadoras/capital_acm *100
    param_data['ratio_acu'] = 0
    param_data['ratio_acu'] = [(param_data['profit'][i] / 5000) * 100 if i == 0 else
                               (param_data['profit'][i] / param_data['capital_acm'][i - 1]) * 100
                               for i in range(len(param_data['profit']))]
    # Creamos DF para ver las caracteristicas del sesgo
    df_ocur = pd.DataFrame(columns=['ocurrencias', 'status_quo', 'aversion_perdida', 'sensibilidad_decreciente'])
    res = pd.concat([pd.DataFrame([ocur[i - 1]['ocurrencia %d' % i]['ratio_cp_capital_acm'],
                                   ocur[i - 1]['ocurrencia %d' % i]['ratio_cg_capital_acm'],
                                   ocur[i - 1]['ocurrencia %d' % i]['ratio_cp_cg'],
                                   ocur[i - 1]['ocurrencia %d' % i]['operaciones']['ganadora']['capital_acm']])
                     for i in range(1, len(ocur) + 1)], axis=1).T
    b = pd.concat([res.iloc[0, :], res.iloc[len(res) - 1, :]], axis=1).T
    df_ocur['ocurrencias'] = [len(res)]
    df_ocur['status_quo'] = [len([1 for i in range(len(res)) if res.iloc[i, 0] < res.iloc[i, 1]]) / len(res)]
    df_ocur['aversion_perdida'] = [len([1 for i in range(len(res)) if res.iloc[i, 2] > 1.5]) / len(res)]
    if b.iloc[0, 3] < b.iloc[1, 3] and b.iloc[1, 2] > 1.5 and \
            b.iloc[0, 0] < b.iloc[1, 0] or b.iloc[0, 1] < b.iloc[1, 1]:
        df_ocur['sensibilidad_decreciente'] = 'Sí'
    else:
        df_ocur['sensibilidad_decreciente'] = 'No'

    return {'Ocurrencias': ocur, 'Caracteristicas': df_ocur}
