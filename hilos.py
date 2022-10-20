import sys
import traceback
import time
from definiciones import Circular
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

import matplotlib
matplotlib.use('Qt5Agg')


"""
Funcion que retorna el valor de salida de la célula dada la tabla para el ECA
@param celula: arreglo de 3 elementos 
@param tabla:  arreglo de 8x4 de la forma [x,x,x,output] donde x el valor de la célula y output la salida
@return regla[3]: 
"""


def buscarEnTabla(celula, tabla):
    for regla in tabla:
        aux = regla[0:3]
        x = np.equal(regla[0:3], celula)
        if x.all():
            return regla[3]


def procesamiento(arregloCircular, tabla, estadoInicial):
    salida = []
    for elem in estadoInicial:
        aux = [arregloCircular.prev(), arregloCircular.next(),
               arregloCircular.next()]
        salida.append(buscarEnTabla(aux, tabla))
    return salida


def pintarUno(scene, rellenoUno, colorUno, desplazamiento, desplzamientoy, tamCuadro):
    pen = QtGui.QPen(colorUno)
    pen.setJoinStyle(QtCore.Qt.PenJoinStyle.SvgMiterJoin)
    rec = QGraphicsRectItem(
        desplazamiento, desplzamientoy, tamCuadro, tamCuadro)
    if rellenoUno:
        rec.setBrush(QtGui.QBrush(colorUno))
    rec.setPen(pen)
    scene.addItem(rec)


def pintarCero(scene, rellenoDos, colorDos, desplazamiento, desplzamientoy, tamCuadro):
    pen = QtGui.QPen(colorDos)
    pen.setJoinStyle(QtCore.Qt.PenJoinStyle.SvgMiterJoin)
    rec = QGraphicsRectItem(
        desplazamiento, desplzamientoy, tamCuadro, tamCuadro)
    if rellenoDos:
        rec.setBrush(QtGui.QBrush(colorDos))
    rec.setPen(pen)
    scene.addItem(rec)


def irPintando(arr, scene, rellenoUno, colorUno, rellenoDos, colorDos, desplazamiento, desplzamientoy, tamCuadro):
    desplazamiento = tamCuadro
    for k in arr:
        if k == 1:
            pintarUno(scene, rellenoUno, colorUno,
                      desplazamiento, desplzamientoy, tamCuadro)
        else:
            pintarCero(scene, rellenoDos, colorDos,
                       desplazamiento, desplzamientoy, tamCuadro)
        desplazamiento += (tamCuadro+1)
    desplzamientoy += (tamCuadro+1)
    return desplzamientoy


def graficaDeVarianza(arr, axes, canvasplot, ventana):
    sumasPuntos = []
    N = len(arr[0])
    for i in arr:
        media = (np.sum(i)/N)
        cont = 0
        for k in i:
            cont += ((i[k]-media)**2) / N
        sumasPuntos.append(cont)
    axes.cla()
    axes.plot(sumasPuntos)
    toolbar = NavigationToolbar2QT(canvasplot, ventana)
    axes.set_xlabel("Number of generations")
    axes.set_ylabel("Number of cells in the ring")
    axes.set_title("Viariance Graph")
    canvasplot.draw()


def graficaDeMedia(arr, axes, canvasplot, ventana):
    sumasPuntos = []
    N = len(arr[0])
    for i in arr:
        sumasPuntos.append(np.sum(i)/N)
    axes.cla()
    axes.plot(sumasPuntos)
    toolbar = NavigationToolbar2QT(canvasplot, ventana)
    axes.set_xlabel("Number of generations")
    axes.set_ylabel("Number of cells in the ring")
    axes.set_title("Average Graph")
    canvasplot.draw()


def graficaDeDensidad(arr, axes, canvasplot, ventana):
    sumasPuntos = []
    for i in arr:
        suma = np.sum(i)
        sumasPuntos.append(suma)
    axes.cla()
    axes.plot(sumasPuntos)
    toolbar = NavigationToolbar2QT(canvasplot, ventana)
    axes.set_xlabel("Number of generations")
    axes.set_ylabel("Number of cells in the ring")
    axes.set_title("Density Graph")
    canvasplot.draw()


def ProcesarEntrada(scene, tabla, estadoInicial, numGeneraciones, axes, canvasplot, ventana, rellenoUno, colorUno, rellenoDos, colorDos, desplazamiento, desplzamientoy, tamCuadro):
    puntos = []
    puntos.append(Circular(estadoInicial))
    for x in range(numGeneraciones):
        res = procesamiento(Circular(puntos[x]), tabla, estadoInicial)
        puntos.append(res)
        desplzamientoy = irPintando(res, scene, rellenoUno, colorUno,
                                    rellenoDos, colorDos, desplazamiento, desplzamientoy, tamCuadro)

    graficaDeDensidad(puntos, axes, canvasplot, ventana)
    return puntos


"""
Clase que implementa un hilo para poder pintar en QgraphicsView usando la señal
"""


class HiloView(QThread):
    s = pyqtSignal(object)
    signalResize = pyqtSignal(QRectF)
    signalTermino = pyqtSignal()
    signalMasVel = pyqtSignal(object)
    signalMenVel = pyqtSignal(object)

    def __init__(self, scene, tabla, estadoInicial, numGeneraciones, axes, canvasplot, ventana, rellenoUno, colorUno, rellenoDos, colorDos, desplazamiento, desplzamientoy, tamCuadro):
        super().__init__()

        self.estadoInicial = estadoInicial
        self.numGeneraciones = numGeneraciones
        self.tabla = tabla

        self.scene = scene
        self.velocidad = 0.15

        self.is_paused = False
        self.is_killed = False

    def run(self):
        puntos = []
        puntos.append(Circular(self.estadoInicial))
        self.s.emit(self.estadoInicial)
        for x in range(self.numGeneraciones):
            while self.is_paused:
                time.sleep(0.10)
                pass
            if self.is_killed:
                break
            res = procesamiento(
                Circular(puntos[x]), self.tabla, self.estadoInicial)
            puntos.append(res)
            time.sleep(self.velocidad)
            rect = self.scene.itemsBoundingRect()
            self.s.emit(res)
            self.signalResize.emit(rect)
        self.signalTermino.emit()

    def pause(self):
        print(">pause")
        self.is_paused = True

    def resume(self):
        print(">resume")
        self.is_paused = False

    def kill(self):
        self.is_paused = False
        self.is_killed = True

    def aumentarVelociad(self):
        aux = self.velocidad-0.15
        if aux >= 0:
            self.velocidad = 0.15
        else:
            self.velocidad = aux
        self.signalMasVel.emit(self.velocidad)

    def disminuirVelociad(self):
        self.velocidad += 0.15
        self.signalMenVel.emit(self.velocidad)
