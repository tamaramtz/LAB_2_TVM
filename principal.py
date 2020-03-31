# -- ------------------------------------------------------------------------------------ -- #
# # -- proyecto: Microestructura y Sistemas de Trading - Laboratorio 2 - Behavioral Finance
# # -- archivo: datos.py - datos generales para uso en el proyecto
# # -- mantiene: Tamara Mtz.
# # -- repositorio: https://github.com/tamaramtz/LAB_2_TVM.git
# # -- ------------------------------------------------------------------------------------ -- #

import funciones as fn

datos = fn.f_leer_archivo(param_archivo='archivo_tradeview_1.xlsx')
datos = fn.f_columnas_datos(param_data=datos)
datos_col = fn.f_columnas_pips(param_data=datos)
dt_stats = fn.f_estadisticas_ba(datos)
df_mad = fn.f_estadisticas_mad(datos)
