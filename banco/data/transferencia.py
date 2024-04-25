# import conexion as con
# from model.movimientos import Transferencia
# from datetime import datetime

# class TransferenciaData():

#     def __init__(self):
#         try: 
#             self.db = con.Conexion().conectar()
#             self.cursor = self.db.cursor()
#             sql_create_transferencias = """CREATE TABLE IF NOT EXISTS transferencias(
#             id INTEGER PRIMARY KEY AUTOINCREMENT,
#             monto NUMERIC,  
#             tipo TEXT, 
#             documento TEXT,
#             internacional BOOLEAN,
#             dolares BOOLEAN,
#             fecha_registro DATETIME,
#             verificado BOOLEAN,
#             motivo TEXT)"""
#             print("Creando tabla transferencias...")
#             self.cursor.execute(sql_create_transferencias)
#             self.db.commit()
#             self.cursor.close()
#             self.db.close()
#             print("Tabla transferencias creada")
#         except Exception as ex:
#             print("Tabla transferencias error", ex)

#     def registrar(self, info:Transferencia):
#         fecha = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
#         print("Conectando a la base de datos...")
#         self.db = con.Conexion().conectar()
#         self.cursor = self.db.cursor()
#         self.cursor.execute("""
#         INSERT INTO transferencias VALUES(null,'{}', '{}', '{}', '{}', '{}', '{}', '{}','{}')
#         """.format(info._monto, info._tipo, info._documento, info._internacional, info._dolares, fecha, False, info._motivo))
#         self.db.commit()
#         if self.cursor.rowcount==1:
#             return True
#         else:
#             return False
        
import conexion as con
from model.movimientos import Transferencia

class TransferenciaData():

    def __init__(self) -> None:
        try:
            sql_create_transferencias = """ CREATE TABLE IF NOT EXISTS transferencias(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            monto NUMERIC,  
            tipo TEXT,
            documento TEXT, 
            internacional BOOLEAN, 
            dolares BOOLEAN, 
            fecha_registro DATETIME, 
            verificado BOOLEAN DEFAULT 'false', 
            motivo TEXT)"""
            cur = self.con.cursor()
            cur.execute(sql_create_transferencias)
            cur.close()
        except Exception as ex:
            print("Tabla transferencia error", ex)

    def registrar(self, info:Transferencia):
        self.db = con.Conexion().conectar()
        self.cursor = self.db.cursor()
        self.cursor.execute("".format(usuario._usuario, usuario._clave, usuario._nombre))
        fila = res.fetchone()
        if fila:
            usuario = Usuario(nombre=fila[1], usuario=fila[2])  
            self.cursor.close()
            self.db.close()
            return usuario      
        else:
            return None