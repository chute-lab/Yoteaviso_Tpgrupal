
import requests
from bs4 import BeautifulSoup
import pyautogui as pg
import time
import webbrowser as web

from Api_Tpgrupal import consultar

# Inputs iniciales
print("\033[4m" "Bienvenido a YoTeAviso""\033[0m")
print("Yo te aviso te va a notificar cuando el producto que seleccionaste baje de precio")
nombre = str(input("Como es tu nombre? ", ))
link_cliente = str(input("Hola "+ nombre +", dejanos el link de Mercadolibre de la propiedad que te gusta:",))



# Api dolar Blue

url2 = "https://api-dolar-argentina.herokuapp.com/api/dolarblue"
r = requests.get(url2)
datos = r.json()
precio_dolar_compra = datos['compra']
precio_dolar_venta = datos['venta']
# print(precio_dolar_compra)
# print(precio_dolar_venta)
''' Aca estamos transformando de str a float el precio de el dolar para poder manipularlo'''
a= precio_dolar_compra
float(a)
dolar_compra_float = int(float(a))
b= precio_dolar_venta
float(b)
dolar_venta_float = int(float(b))

# _________________________

#Aca estamos trayendo el CSV con la info de los precio promedio por mt2
import pandas as pd

data = pd.read_csv("precio-venta-deptos.csv")
dataframe = pd.DataFrame(data)


data_limpio= dataframe.loc[:,['barrio','precio_prom','año']]

data_validada = data_limpio[data_limpio.precio_prom.notna()]
#Aca estamos filtrando para que nos muestre los valores mas actualizados (anio 2019)
validado3= data_validada[data_validada.año > 2018 ]
# Aca estamos sacando los barrios que estaban duplicados
test = validado3.drop_duplicates(subset=['barrio'])
#Aca estamos sacando el indice de las columnas, pq quedaba mal
sin_indice = test.set_index('barrio')




respuesta = str(input('Queres que te demos estadisticas de precios por m2 en CABA:' '\n' 'si/no' '\t'))

while respuesta == "si" :
    print("Yoteaviso te avisa.... Estos son los precios promedios(mt2) por barrios en CABA:", '\n', sin_indice, '\n')
    #Aca estamos llamando a nuestra Api propia
    urlpropia = "http://127.0.0.1:4000/consultas"
    ra = requests.get(urlpropia)
    datos_propios = ra.json()
    print(datos_propios)
    print("_________________________")

    break
else:
      pass



# Input de variables con excepciones

while True:
    try:
        precio_alerta = float(input("Cuando baje de que precio queres que te avisemos?"))
        if precio_alerta == float or precio_alerta > 0:
            break
        else:
            print('Valor no valido')
    except(TypeError, ValueError):
        print("El valor no es valido, introduzca un valor valido")

while True:
    try:
        whatsapp = "+54" + str(input("Dejame tu numero de whatsapp"))
        if (len(whatsapp) == 13):
            break
        else:
            print('Valor no valido')
    except len(whatsapp) != 13:
        print("El valor no es valido, no tiene 10 caracteres")
    except(TypeError, ValueError):
        print("El valor no es valido, introduzca un valor valido")



# Scarpping de la pagina web en busca del precio actual del producto seleccionado

url = requests.get(link_cliente)
#
soup = BeautifulSoup(url.content,"html.parser")
resultado = soup.find("span", {"class":"price-tag-fraction"}) #la posta



precioInicio_text = resultado.text
precioInicial = float(precioInicio_text)
# precioInicial = float()



'''Esto lo estamos haciendo en particular para meli pq el precio lo da en numeros con coma chicos'''
precioInicial = precioInicial * 1000
'''Aca estamos conviertiendo el precio que nos dio en cliente en pesos a dolares y lo redondemos a dos decimales'''
precio_whatsapp = round((precioInicial * dolar_venta_float),2)
'''Aca estamos pasando el precio del cliente convertido en dolares a str para poder concatenarlo en el mensaje de wapp'''
a2= precio_whatsapp
str(a2)
preciowappstr = str(a2)


# Scrapping para mandar mensaje de whatsapp

if precioInicial < precio_alerta:
    phone_no= whatsapp
    parsedMessage=("Hola " + nombre + ", soy Carla de Yo te aviso." '\n'"Tu auto bajo de precio, el precio en pesos es $"+ preciowappstr + " . No dudes mas, compralo YA!" '\n'+ link_cliente)
    web.open('https://web.whatsapp.com/send?phone='+phone_no+'&text='+parsedMessage)
    time.sleep(8)
    for i in range(2):
        pg.write('')
        pg.press('enter')
        print('Mensaje #'+str(i+1)+' enviado')
        pass
else:
 print("Por el momento no bajo del precio esperado")



# Insertar datos en base de datos (database, ppo)

import sqlite3

class busqueda():
    def grabar(self):
        conexion = sqlite3.connect("consultaprecios.db")
        cursor = conexion.cursor()
        cursor.execute("INSERT INTO tablaclientes VALUES (?,?,?,?)", (nombre, link_cliente, precio_alerta,whatsapp))
        conexion.commit()
pass

instancia = busqueda()
instancia.grabar()



# url_nuestra = http://127.0.0.1:4000//consultas









# Cosas para hacer
# Api propia
# - Barrio mas buscado dentro de la gente que nos consulto, lectura de archivos
# Polimorfismo y herencia, ecamsulamiento
# Github
# Uso de analisis de datos para decisiones de negocio






# ____________________________________________________________

# def getting_api_response(url2):
#     response = rq.get(url)
#     if response.status_code == 200:
#         print("Recibiendo datos exitosamente: {}".format(response))
#     else:
#         print("Error en recibir datos, response_status_code: {}".format(response))
#     response_json = response.json()
#     json_data = response_json["articles"]
#     for data in json_data:
#         print(data)
#     return




# Insert impitus in sql
# CREATE TABLE clientes (nombre     VARCHAR(100),link   VARCHAR(200), precio_alerta     VARCHAR(100)
# import sqlite3
# conexion = sqlite3.connect("consultaprecios.db")
# cursor = conexion.cursor()
# sentenciaSQL = "CREATE TABLE clientes2"
# sentenciaSQL = sentenciaSQL + "(nombre VARCHAR(100)"
# sentenciaSQL = sentenciaSQL + "(link VARCHAR(100)"
# cursor.execute(sentenciaSQL)
# conexion.commit()





# resultado = soup.find("span", {"class":"data-price"})
# resultado = soup.find("script", {"pricesData":[{"prices":[{"amount"}]}]}) #Este es para zonparop
# print(resultado)

# barrio = soup.find("div", {"class":"map-location"})
# print(soup)

# punct = string.punctuation
# for sinusd in resultado:
#     sinusd = resultado.replace("USD ", "")
# print(sinusd)























# if precioInicial < precio_alerta:
#     phone_no= whatsapp
#     parsedMessage="Bajo de precio"
#     web.open('https://web.whatsapp.com/send?phone='+phone_no+'&text='+parsedMessage)
#     time.sleep(8)
#     envio()
# else:
#     print("Por el momento no bajo del precio esperado")
#
# def envio():
#     pg.write('Bajo de precio')
#     pg.press('enter')
#     print('Mensaje enviado')
# pass








# import pyautogui as pg
# import time
# import webbrowser as web
# phone_no="+5491150163447"
# parsedMessage=""
# web.open('https://web.whatsapp.com/send?phone='+phone_no+'&text='+parsedMessage)
# time.sleep(8)
# for i in range(10):
#     pg.write('Que haces')
#     pg.press('enter')
#     print('Mensaje #'+str(i+1)+' enviado')
#     pass
# pg.alert('Bomba de mensajes finalizada')
