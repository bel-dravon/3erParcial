from flask import Flask, jsonify
from decouple import config
from modelo.modeloProducto import ProductoModel
from modelo.modeloEmpleado import EmpleadoModel
app = Flask(__name__)	


@app.route('/')
def hello_world():
    return 'Hola Mundo!'

""" EMPLEADO """
@app.route('/empleado',methods=['GET'])
def listar_empleados():
    emp = EmpleadoModel.listar_empleado()
    return emp

@app.route('/empleado',methods=['POST'])
def insertar_empleados():
    emp = EmpleadoModel.insertar_empleado()
    return emp

@app.route('/empleado:<codigo>',methods=['PUT'])
def modificar_empleados(codigo):
    emp = EmpleadoModel.modificar_empleado(codigo)
    return emp

""" PRODUCTO """
@app.route('/producto',methods=['GET'])
def listar_productos():
    pro = ProductoModel.listar_producto()
    return pro

@app.route('/producto',methods=['POST'])
def crear_productos():
    pro = ProductoModel.insertar_producto()
    return pro

@app.route('/producto:<codigo>',methods=['PUT'])
def modificar_productos(codigo):
    pro = ProductoModel.modificar_producto(codigo)
    return pro

""" REPORTE """
@app.route('/reporte', methods=['GET'])
def reortes():
    mul = ProductoModel.reporte()
    return mul

if __name__ == '__main__':
    app.run(host='0.0.0.0') 