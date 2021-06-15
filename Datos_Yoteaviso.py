#
import pandas as pd
import numpy as np
data = pd.read_csv("precio-venta-deptos.csv")
dataframe = pd.DataFrame(data)


data_limpio= dataframe.loc[:,['barrio','precio_prom','año']]

data_validada = data_limpio[data_limpio.precio_prom.notna()]

validado3= data_validada[data_validada.año > 2018 ]


test = validado3.drop_duplicates(subset=['barrio'])
print(test)



