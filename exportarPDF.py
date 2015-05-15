from PyQt4.QtGui import *
from PyQt4.QtCore import * 
from qgis.core import *
from qgis.utils import iface

## Haciendo el composer 

mapRenderer = iface.mapCanvas().mapRenderer()
c = QgsComposition(mapRenderer)
c.setPlotStyle(QgsComposition.Print)


##Agregando el mapa al composer
x, y = 0.5, 0.5
w, h = c.paperWidth(), c.paperHeight()
composerMap = QgsComposerMap(c, x ,y, w, h)
composerMap.setItemPosition(-300,-450)
c.addItem(composerMap)




##Agregando la leyenda
legend = QgsComposerLegend(c)
legend.model().setLayerSet(mapRenderer.layerSet())
legend.setItemPosition(100,10,False)
legend.setTitle("")
c.addItem(legend)




##Exportando a pdf
printer = QPrinter()
printer.setOutputFormat(QPrinter.PdfFormat)
printer.setOutputFileName("C:/Users/INE/Documents/MapaRepublica/pruebaMapa1.pdf")
printer.setPaperSize(QSizeF(c.paperWidth(), c.paperHeight()), QPrinter.Millimeter)
printer.setFullPage(True)
printer.setColorMode(QPrinter.Color)
printer.setResolution(c.printResolution())

pdfPainter = QPainter(printer)
paperRectMM = printer.pageRect(QPrinter.Millimeter)
paperRectPixel = printer.pageRect(QPrinter.DevicePixel)
c.render(pdfPainter, paperRectPixel, paperRectMM)
pdfPainter.end()


