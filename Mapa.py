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
    QgsPrintLayout,
    QgsLayoutItemMap,
    QgsLayoutPoint,
    QgsUnitTypes,
    QgsLayoutSize,
    QgsLayoutExporter,
 )


class Mapa:
    def __init__(self):
        self.mapa = None
        self.qgs = QgsApplication([],True)
        self.qgs.initQgis()
        self.proyecto = QgsProject().instance()
        self.colorCyan = QColor(0,174,239,255)
        self.colorBlanco = QColor(255,255,255,255)



    def pintar_mapa_intervalos(self,fieldName, color1 ,color2, numeroClases ,discreto = False):
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
        #props = {'color_border': 'black', 'style': 'solid', 'style_border': 'solid', 'width_border': '0.4'}
        #symbol = QgsFillSymbol.createSimple(props)

        symbol = self.mapa.renderer().symbol()

        renderer = QgsGraduatedSymbolRenderer.createRenderer(self.mapa,
                                                             fieldName, numeroClases, QgsGraduatedSymbolRenderer.Quantile, symbol, rampa)
        self.mapa.setRenderer(renderer)

    def cambiarBorde(self, color = 'white', grosor = 0.3):
        props = {'color_border': color, 'style': 'solid', 'style_border': 'solid', 'width_border': grosor}
        symbol = QgsFillSymbol.createSimple(props)
        self.mapa.renderer().updateSymbols(symbol)





    def _exportarMapaPruebas(self):
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

    def exportarMapa(self,formato = 'svg'):
        layout = QgsPrintLayout(self.proyecto)
        layout.initializeDefaults()

        #Añadiendo mapa
        mapa = QgsLayoutItemMap(layout)
        mapa.attemptMove(QgsLayoutPoint(5,5,QgsUnitTypes.LayoutMillimeters))
        mapa.attemptResize(QgsLayoutSize(200,200,QgsUnitTypes.LayoutMillimeters))
        #mapa.zoomToExtent(iface.mapCanvas().extent())
        layout.addLayoutItem(mapa)

        base_path = os.path.join(QgsProject.instance().homePath())
        pdf_path = os.path.join(base_path, "output.pdf")

        exporter = QgsLayoutExporter(layout)
        exporter.exportToPdf(pdf_path, QgsLayoutExporter.PdfExportSettings())

