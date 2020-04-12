# -- ------------------------------------------------------------------------------------ -- #
# # -- proyecto: Microestructura y Sistemas de Trading - Laboratorio 2 - Behavioral Finance
# # -- archivo: datos.py - datos generales para uso en el proyecto
# # -- mantiene: Tamara Mtz.
# # -- repositorio: https://github.com/tamaramtz/LAB_2_TVM.git
# # -- ------------------------------------------------------------------------------------ -- #

import funciones as fn
import visualizaciones as vn

datos = fn.f_leer_archivo(param_archivo='archivo_tradeview_1.xlsx')
datos = fn.f_columnas_tiempos(datos)
datos = fn.f_columnas_pips(datos)
datos = fn.f_capital_acm(datos)
dt_stats = fn.f_estadisticas_ba(datos)
pl_stats = vn.plot_ranking(dt_stats)
profit_d = fn.f_profit_diario(datos)
df_mad = fn.f_estadisticas_mad(datos)
ddu = vn.plot_profit_diario(profit_d)
ocur = fn.f_be_de(datos)
pl_ocur = vn.plot_de(ocur)
