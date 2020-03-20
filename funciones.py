# -- ------------------------------------------------------------------------------------ -- #
# -- proyecto: Microestructura y Sistemas de Trading - Laboratorio 2 - Behavioral Finance
# -- archivo: datos.py - datos generales para uso en el proyecto
# -- mantiene: Tamara Mtz.
# -- repositorio: https://github.com/tamaramtz/LAB_2_TVM.git
# -- ------------------------------------------------------------------------------------ -- #
import pandas as pd
import numpy as np

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

def f_columnas_datos(param_data):
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

    """
    param_data['pip_size'] = 0
    for i in range(0, len(param_data['type'])):
        #(closeprice - openprice)*multiplicador
        #param_data['pip_size'] = np.zeros(len(param_data['type']))
        param_data['pip_size'] = param_data[param_data['type'] == 'sell']['openprice'] - \
                                 param_data[param_data['type'] == 'sell']['closeprice']
        param_data['pip_size'][param_data['type'] == 'buy'] = (param_data[param_data['type'] == 'buy']['closeprice'] - \
                               param_data[param_data['type'] == 'buy']['openprice'])
        param_data['profit_acm'] = param_data['profit'].cumsum()

    return param_data


def f_estadisticas_ba(param_data):
    """

    Parameters
    ----------
    param_data

    Returns
    -------
    dataFrame
    """
    df_ba = pd.DataFrame(index=['Ops totales', 'Ganadoras', 'Ganadoras_c', 'Ganadoras_v', 'Perdedoras', 'Perdedoras_c',
                                'Perdedoras_v', 'Media (Profit)', 'Media (Pips)', 'r_efectividad', 'r_proporcion',
                                'r_efectividad_c', 'r_efectividad_v'], columns=['valor', 'descripción'])
    df_ba.index.name = "medida"
    df_ba.loc['Ops totales', ['valor', 'descripcion']] = [len(param_data['order']),'Operaciones totales']
    df_ba.loc['Ganadoras', ['valor', 'descripcion']] = [len(param_data[param_data['pips_size']>=0]),
                                                          'Operaciones ganadoras']
    df_ba.loc['Ganadoras_c', ['valor', 'descripcion']] = [len(datos[(datos['type'] =='buy') &
                                                                    (datos['pips_acm'] >= 0)]),
                                                          'Operaciones ganadoras de compra']
    df_ba.loc['Ganadoras_v', ['valor', 'descripcion']] = [len(datos[(datos['type'] == 'sell') &
                                                                    (datos['pips_acm'] >= 0)]),
                                                          'Operaciones ganadoras de venta']








