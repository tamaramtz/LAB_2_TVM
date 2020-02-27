# -- ------------------------------------------------------------------------------------ -- #
# -- proyecto: Microestructura y Sistemas de Trading - Laboratorio 2 - Behavioral Finance
# -- archivo: datos.py - datos generales para uso en el proyecto
# -- mantiene: Tamara Mtz.
# -- repositorio: https://github.com/tamaramtz/LAB_2_TVM.git
# -- ------------------------------------------------------------------------------------ -- #
import pandas as pd

# -- ------------------------------------------------------------------------------------ -- #

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
# -- ------------------------------------------------------------------------------------ -- #
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