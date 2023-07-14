from flask import jsonify, request
from modelo.coneccion import db_connection
from modelo.modeloEmpleado import EmpleadoModel

def buscar_producto(codigo):
        try:
            conn = db_connection()
            cur = conn.cursor()
            cur.execute("""select * from empleados where id_Producto =%s""",(codigo,))
            datos = cur.fetchone()
            conn.close()
            if datos != None:
                cafe = {
                    'id_Producto':datos[0],
                    'nombre':datos[1],
                    'descripcion':datos[1],
                    'precio':datos[3]
                }
                return cafe
            else:
                return None
        except Exception as ex:
            return ex
        
class ProductoModel():

    @classmethod
    def listar_producto(self):
        try:
            conn = db_connection()
            cur = conn.cursor()
            cur.execute("""select * from productos""")
            print(cur)
            datos = cur.fetchall()
            cafes = []
            for fila in datos:
                cafe = {
                    'id_producto':fila[0],
                    'nombre':fila[1],
                    'descripcion':fila[2],
                    'precio':fila[3],
                    'ci_e':fila[4]
                }
                cafes.append(cafe)
            conn.close()
            return jsonify({'cafes': cafes,'mensaje':"Productos listados",'exito': True})
        except Exception as ex:
            return jsonify({'mensaje':"ERROR", 'exito': False})
        
    @classmethod
    def insertar_producto(self):
        try:
            cafe = buscar_producto(request.json['ci'])            
            if cafe is not None:
                return jsonify({'mensaje':"El producto ya existe",'exito': True})
            else:
                ci = EmpleadoModel.buscar_empleado(request.json['ci'])            
                if ci is not None:
                    conn = db_connection()
                    cur = conn.cursor()
                    cur.execute('insert into productos values(%s,%s,%s,%s,%s)',
                                request.json['id_Producto'],request.json['nombre'],request.json['descripcion'],request.json['precio'],request.json['ci_e'])
                    conn.commit()
                    conn.close()
                    return jsonify({'mensaje':"Producto insertado", 'exito': True}) 
                else:
                    return jsonify({'mensaje':"El empleado no existe",'exito': False})   
        except Exception as ex:
            return jsonify({'mensaje':"ERROR", 'exito': False})
        
    @classmethod
    def modificar_producto(self,codigo):
        try:
            cafe = buscar_producto(codigo)
            if cafe is not None:
                conn = db_connection()
                cur = conn.cursor()
                cur.execute("""UPDATE productos SET nombre=%s, descripcion=%s, precio=%s, ci_e=%s WHERE id_Producto=%s""",
                    (request.json['nombre'],request.json['descripcion'],request.json['precio'],request.json['ci_es'],codigo))
                conn.commit()
                conn.close()
                return jsonify({'mensaje': "Producto modificado.", 'exito': True})
            else:
                return jsonify({'mensaje': "Producto no encontrado.", 'exito': False})
        except Exception as ex:
                return jsonify({'mensaje': "Error", 'exito': False})
        
    @classmethod
    def reporte():
        try:
            conn = db_connection()
            cur = conn.cursor()
            cur.execute("""select productos.nombre as cafe, count(empleados.nombre) as empleados from productos join empleados on productos.ci_e = empleados.ci group by productos.nombre""") 
            datos = cur.fetchall()
            cafes = []
            for fila in datos:
                cafe = {
                    'cafe':fila[0],
                    'empleado':fila[1]
                }
                cafes.append(cafe)
            conn.close()
            return jsonify({'cafes': cafes,'mensaje':"Cantidad de empleados que vendieron",'exito': True})      
        except Exception as ex:
            return jsonify({'mensaje': "Error", 'exito': False})


