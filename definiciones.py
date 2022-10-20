from PyQt5 import QtCore, QtWidgets, QtGui
import numpy as np
import pickle
import json

# Obtener un arreglo n con cierto porcentaje de 1's


def obtenerCondicionInicial(numCeluas, porcentajeUnos):
    arr = np.zeros(numCeluas)
    contUnos = int((numCeluas*porcentajeUnos)/100)
    arr[:contUnos] = 1
    np.random.shuffle(arr)
    return arr


class Circular(list):

    def __init__(self, sequence=[]):
        super(Circular, self).__init__(sequence)
        self.position = 0

    def current(self):
        return self[self.position]

    def next(self, n=1):
        self.position = (self.position + n) % len(self)
        return self[self.position]

    def prev(self, n=1):
        return self.next(-n)


def mostrarDialogoOk(parent, mensaje):
    msg = QtWidgets.QMessageBox(parent)
    fuente = msg.font()
    fuente.setPointSize(12)
    msg.setFont(fuente)
    msg.setWindowIcon(QtGui.QIcon("./logoESCOM.png"))
    msg.setIcon(QtWidgets.QMessageBox.Information)
    msg.setText(mensaje)
    msg.setStandardButtons(QtWidgets.QMessageBox.Ok)
    msg.setWindowTitle("Ok")

    msg.exec_()


def mostrarDialogoError(parent, mensaje):
    msg = QtWidgets.QMessageBox(parent)
    msg.setWindowIcon(QtGui.QIcon("./logoESCOM.png"))
    fuente = msg.font()
    fuente.setPointSize(12)
    msg.setFont(fuente)
    msg.setIcon(QtWidgets.QMessageBox.Warning)
    msg.setText(mensaje)
    msg.setStandardButtons(QtWidgets.QMessageBox.Ok)
    msg.setWindowTitle("Error")

    msg.exec_()


class DialogoGuardarArchio(QtWidgets.QDialog):
    def __init__(self, parent, estadoInicial, regla, generaciones, color1, relleno1, color0, relleno0, tamCuadro):
        super().__init__(parent)
        self.dialog = QtWidgets.QFrame(self)
        self.setWindowIcon(QtGui.QIcon("./Icons/logoESCOM.png"))
        self.setWindowTitle("Save")
        self.dialog.setWindowTitle("Save initial condition")
        self.dialog.setWindowIcon(QtGui.QIcon('./Icons/guardar.png'))

        fuente = self.font()
        fuente.setPointSize(12)
        self.setFont(fuente)

        layoutDialog = QtWidgets.QVBoxLayout(self)
        btnsLayout = QtWidgets.QHBoxLayout()

        lblNombre = QtWidgets.QLabel("Enter the file name")
        txtNombre = QtWidgets.QLineEdit()

        btnGuardar = QtWidgets.QPushButton("Save")
        btnCancelar = QtWidgets.QPushButton("Cancel")

        lblNombre.setAlignment(QtCore.Qt.AlignCenter)

        layoutDialog.addWidget(lblNombre)
        layoutDialog.addWidget(txtNombre)
        layoutDialog.addLayout(btnsLayout)

        btnsLayout.addWidget(btnGuardar)
        btnsLayout.addWidget(btnCancelar)

        def guardarArchivo():
            texto = txtNombre.text()
            if len(texto) == 0:
                mostrarDialogoError(self, "Enter the file name")
                pass
            else:
                ruta = "./Guardado/"
                ruta += texto
                ruta += ".data"
                try:
                    data = {
                        "estadoInicial": estadoInicial,
                        "regla": regla,
                        "generaciones": generaciones,
                        "colorUno": color1,
                        "rellenoUno": relleno1,
                        "colorCero": color0,
                        "rellenoCero": relleno0,
                        "tamCuadro": tamCuadro
                    }
                    with open(ruta, 'w') as filehandle:
                        json.dump(data, filehandle)
                    msj = "File saved as: " + texto + ".data"
                    self.close()
                    mostrarDialogoOk(self, msj)
                except Exception as e:
                    print(e)
                    error = QtWidgets.QErrorMessage(self)
                    error.showMessage("Error saving the file")
                pass

        def cerrarVentana():
            self.close()

        btnGuardar.clicked.connect(guardarArchivo)
        btnCancelar.clicked.connect(cerrarVentana)


class DialogoImagen(QtWidgets.QDialog, QtGui.QImage):
    def __init__(self, parent, img):
        super().__init__(parent)
        self.dialog = QtWidgets.QFrame(self)
        self.setWindowIcon(QtGui.QIcon("./Icons/logoESCOM.png"))
        self.setWindowTitle("Save image")
        self.dialog.setWindowTitle("Save Image")
        self.dialog.setWindowIcon(QtGui.QIcon('./Icons/guardar.png'))

        fuente = self.font()
        fuente.setPointSize(12)
        self.setFont(fuente)

        layoutDialog = QtWidgets.QVBoxLayout(self)
        btnsLayout = QtWidgets.QHBoxLayout()

        lblNombre = QtWidgets.QLabel("Enter the image name")
        txtNombre = QtWidgets.QLineEdit()

        btnGuardar = QtWidgets.QPushButton("Save")
        btnCancelar = QtWidgets.QPushButton("Cancel")

        lblNombre.setAlignment(QtCore.Qt.AlignCenter)

        layoutDialog.addWidget(lblNombre)
        layoutDialog.addWidget(txtNombre)
        layoutDialog.addLayout(btnsLayout)

        btnsLayout.addWidget(btnGuardar)
        btnsLayout.addWidget(btnCancelar)

        def guardarImagen():
            texto = txtNombre.text()
            if len(texto) == 0:
                mostrarDialogoError(self, "Please, enter the image name")
            else:
                ruta = ".\\Imagenes\\"
                ruta += texto
                ruta += ".png"
                self.close()
                try:
                    img.save(ruta)
                    msj = "Image saved as: " + texto + ".png"
                    mostrarDialogoOk(self, msj)
                except:
                    error = QtWidgets.QErrorMessage(self)
                    error.showMessage("Error al guardar la imagen")

        def cerrarVentana():
            self.close()

        btnCancelar.clicked.connect(cerrarVentana)
        btnGuardar.clicked.connect(guardarImagen)

        self.resize(300, 100)
        self.dialog.resize(300, 100)
