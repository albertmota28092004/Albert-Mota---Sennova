import conexion as con
from model.usuario import Usuario

class UsuarioData():
    def login(self, usuario:Usuario):
        self.db = con.Conexion().conectar()
        self.cursor = self.db.cursor()
        res = self.cursor.execute("SELECT * FROM usuarios WHERE usuario='{}' AND clave='{}'".format(usuario._usuario, usuario._clave, usuario._nombre))
        fila = res.fetchone()
        if fila:
            usuario = Usuario(nombre=fila[1], usuario=fila[2])  
            self.cursor.close()
            self.db.close()
            return usuario      
        else:
            return None