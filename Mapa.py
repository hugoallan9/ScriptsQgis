#from PyQt4.QtGui import *
#from PyQt4.QtCore import *
import math

from qgis.utils import iface
from PyQt5.QtGui import QColor, QFont
from PyQt5.QtCore import QSize, QPointF, Qt
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
    QgsRectangle,
    QgsLayoutItemLabel,
    QgsLayoutItemLegend,
    QgsPointXY,
    QgsRenderContext,
    QgsLayoutItemPage,
 )
from qgis.gui import (
    QgsMapCanvas,
    QgsVertexMarker,
    QgsMapCanvasItem,
    QgsRubberBand,
)


class Mapa:
    def __init__(self):
        self.mapa = None
        self.qgs = QgsApplication([],True)
        self.qgs.initQgis()
        self.proyecto = QgsProject().instance()
        self.colorCyan = QColor(0,174,239,255)
        self.colorBlanco = QColor(255,255,255,255)
        self.paperHeight = 0
        self.paperWidth= 0



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

    def cambiarTamHoja(self, layout, size = "Letter", height = 0, width = 0):
        pc = layout.pageCollection()
        if size == "Letter":
            self.paperHeight = 8.5
            self.paperWidth = 11
        elif size == "Presentation":
            self.paperWidth = 9.60 * 2.36
            self.paperHeight = 9.60
        elif size == "Personalizado":
            self.paperHeight = width
            self.paperWidth = height
        pc.pages()[0].setPageSize(QgsLayoutSize(width = self.paperWidth, height = self.paperHeight,
                                                units = QgsUnitTypes.LayoutInches))

    def insertarTitulo(self, layout, titulo):
        label = None
        if self.layout.itemById('labelTitulo') == None:
            label = QgsLayoutItemLabel(layout)
            label.setId('labelTitulo')
        else:
            label = self.layout.itemById('labelTitulo')
        label.setText(titulo)
        fuente = QFont("Arial", math.floor(72 * self.paperHeight * 1 / 10 * 0.5))
        label.setFont(fuente)
        label.adjustSizeToText()
        tamTexto = label.sizeForText()
        label.attemptMove(
            QgsLayoutPoint(self.paperWidth / 2 - (tamTexto.width() / 2) * 0.0394, 0.01, QgsUnitTypes.LayoutInches))
        layout.addLayoutItem(label)


    def exportarMapa(self,formato = 'svg'):
        self.manager = self.proyecto.layoutManager()
        layoutName = 'Layout1'
        layouts_list = self.manager.printLayouts()
        # remove any duplicate layouts
        for layout in layouts_list:
            if layout.name() == layoutName:
                self.manager.removeLayout(layout)
        self.layout = QgsPrintLayout(self.proyecto)
        self.layout.initializeDefaults()
        self.cambiarTamHoja(self.layout, size="Letter")
        self.manager.addLayout(self.layout)

        #Añadiendo mapa
        mapa = QgsLayoutItemMap(self.layout)
        mapa.attemptMove(QgsLayoutPoint(self.paperWidth/20,self.paperHeight*2/20,QgsUnitTypes.LayoutInches))
        mapa.attemptResize(QgsLayoutSize(self.paperHeight*17/20,self.paperWidth,QgsUnitTypes.LayoutInches))
        mapa.setExtent(self.mapa.extent())
        self.layout.addLayoutItem(mapa)


        self.insertarTitulo(self.layout, "En UNICEF amamos a los niños")


        '''
        

        legend = QgsLayoutItemLegend(layout)
        legend.setTitle("Legend")
        layout.addLayoutItem(legend)
        #legend.attemptMove(QgsLayoutPoint(246, 5, QgsUnitTypes.LayoutMillimeters))
'''
        base_path = os.path.join(QgsProject.instance().homePath())
        pdf_path = os.path.join(base_path, "output.pdf")

        #layout = manager.layoutByName(layoutName)
        exporter = QgsLayoutExporter(self.layout)
        exporter.exportToPdf(pdf_path, QgsLayoutExporter.PdfExportSettings())

