from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_mysqldb import MySQL
import random

app = Flask(__name__)
CORS(app)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'banco'
 
mysql = MySQL(app)

@app.route('/api/get-cuenta/',  methods = ['POST'])
def get_cuenta():
    res = request.get_json()
    cedula = str(res["cedula"])
    #print(cedula)
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT nombres, apellidos, email, telefono, numero, tipo, saldo FROM clientes, cuentas WHERE clientes.cedula = %s AND clientes.cedula = cuentas.cedula", [cedula]) 
    rows = cursor.fetchall()
    for row in rows:
        print(row)
    return jsonify(rows)

@app.route('/api/set-cuenta/', methods = ['POST'])
def save_results():
    res = request.get_json()
    cedula = res["cedula"]
    nombres = res['nombres']
    apellidos = res['apellidos']
    email = res['email']
    direccion = res['direccion']
    telefono = res['telefono']
    tipo = res['tipo']
    #print(res)
    numero = random.randint(1800000000, 1900000000)
    #print(numero)
    cursor = mysql.connection.cursor()
    cursor.execute("INSERT INTO clientes VALUES(%s, %s, %s, %s, %s, %s)", [cedula, nombres, apellidos, email, direccion, telefono])
    cursor.execute("SELECT numero FROM cuentas WHERE numero = %s", [numero])
    rows = cursor.fetchall()
    if len(rows) == 0:
        print("Holasasas")
        cursor.execute("INSERT INTO cuentas VALUES(%s, %s, %s, %s)", [numero, tipo, 0.00, cedula])
    mysql.connection.commit()
    cursor.close()
    return "Cuenta creada"

@app.route('/api/transacciones/', methods = ['POST'])
def transacciones():
    res = request.get_json()
    num_cuenta_ori = str(res['num_cuenta_ori'])
    num_cuenta_dest = res['num_cuenta_dest']
    monto = float(res['monto'])
    fecha = res['fecha']
    #print(res)
    cursor = mysql.connection.cursor()
    cursor.execute("INSERT INTO transacciones VALUES(null, %s, %s, %s, %s)", [num_cuenta_ori, num_cuenta_dest, monto, fecha])
    cursor.execute("SELECT saldo FROM cuentas WHERE numero = %s", [num_cuenta_ori])
    rows = cursor.fetchall()
    if rows[0][0] >= monto:
        cursor.execute("UPDATE cuentas SET saldo = (saldo - %s) WHERE numero = %s", [monto, num_cuenta_ori])
        cursor.execute("UPDATE cuentas SET saldo = (saldo + %s) WHERE numero = %s", [monto, num_cuenta_dest])
    else:
        return "Saldo insuficiente"
    mysql.connection.commit()
    cursor.close()
    return "Realizada"

@app.route('/api/solicitudes/', methods = ['POST'])
def solicitudes():
    res = request.get_json()
    cedula = res['cedula']
    nombres = res['nombres']
    apellidos = res['apellidos']
    email = res['email']
    telefono = res['telefono']
    monto = res['monto']
    uso = res['uso']
    tasa = res['tasa']
    #print(res)
    cursor = mysql.connection.cursor()
    cursor.execute("INSERT INTO sol_creditos VALUES(null, %s, %s, %s, %s, %s, %s, %s, %s)", [cedula, nombres, apellidos, email, telefono, monto, uso, tasa])
    mysql.connection.commit()
    cursor.close()
    return "Guardado"

if __name__ == '__main__':
    app.run(debug=True, port=8000)
