from hilos import *
import json
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
import sys
import random
import os

from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QPainter, QColor, QFont, QImage
from definiciones import *
from random import randint
from expresionesRegulares import *

import numpy as np
import matplotlib
matplotlib.use('Qt5Agg')


vista = 0


class MyWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        # Layout principal
        vbox_princial = QVBoxLayout(self)
        hbox = QHBoxLayout()

        self.setWindowTitle("Elementary Cellular Automaton Simulator - IPC")
        self.setWindowIcon(QtGui.QIcon('./Icons/logoESCOM.png'))

        # Tamaño de cuadro
        self.tamCuadro = 10

        # desplazamineto
        self.desplazamiento = self.tamCuadro
        self.desplzamientoy = self.tamCuadro

        # Colores
        self.colorUno = QColor(0, 0, 0)
        self.rellenoUno = True

        self.colorDos = QColor(255, 255, 255)
        self.rellenoDos = False

        self.estadoInicial = []

        # Arreglo de puntos
        self.puntos = []

        # Munu
        menu = QMenuBar()
        archivo = menu.addMenu("File")
        colores = menu.addMenu("Colors")
        tipoDeGrafica = menu.addMenu("Graph type")

        menu.addMenu(archivo)
        menu.addMenu(colores)
        menu.addMenu(tipoDeGrafica)

        self.banderaGrafica = 0
        # Elementos para el menu de grafica
        grafica_densidad = QtWidgets.QAction("Density", menu)
        grafica_media = QtWidgets.QAction("Average", menu)
        grafica_varianza = QtWidgets.QAction("Variance", menu)

        grafica_densidad.setIcon(QtGui.QIcon('./Icons/si.png'))
        grafica_media.setIcon(QtGui.QIcon('./Icons/no.png'))
        grafica_varianza.setIcon(QtGui.QIcon('./Icons/no.png'))

        # Elemenetos menu Archivo
        guardar = QtWidgets.QAction("Save", menu)
        guardar.setIcon(QtGui.QIcon('./Icons/guardar.png'))

        cargar = QtWidgets.QAction("Load", menu)
        cargar.setIcon(QtGui.QIcon('./Icons/cargar.png'))

        # Elemenetos menu Colores
        cambiarColorUno = QtWidgets.QAction("Change 1 state color", menu)
        activarRellenoUno = QtWidgets.QAction("Fill 1's", menu)
        cambiarColorCero = QtWidgets.QAction("Change 0 state color", menu)
        activarRellenoDos = QtWidgets.QAction("Fill 0's", menu)

        # Agregando elementos a toolbar grafica
        tipoDeGrafica.addAction(grafica_densidad)
        tipoDeGrafica.addAction(grafica_media)
        tipoDeGrafica.addAction(grafica_varianza)

        # Agregar elemenetos a toolbar
        colores.addAction(cambiarColorUno)
        colores.addSeparator()
        colores.addAction(activarRellenoUno)
        colores.addSeparator()
        colores.addAction(cambiarColorCero)
        colores.addSeparator()
        colores.addAction(activarRellenoDos)
        archivo.addAction(guardar)
        archivo.addSeparator()
        archivo.addAction(cargar)

        activarRellenoUno.setIcon(QtGui.QIcon('./Icons/si.png'))
        activarRellenoDos.setIcon(QtGui.QIcon('./Icons/no.png'))

        # Agregar Icono al color
        auxColor1 = QtGui.QPixmap(100, 100)
        auxColor1.fill(self.colorUno)
        iconoColor1 = QtGui.QIcon(auxColor1)

        auxColor2 = QtGui.QPixmap(100, 100)
        auxColor2.fill(self.colorDos)
        iconoColor2 = QtGui.QIcon(auxColor2)

        cambiarColorUno.setIcon(iconoColor1)
        cambiarColorCero.setIcon(iconoColor2)

        # accion par los tipos de graficas
        def selec_graficaDensidad():
            self.banderaGrafica = 0
            grafica_densidad.setIcon(QtGui.QIcon('./Icons/si.png'))
            grafica_media.setIcon(QtGui.QIcon('./Icons/no.png'))
            grafica_varianza.setIcon(QtGui.QIcon('./Icons/no.png'))

        def selec_graficaMedia():
            self.banderaGrafica = 1
            grafica_densidad.setIcon(QtGui.QIcon('./Icons/no.png'))
            grafica_media.setIcon(QtGui.QIcon('./Icons/si.png'))
            grafica_varianza.setIcon(QtGui.QIcon('./Icons/no.png'))

        def selec_graficaVarianza():
            self.banderaGrafica = 2
            grafica_densidad.setIcon(QtGui.QIcon('./Icons/no.png'))
            grafica_media.setIcon(QtGui.QIcon('./Icons/no.png'))
            grafica_varianza.setIcon(QtGui.QIcon('./Icons/si.png'))

        # Toggle para el relleno
        def toggleRellenoUno():
            if self.rellenoUno:
                self.rellenoUno = False
                activarRellenoUno.setIcon(QtGui.QIcon('./Icons/no.png'))
            else:
                self.rellenoUno = True
                activarRellenoUno.setIcon(QtGui.QIcon('./Icons/si.png'))

        def toggleRellenoDos():
            if self.rellenoDos:
                self.rellenoDos = False
                activarRellenoDos.setIcon(QtGui.QIcon('./Icons/no.png'))
            else:
                self.rellenoDos = True
                activarRellenoDos.setIcon(QtGui.QIcon('./Icons/si.png'))

        def abrirColorPickerUno():
            self.colorUno = QColorDialog().getColor()
            auxColor1 = QtGui.QPixmap(100, 100)
            auxColor1.fill(self.colorUno)
            iconoColor1 = QtGui.QIcon(auxColor1)
            cambiarColorUno.setIcon(iconoColor1)
            pass

        def abrirColorPickerDos():
            self.colorDos = QColorDialog().getColor()
            auxColor2 = QtGui.QPixmap(100, 100)
            auxColor2.fill(self.colorDos)
            iconoColor2 = QtGui.QIcon(auxColor2)
            cambiarColorCero.setIcon(iconoColor2)
            pass

        # Señales para el tipo de grafica
        grafica_densidad.triggered.connect(selec_graficaDensidad)
        grafica_media.triggered.connect(selec_graficaMedia)
        grafica_varianza.triggered.connect(selec_graficaVarianza)

        # Señales para conectar los eventos
        cambiarColorUno.triggered.connect(abrirColorPickerUno)
        cambiarColorCero.triggered.connect(abrirColorPickerDos)
        activarRellenoUno.triggered.connect(toggleRellenoUno)
        activarRellenoDos.triggered.connect(toggleRellenoDos)

        # Barra de herramientas
        toolbar = QToolBar()
        lblTamCelula = QLabel("Cell size")

        lblVelocidad = QLabel("    Simulation sleep time: ")
        lblVelocidad2 = QLabel(" 0.15s")

        spinBox = QSpinBox()
        spinBox.setValue(int(self.tamCuadro))
        spinBox.setMinimum(0)
        spinBox.setMaximum(50)
        spinBox.setSingleStep(2)
        self.valActual = spinBox.value()
        fuentelblCelula = lblTamCelula.font()
        fuentelblCelula.setPointSize(12)
        lblTamCelula.setFont(fuentelblCelula)
        toolbar.addWidget(lblTamCelula)
        toolbar.addWidget(spinBox)

        toolbar.addWidget(lblVelocidad)
        toolbar.addWidget(lblVelocidad2)

        # Elementos para expresión regular
        toolbar.addWidget(
            QLabel("  Input regular expression to generate initial state: "))
        txtRegex = QLineEdit()
        txtRegex.setFixedWidth(400)
        btnRegex = QPushButton("Generate")
        btnRegex.setToolTip("Generate initial state from regexp")

        toolbar.addWidget(txtRegex)
        toolbar.addWidget(btnRegex)

        # Cambio de fuente a todos los elementos
        self.setFont(fuentelblCelula)

        def cambioTamCelula():
            self.tamCuadro = spinBox.value()

        # Conectar señal del slider
        spinBox.valueChanged.connect(cambioTamCelula)

        # Frames
        frameDibujo = QFrame()
        frameDibujo.setFrameShape(QFrame.StyledPanel)

        frameOpciones = QFrame()
        frameOpciones.setFrameShape(QFrame.StyledPanel)

        # Layout principal
        layoutMain = QVBoxLayout()
        layoutMain.addWidget(menu)

        layoutMain.addWidget(frameDibujo)
        layoutMain.addWidget(frameOpciones)

        # Elementos para la parte izquierda

        # labels
        lblEntrada = QLabel("Type of Input")
        lblRegla = QLabel("Input The Rule")
        lblReglaEjemplo = QLabel("Example:")
        lblEjemploRegla = QLabel("30")

        # botones
        btnOpcionesDeEntradaA = QCheckBox("Binary")
        btnOpcionesDeEntradaB = QCheckBox("Decimal")
        btnOpcionesDeEntradaB.toggle()

        # Entrada de texto
        inTxtRegla = QLineEdit()
        inTxtRegla.setFixedWidth(200)

        vboxRegla = QVBoxLayout()
        vboxRegla.addWidget(lblEntrada)
        vboxRegla.addWidget(btnOpcionesDeEntradaA)
        vboxRegla.addWidget(btnOpcionesDeEntradaB)
        vboxRegla.addWidget(lblRegla)
        vboxRegla.addWidget(inTxtRegla)
        vboxRegla.addWidget(lblReglaEjemplo)
        vboxRegla.addWidget(lblEjemploRegla)

        # Elementos para la parte central

        # Label
        lblCondIni = QLabel("Initial state")
        lblGen = QLabel("Num. of generations")

        lblNumCel = QLabel("Num. of cells")
        lblPorcentaje = QLabel("Pct. of 1's")

        # Btn
        btnAleatorio = QCheckBox("Random")

        # Entrada de texto
        txtCondIni = QTextEdit()
        txtCondIni.setFixedWidth(400)
        txtCondIni.setToolTip("Initial condition")
        txtGen = QLineEdit()
        txtGen.setFixedWidth(100)
        txtGen.setToolTip("Number of generations")

        txtNumCel = QLineEdit("100")
        txtNumCel.setFixedWidth(100)
        txtNumCel.setToolTip("No. of cells")

        txtPorcentaje = QLineEdit("10")
        txtPorcentaje.setFixedWidth(100)
        txtPorcentaje.setToolTip("Percentage of 1's in initial state")

        # Layouts para controles inferiores
        layoutOpsInf = QHBoxLayout()

        layoutNG = QVBoxLayout()
        layoutNC = QVBoxLayout()
        layoutPUnos = QVBoxLayout()

        layoutNG.addWidget(lblGen)
        layoutNG.addWidget(txtGen)

        layoutNC.addWidget(lblNumCel)
        layoutNC.addWidget(txtNumCel)

        layoutPUnos.addWidget(lblPorcentaje)
        layoutPUnos.addWidget(txtPorcentaje)

        layoutOpsInf.addLayout(layoutNG)
        layoutOpsInf.addLayout(layoutNC)
        layoutOpsInf.addLayout(layoutPUnos)

        # Layout
        vboxCondIni = QVBoxLayout()
        vboxCondIni.addWidget(lblCondIni)
        vboxCondIni.addWidget(btnAleatorio)
        vboxCondIni.addWidget(txtCondIni)
        vboxCondIni.addLayout(layoutOpsInf)
        # vboxCondIni.addWidget(lblGen)
        # vboxCondIni.addWidget(txtGen)

        # Elementos para la parte derecha
        btnAceptar = QPushButton("Aceptar")
        btnZoomIn = QPushButton("Zoom +")
        btnZoomIn.setIcon(QtGui.QIcon('./Icons/zoom-in.png'))
        btnZoomIn.setIconSize(QtCore.QSize(44, 44))
        btnZoomIn.setToolTip("Zoom in the simulation")

        btnZoomOut = QPushButton("Zoom -")
        btnZoomOut.setIcon(QtGui.QIcon('./Icons/zoom-out.png'))
        btnZoomOut.setIconSize(QtCore.QSize(44, 44))
        btnZoomOut.setToolTip("Zoom out the simulation")

        btnGuardar = QPushButton("Save image")
        btnGuardar.setToolTip("Save image to file")

        # Layout para botones multimedia
        bntsMultimedia = QHBoxLayout()
        btnPlay = QPushButton("")
        btnPlay.setIcon(QtGui.QIcon('./Icons/play-button.png'))
        btnPlay.setIconSize(QtCore.QSize(44, 44))
        btnPlay.setToolTip("Start/Pause the simulation")

        btnStop = QPushButton("")
        btnStop.setIcon(QtGui.QIcon('./Icons/detener.png'))
        btnStop.setIconSize(QtCore.QSize(44, 44))
        btnStop.setToolTip("Stop the simulation")

        btnAumentarVel = QPushButton("")
        btnAumentarVel.setIcon(QtGui.QIcon('./Icons/hacia-adelante.png'))
        btnAumentarVel.setIconSize(QtCore.QSize(44, 44))
        btnAumentarVel.setToolTip("Increase the speed of the simulation")

        btnDisminuirVel = QPushButton("")
        btnDisminuirVel.setIcon(QtGui.QIcon('./Icons/hacia-atras.png'))
        btnDisminuirVel.setIconSize(QtCore.QSize(44, 44))
        btnDisminuirVel.setToolTip("Decrease the speed of the simulation")

        bntsMultimedia.addWidget(btnPlay)
        bntsMultimedia.addWidget(btnStop)
        bntsMultimedia.addWidget(btnDisminuirVel)
        bntsMultimedia.addWidget(btnAumentarVel)

        # Layout
        vboxDer = QVBoxLayout()
        # vboxDer.addWidget(btnAceptar)
        vboxDer.addLayout(bntsMultimedia)
        vboxDer.addWidget(btnGuardar)

        # Layout botones de zoom
        btnsLayout = QHBoxLayout()
        btnsLayout.addWidget(btnZoomIn)
        btnsLayout.addWidget(btnZoomOut)

        vboxDer.addLayout(btnsLayout)

        # Area para la graficacion de puntos
        layoutPlot = QVBoxLayout()
        self.plotArea = Figure(tight_layout=True)
        self.axes = self.plotArea.add_subplot(111)
        self.canvasplot = FigureCanvasQTAgg(self.plotArea)
        self.toolbar = NavigationToolbar2QT(self.canvasplot, self)
        self.axes.set_xlabel("Number of generations")
        self.axes.set_ylabel("Number of cells in the ring")
        layoutPlot.addWidget(self.toolbar)
        layoutPlot.addWidget(self.canvasplot)

        # Area para pintar
        self.scene = QGraphicsScene()
        self.view = QGraphicsView(self.scene)
        self.view.setScene(self.scene)
        self.view.setDragMode(QGraphicsView.DragMode.ScrollHandDrag)
        hboxDibujo = QHBoxLayout()
        frameDibujo.setLayout(hboxDibujo)
        hboxDibujo.addWidget(self.view)

        def condicionInicialRegexp():
            if len(txtRegex.text()) == 0:
                mostrarDialogoError(self, "Input a regular expression")
            else:
                txtCondIni.setText(' ')
                txtCondIni.setText(obtnerCadenaRegExpr(
                    txtRegex.text(), int(txtNumCel.text())))
            # txtCondIni.setText(obtenerCadenaRegExp())
            pass

        def cambioBinarioDecimalA():
            lblEjemploRegla.setText("00011110")
            btnOpcionesDeEntradaB.toggle()

        def cambioBinarioDecimalB():
            lblEjemploRegla.setText("30")
            btnOpcionesDeEntradaA.toggle()

        def ZoomIn():
            self.view.scale(1.5, 1.5)
            # self.view.scrollContentsBy(0,50)

        def ZoomOut():
            self.view.scale(0.9, 0.9)

        # Guarda el área de dibujo como una imágen
        def guardarImg():
            img = QImage(int(self.scene.width()), int(
                self.scene.height()), QImage.Format.Format_ARGB32_Premultiplied)
            img.fill(QtCore.Qt.white)
            q = QPainter(img)
            self.scene.render(q)
            q.end()

            dialogImg = DialogoImagen(self, img)
            dialogImg.show()

        self.isRunning = False
        self.isFT = True
        self.auxBtn = True

        self.numCelulas = 0
        self.porcentajeDeUnos = 0

        # Si no se han ingresado todos lo datos retorna True
        def validarEntradas():
            if len(inTxtRegla.text()) == 0 and len(txtGen.text()) == 0 and len(txtCondIni.toPlainText()) == 0 and len(txtPorcentaje.text()) and len(txtNumCel.text()):
                return True
            else:
                self.numGeneraciones = int(txtGen.text())
                self.numCelulas = int(txtPorcentaje.text())
                self.porcentajeDeUnos = int(txtNumCel.text())
                if self.isFT:
                    for elem in txtCondIni.toPlainText():
                        self.estadoInicial.append(int(elem))
                return False

        self.aux = []

        def pruebaS(arr):
            self.desplzamientoy = irPintando(arr, self.scene, self.rellenoUno, self.colorUno,
                                             self.rellenoDos, self.colorDos, self.desplazamiento, self.desplzamientoy, self.tamCuadro)
            self.aux.append(arr)
            if self.banderaGrafica == 0:
                graficaDeDensidad(self.aux, self.axes, self.canvasplot, self)
            elif self.banderaGrafica == 1:
                graficaDeMedia(self.aux, self.axes, self.canvasplot, self)
            else:
                graficaDeVarianza(self.aux, self.axes, self.canvasplot, self)

        def aumentarVelocidad(vel):
            lblVelocidad2.setText(" " + str(vel))

        def disminuirVelocidad(vel):
            lblVelocidad2.setText(" " + str(vel))

        def terminoSimulacion():
            btnPlay.setIcon(QtGui.QIcon('./Icons/play-button.png'))
            btnPlay.setIconSize(QtCore.QSize(44, 44))
            self.isRunning = False
            self.auxBtn = True
            self.aux = []
            self.isFT = True

        def resizeView(nuevoRect):
            self.view.fitInView(
                nuevoRect, QtCore.Qt.AspectRatioMode.KeepAspectRatio)

        def pintarArreglo():
            # Si no se esta ejecutando la animación se puede correr normalmente

            # limpiar scene
            if self.isFT:
                self.scene.clear()
                self.aux = []
                self.scene = QGraphicsScene()
                self.view.setScene(self.scene)
                self.puntos = []
                self.estadoInicial = []
                self.desplazamiento = self.tamCuadro
                self.desplzamientoy = self.tamCuadro
            # btnOpcionesDeEntradaA
            if validarEntradas():
                mostrarDialogoError(self, "Ingrese los datos")
                pass
            else:
                num = 0
                if btnOpcionesDeEntradaA.isChecked():
                    num = int(inTxtRegla.text(), 2)
                else:
                    num = int(inTxtRegla.text())

                if num > 255 or num < 0:
                    mostrarDialogoError(
                        self, "Invalid Rule, enter a value between 0 and 255")
                    pass
                else:
                    numEntrada = format(num, '#010b')
                    numEntradaBin = [int(x) for x in numEntrada[2:]]
                    # Arreglo en binario
                    regla = numEntradaBin
                    self.tabla = np.array(([1, 1, 1, regla[0]], [1, 1, 0, regla[1]], [1, 0, 1, regla[2]], [1, 0, 0, regla[3]], [
                                          0, 1, 1, regla[4]], [0, 1, 0, regla[5]], [0, 0, 1, regla[6]], [0, 0, 0, regla[7]]))
                    self.isFT = False
                    if not self.isRunning:
                        #self.desplzamientoy = irPintando( self.estadoInicial, self.scene, self.rellenoUno, self.colorUno, self.rellenoDos, self.colorDos, self.desplazamiento, self.desplzamientoy, self.tamCuadro)
                        self.worker = HiloView(self.scene, self.tabla, self.estadoInicial, self.numGeneraciones, self.axes, self.canvasplot, self,
                                               self.rellenoUno, self.colorUno, self.rellenoDos, self.colorDos, self.desplazamiento, self.desplzamientoy, self.tamCuadro)
                        self.worker.s.connect(pruebaS)
                        self.worker.signalResize.connect(resizeView)
                        self.worker.signalTermino.connect(terminoSimulacion)
                        self.worker.signalMasVel.connect(aumentarVelocidad)
                        self.worker.signalMenVel.connect(disminuirVelocidad)
                        self.worker.start()
                        self.isRunning = True

                        # Cambiar boton por pause
                        btnPlay.setIcon(QtGui.QIcon(
                            './Icons/pause-button.png'))
                        btnPlay.setIconSize(QtCore.QSize(44, 44))
                        btnStop.clicked.connect(self.worker.kill)

                        btnAumentarVel.clicked.connect(
                            self.worker.aumentarVelociad)
                        btnDisminuirVel.clicked.connect(
                            self.worker.disminuirVelociad)

                    else:
                        if self.auxBtn:
                            btnPlay.setIcon(QtGui.QIcon(
                                './Icons/play-button.png'))
                            btnPlay.setIconSize(QtCore.QSize(44, 44))
                            self.worker.pause()
                            self.auxBtn = False
                        else:
                            btnPlay.setIcon(QtGui.QIcon(
                                './Icons/pause-button.png'))
                            btnPlay.setIconSize(QtCore.QSize(44, 44))

                            self.worker.resume()
                            self.auxBtn = True

        def detenido():
            btnPlay.setIcon(QtGui.QIcon('./Icons/play-button.png'))
            btnPlay.setIconSize(QtCore.QSize(44, 44))
            self.isRunning = False
            self.auxBtn = True
            self.aux = []
            self.isFT = True

        # Genera aleatoriamente: regla, numero de generaciones y edo. Inicial
        def modoAleatorio():
            btnAleatorio.toggle()
            #edoInicialAleat = bin(randint(0, 2**30))
            #edoInicialarr = [int(x) for x in edoInicialAleat[2:]]
            cadEdoIni = ""
            if len(txtNumCel.text()) == 0 and len(txtPorcentaje.text()) == 0:
                mostrarDialogoError(
                    self, "Enter the number of cells and 1's percentage")
            else:
                self.numCelulas = int(txtNumCel.text())
                self.porcentajeDeUnos = int(txtPorcentaje.text())
                edoInicialarr = obtenerCondicionInicial(
                    self.numCelulas, self.porcentajeDeUnos)
                for i in edoInicialarr:
                    cadEdoIni += str(int(i))
                txtCondIni.setText(cadEdoIni)
                inTxtRegla.setText(str(randint(0, 255)))
                txtGen.setText((str(randint(0, 200))))

            pass

        # Funcion para mostrar el estado inicial
        def guardarEstadoInicial():
            if validarEntradas():
                mostrarDialogoError(self, "Please, provide all the data")
                pass
            else:
                gimg = DialogoGuardarArchio(self, txtCondIni.toPlainText(), inTxtRegla.text(), txtGen.text(
                ), self.colorUno.name(), self.rellenoUno, self.colorDos.name(), self.rellenoDos, self.tamCuadro)
                gimg.show()
                pass

        # Funcion para cargar el archivo .data
        def cargarEstadoInicial():
            selectorArchivo, _ = QFileDialog.getOpenFileName(
                self, 'Open file', './Guardado', "*.data")
            cad = ""
            if len(selectorArchivo) != 0:
                with open(selectorArchivo) as filehandle:
                    data = json.load(filehandle)
                    txtCondIni.setText(data['estadoInicial'])
                    inTxtRegla.setText(data['regla'])
                    txtGen.setText(data['generaciones'])
                    self.colorUno = QColor(data['colorUno'])
                    self.colorDos = QColor(data['colorCero'])
                    self.tamCuadro = data['tamCuadro']
                    spinBox.setValue(self.tamCuadro)
                    self.rellenoUno = data['rellenoUno']
                    self.rellenoDos = data['rellenoCero']

                    toggleRellenoUno()
                    toggleRellenoUno()
                    toggleRellenoDos()
                    toggleRellenoDos()

                    auxColor1 = QtGui.QPixmap(100, 100)
                    auxColor1.fill(self.colorUno)
                    iconoColor1 = QtGui.QIcon(auxColor1)
                    cambiarColorUno.setIcon(iconoColor1)

                    auxColor2 = QtGui.QPixmap(100, 100)
                    auxColor2.fill(self.colorDos)
                    iconoColor2 = QtGui.QIcon(auxColor2)
                    cambiarColorCero.setIcon(iconoColor2)

                    self.tamCuadro = data['tamCuadro']
                pintarArreglo()

        # señales para Guardar y cargar
        guardar.triggered.connect(guardarEstadoInicial)
        cargar.triggered.connect(cargarEstadoInicial)

        # Señal para boton regexp
        btnRegex.clicked.connect(condicionInicialRegexp)

        # Señal para cambio en las opciones {binario, decimal}
        btnOpcionesDeEntradaA.clicked.connect(cambioBinarioDecimalA)
        btnOpcionesDeEntradaB.clicked.connect(cambioBinarioDecimalB)

        # Señales para botones multimedia
        btnPlay.clicked.connect(pintarArreglo)
        btnStop.clicked.connect(detenido)

        btnAceptar.clicked.connect(pintarArreglo)
        btnZoomIn.clicked.connect(ZoomIn)
        btnZoomOut.clicked.connect(ZoomOut)

        btnGuardar.clicked.connect(guardarImg)

        # Señal para boton aleatorio
        btnAleatorio.clicked.connect(modoAleatorio)

        # Layout para las opciones
        hboxOpciones = QHBoxLayout()
        frameOpciones.setLayout(hboxOpciones)
        frameOpciones.setFixedHeight(200)

        # Agregar elementos para agregar la regla
        hboxOpciones.addLayout(vboxRegla)
        hboxOpciones.addLayout(vboxCondIni)
        hboxOpciones.addLayout(vboxDer)

        vbox_princial.addWidget(menu)
        vbox_princial.addWidget(toolbar)
        vbox_princial.addLayout(hbox)
        hbox.addLayout(layoutMain, 2)
        hbox.addLayout(layoutPlot, 1)


if __name__ == "__main__":

    directorio = "./Imagenes"
    try:
        os.stat(directorio)
    except:
        os.mkdir(directorio)

    directorio = "./Guardado"
    try:
        os.stat(directorio)
    except:
        os.mkdir(directorio)

    app = QtWidgets.QApplication(sys.argv)

    widget = MyWidget()
    widget.resize(1720, 800)
    widget.show()

    sys.exit(app.exec_())
