from flask import Flask, render_template, request
import getrut
import mysql.connector
import json

def getrows(rut):
    cnx = mysql.connector.connect(user='seerk', password='',
                                  host='mysql.server',
                                  database='seerk$rutdata')
    cursor = cnx.cursor()

    get_range = ("SELECT data FROM data WHERE rut = "+str(rut))

    cursor.execute(get_range)
    row = cursor.fetchone()
    cursor.close()
    cnx.close()
    array=json.loads(row[0])
    return array

def digito_verificador(rut):
    value = 11 - sum([ int(a)*int(b)  for a,b in zip(str(rut).zfill(8), '32765432')])%11
    return {10: 'K', 11: '0'}.get(value, str(value))

app = Flask(__name__)

@app.route('/')
def hello_world():
    if (request.args.get('rut')==None) or (request.args.get('rut')==""):
        data="false"
        rut=0
    else:
        rut=str(request.args.get('rut'))
        rut=rut+"-"+str(digito_verificador(rut))
        data=getrows(request.args.get('rut'))
    return render_template('layout.html', data=data, rut=rut)
