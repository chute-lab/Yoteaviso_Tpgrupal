from flask import Flask, jsonify
from statistics import mean
app = Flask(__name__)



@app.route('/consultas', methods = ['GET'])
def consultar():
    import sqlite3
    conexion = sqlite3.connect("consultaprecios.db")
    cursor = conexion.cursor()
    sentenciaSQL = cursor.execute("SELECT precioalerta FROM tablaclientes")
    resultado = cursor.fetchall()
    for resultadox in resultado:
        print(resultadox)
    conexion.commit()
    return jsonify("Lo minimo que la gente esta dispuesta a pagar por una propiedad es:", min(resultado))





if __name__ == '__main__':
    app.run(debug= True, port=4000)







