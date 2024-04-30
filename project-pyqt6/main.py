import sys
from PyQt5.QtGui import QMouseEvent
from PyQt5.QtWidgets import QApplication, QMainWindow, QHeaderView
from PyQt5.QtCore import QPropertyAnimation, QEasingCurve
from PyQt5 import QtCore, QtWidgets
from PyQt5.uic import loadUi 
from conexion_sqlite import Comunicacion

class VentanaPrincipal(QMainWindow):
    def __init__(self):
        super(VentanaPrincipal, self).__init__()
        loadUi('diseno.ui', self)

        self.bt_menu.clicked.connect(self.mover_menu)
        # Clase comunicación sqlite
        self.base_datos = Comunicacion()
        # self.Id = str()

        # Ocultamos los botones
        self.bt_restaurar.hide()
        # Botones
        self.bt_refrescar.clicked.connect(self.mostrar_productos)
        self.bt_registrar_tabla.clicked.connect(self.registrar_productos)
        self.bt_eliminar_tabla.clicked.connect(self.eliminar_productos)
        self.bt_actualizar_tabla.clicked.connect(self.editar_productos)
        self.bt_buscar_actualizar.clicked.connect(self.buscar_por_nombre_actualiza)
        self.bt_buscar_eliminar.clicked.connect(self.buscar_por_nombre_eliminar)
        
        # Control barra de títulos
        self.bt_minimizar.clicked.connect(self.control_bt_minimizar)
        self.bt_restaurar.clicked.connect(self.control_bt_normal)
        self.bt_maximizar.clicked.connect(self.control_bt_maximizar)
        self.bt_cerrar.clicked.connect(lambda: self.close())

        # Eliminar barra y de título - opacidad
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        self.setWindowOpacity(1)

        # SizeGrip
        self.gripSize = 10
        self.grip = QtWidgets.QSizeGrip(self)
        self.grip.resize(self.gripSize, self.gripSize)

        # Mover ventana
        self.frame_superior.mouseMoveEvent = self.mover_ventana

        # Conexión botones
        self.bt_datos.clicked.connect(lambda: self.stackedWidget.setCurrentWidget(self.page_datos))
        self.bt_registrar.clicked.connect(lambda: self.stackedWidget.setCurrentWidget(self.page_registrar))
        self.bt_actualizar.clicked.connect(lambda: self.stackedWidget.setCurrentWidget(self.page_actualizar))
        self.bt_eliminar.clicked.connect(lambda: self.stackedWidget.setCurrentWidget(self.page_eliminar))
        self.bt_ajustes.clicked.connect(lambda: self.stackedWidget.setCurrentWidget(self.page_ajustes))

        # Ancho de columna adaptable
        self.tabla_eliminar.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tabla_productos.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

    def control_bt_minimizar(self):
        self.showMinimized()

    def control_bt_normal(self):
        self.showNormal()
        self.bt_restaurar.hide()
        self.bt_maximizar.show()

    def control_bt_maximizar(self):
        self.showMaximized()
        self.bt_maximizar.hide()
        self.bt_restaurar.show()

    # SizeGrip
    def resizeEvent(self, event):
        rect = self.rect()
        self.grip.move(rect.right() - self.gripSize, rect.bottom() - self.gripSize)

    # Mover ventana
    def mousePressEvent(self, event):
        self.click_position = event.globalPos()

    def mover_ventana(self, event):
        if self.isMaximized() == False:
            if event.buttons() == QtCore.Qt.LeftButton:
                self.move(self.pos() + event.globalPos() - self.click_position)
                self.click_position = event.globalPos()
                event.accept()
        elif event.globalPos().y()<=10:
            self.showMaximized()
            self.bt_maximizar.hide()
            self.bt_restaurar.show()
        else:
            self.showNormal()
            self.bt_restaurar.hide()
            self.bt_maximizar.show()

    def mover_menu(self):
        if True:
            width = self.frame_control.width()
            normal = 0
            if width == 0:
                extender = 200
            else:
                extender = normal
            self.animacion = QPropertyAnimation(self.frame_control, b'minimumWidth')
            self.animacion.setDuration(300)
            self.animacion.setStartValue(width)
            self.animacion.setEndValue(extender)
            self.animacion.setEasingCurve(QtCore.QEasingCurve.InOutQuart)
            self.animacion.start()
    
    # Configuración página base de datos
    def mostrar_productos(self):
        datos = self.base_datos.mostrar_productos()
        i = len(datos)
        self.tabla_productos.setRowCount(i)
        tablerow = 0
        for row in datos:
            self.Id = row[0]
            self.tabla_productos.setItem(tablerow, 0, QtWidgets.QTableWidgetItem(row[1]))
            self.tabla_productos.setItem(tablerow, 1, QtWidgets.QTableWidgetItem(row[2]))
            self.tabla_productos.setItem(tablerow, 2, QtWidgets.QTableWidgetItem(row[3]))
            self.tabla_productos.setItem(tablerow, 3, QtWidgets.QTableWidgetItem(row[4]))
            self.tabla_productos.setItem(tablerow, 4, QtWidgets.QTableWidgetItem(row[5]))
            tablerow += 1
            self.signal_actualizar.setText("")
            self.signal_registrar.setText("")
            self.signal_eliminar.setText("")

    def registrar_productos(self):
        codigo = self.reg_codigo.text().upper()
        nombre = self.reg_nombre.text().upper()
        modelo = self.reg_modelo.text().upper()
        precio = self.reg_precio.text().upper()
        cantidad = self.reg_cantidad.text().upper()
        if codigo != '' and nombre != '' and modelo != '' and precio != '' and cantidad != '':
            self.base_datos.inserta_producto(codigo, nombre, modelo, precio, cantidad)
            self.signal_registrar.setText('Productos registrados!')
            self.reg_codigo.clear()
            self.reg_nombre.clear()
            self.reg_modelo.clear()
            self.reg_precio.clear()
            self.reg_cantidad.clear()
        else:
            self.signal_registrar.setText('Hay espacios vacíos...')

    def buscar_por_nombre_actualiza(self):
        id_producto = self.actualizar_buscar.text().upper()
        id_producto = str("'" + id_producto + "'")
        self.producto = self.base_datos.busca_producto(id_producto)
        if len(self.producto) != 0:
            self.Id = self.producto[0][0]
            self.act_codigo.setText(self.producto[0][1])
            self.act_nombre.setText(self.producto[0][2])
            self.act_modelo.setText(self.producto[0][3])
            self.act_precio.setText(self.producto[0][4])
            self.act_cantidad.setText(self.producto[0][5])
        else:
            self.signal_actualizar.setText("No existe...")

    def editar_productos(self):
        if self.producto != '':
            codigo = self.act_codigo.text().upper()
            nombre = self.act_nombre.text().upper()
            modelo = self.act_modelo.text().upper()
            precio = self.act_precio.text().upper()
            cantidad = self.act_cantidad.text().upper()
            act = self.base_datos.actualiza_productos(self.Id, codigo, nombre, modelo, precio, cantidad)
            if act == 1:
                self.signal_actualizar.setText("Actualizado!")
                self.act_codigo.clear()
                self.act_nombre.clear()
                self.act_modelo.clear()
                self.act_precio.clear()
                self.act_cantidad.clear()
                self.actualizar_buscar.setText('')
            elif act == 0:
                self.signal_actualizar.setText("Error...")
            else:
                self.signal_actualizar.setText("Incorrecto...")

    def buscar_por_nombre_eliminar(self):
        nombre_producto = self.eliminar_buscar.text().upper()
        nombre_producto = str("'" + nombre_producto + "'")
        producto = self.base_datos.busca_producto(nombre_producto)
        self.tabla_eliminar.setRowCount(len(producto))

        if len(producto) == 0:
            self.signal_eliminar.setText("No existe...")
        else:
            self.signal_eliminar.setText("Producto seleccionado!")
        tablerow = 0
        for row in producto:
            self.producto_a_borrar = row[2]
            self.tabla_eliminar.setItem(tablerow, 0, QtWidgets.QTableWidgetItem(row[1]))
            self.tabla_eliminar.setItem(tablerow, 1, QtWidgets.QTableWidgetItem(row[2]))
            self.tabla_eliminar.setItem(tablerow, 2, QtWidgets.QTableWidgetItem(row[3]))
            self.tabla_eliminar.setItem(tablerow, 3, QtWidgets.QTableWidgetItem(row[4]))
            self.tabla_eliminar.setItem(tablerow, 4, QtWidgets.QTableWidgetItem(row[5]))
            tablerow += 1
        
    def eliminar_productos(self):
        self.row_flag = self.tabla_eliminar.currentRow()
        if self.row_flag == 0:
            self.tabla_eliminar.removeRow(0)
            self.base_datos.elimina_productos("'" + self.producto_a_borrar + "'")
            self.signal_eliminar.setText("Producto eliminado!")
            self.eliminar_buscar.setText('')

if __name__ == "__main__":
    app = QApplication(sys.argv)
    mi_app = VentanaPrincipal()
    mi_app.show()
    sys.exit(app.exec())



