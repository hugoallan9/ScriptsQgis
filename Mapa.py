#from PyQt4.QtGui import *
#from PyQt4.QtCore import *

from qgis.utils import iface
from PyQt5.QtGui import QColor
from PyQt5.QtCore import QSize
import os
from qgis.core import (
    QgsProject,
    QgsApplication,
    QgsGradientColorRamp,
    QgsGraduatedSymbolRenderer,
    QgsCategorizedSymbolRenderer,
    QgsClassificationQuantile,
    QgsMapSettings,
    QgsMapRendererParallelJob,
    QgsFillSymbol,
 )


class Mapa:
    def __init__(self):
        self.mapa = None
        self.qgs = QgsApplication([],True)
        self.qgs.initQgis()
        self.proyecto = QgsProject()
        self.colorCyan = QColor(0,174,239,255)
        self.colorBlanco = QColor(255,255,255,255)



    def pintar_mapa_intervalos(self,fieldName, color1 ,color2 ,discreto = False):
        rampa = QgsGradientColorRamp(color1,color2,discreto)
        #Crear el método de clasificación
        clasificacion = QgsClassificationQuantile()
        clasificacion.classes(self.mapa, fieldName,4)
        #Creación de render
        clas = clasificacion.classes(self.mapa, fieldName,4)
        renderer = QgsGraduatedSymbolRenderer(fieldName)
        renderer.setClassAttribute(fieldName)
        renderer.setClassificationMethod(clasificacion)
        renderer.updateColorRamp(rampa)
        props = {'color_border': '255,255,255,255', 'style': 'solid', 'style_border': 'solid', 'width_border': '0.4'}
        symbol = QgsFillSymbol.createSimple(props)
        renderer = QgsGraduatedSymbolRenderer.createRenderer(self.mapa,
                                                             fieldName, 4, QgsGraduatedSymbolRenderer.Quantile, symbol, rampa)
        self.mapa.setRenderer(renderer)

    def exportarMapa(self):
        image_location = os.path.join(QgsProject.instance().homePath(), "render1.png")
        vlayer = self.mapa
        settings = QgsMapSettings()
        settings.setLayers([vlayer])
        settings.setBackgroundColor(QColor(255, 255, 255))
        settings.setOutputSize(QSize(800, 600))
        settings.setExtent(vlayer.extent())

        render = QgsMapRendererParallelJob(settings)

        def finished():
            img = render.renderedImage()
            # save the image; e.g. img.save("/Users/myuser/render.png","png")
            img.save(image_location, "png")

        render.finished.connect(finished)

        # Start the rendering
        render.start()

        # The following loop is not normally required, we
        # are using it here because this is a standalone example.
        from qgis.PyQt.QtCore import QEventLoop
        loop = QEventLoop()
        render.finished.connect(loop.quit)
        loop.exec_()




