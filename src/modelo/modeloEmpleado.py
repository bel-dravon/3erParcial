from flask import jsonify, request
from modelo.coneccion import db_connection

class EmpleadoModel():
    
    @classmethod
    def listar_empleado(self):
        try:
            conn = db_connection()
            cur = conn.cursor()
            cur.execute("""select * from empleados""")
            datos = cur.fetchall()
            empleados = []
            for fila in datos:
                empleado = {
                    'ci':fila[0],
                    'nombre':fila[1],
                    'direccion':fila[2],
                    'fecha_nac':fila[3],
                    'procendencia':fila[4]
                }
                empleados.append(empleado)
            conn.close()
            return jsonify({'empleado': empleados,'mensaje':"Empleados listados",'exito': True})
        except Exception as ex:
            return jsonify({'mensaje':"ERROR", 'exito': False})
        
    def buscar_empleado(codigo):
        try:
            conn = db_connection()
            cur = conn.cursor()
            cur.execute("""select * from empleados where ci =%s""",(codigo,))
            datos = cur.fetchone()
            conn.close()
            if datos is not None:
                empleado = {'ci':datos[0],
                        'nombre':datos[1],
                        'direccion':datos[2],
                        'fecha_nac':datos[3],
                        'procedencia':datos[4]}
                return empleado
            else:
                return None
        except Exception as ex:
            return ex

        
    @classmethod
    def insertar_empleado(self):
        try:
            empleado = self.buscar_empleado(request.json['ci'])
            if empleado is not None:
                return jsonify({'mensaje':"El ci del empleado ya existe", 'exito': True})
            else:
                conn = db_connection()
                cur = conn.cursor()
                cur.execute('insert into empleados values(%s,%s,%s,%s,%s)',
                            (request.json['ci'],request.json['nombre'],request.json['direccion'],request.json['fecha_nac'],request.json['procedencia']))
                conn.commit()
                conn.close()
                return jsonify({'mensaje':'Empleado insertado', 'exito': True})
        except Exception as ex:
            return jsonify({'mensaje':"ERROR", 'exito': False})
    
    @classmethod
    def modificar_empleado(self,codigo):
        try:
            empleado = self.buscar_empleado(codigo)
            if empleado is not None:
                conn = db_connection()
                cur = conn.cursor()
                cur.execute("""UPDATE empleados SET nombre=%s, direccion=%s, fecha_nac=%s, procedencia=%s WHERE ci=%s""",
                    (request.json['nombre'],request.json['direccion'],request.json['fecha_nac'],request.json['procedencia'],codigo))
                conn.commit()
                conn.close()
                return jsonify({'mensaje': "Empleado modificado.",'exito': True})
            else:
                return jsonify({'mensaje': "Empleado no encontrado.", 'exito': False})
        except Exception as ex:
                return jsonify({'mensaje': "Error", 'exito': False})
        
