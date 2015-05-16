#--- Load a csv file and set CRS
#---1 Reference library
from PyQt4.QtGui import *
from PyQt4.QtCore import * 
from qgis.core import *
from qgis.utils import iface
print QgsApplication.showSettings()
from qgis.gui import *

canvas = QgsMapCanvas()




print QgsApplication.showSettings()

##Agregando el mapa de la Republica como un layer
mapa = QgsVectorLayer("C:/Users/hugoa_000/Documents/MapaRepublica/22_DEPARTAMENTOS.shp","","ogr")
if not mapa.isValid():
    print "ERROR: El mapa no pudo ser cargado."
idMapa = mapa.id()
print(idMapa)


##Agregando el CSV como una capa vectorial
uri = "file:///C:/Users/hugoa_000/Documents/pruebaDatos.csv?delimiter=%s&x=%s&y=%s" % (";","x","y")
datos = QgsVectorLayer(uri, "", "delimitedtext")
print "La capa de los csv es valida: " 
print datos.isValid()
idDatos = datos.id()
print idDatos

##Agregando el mapa a la region activa para poder ser renderizado
QgsMapLayerRegistry.instance().addMapLayer(mapa)
QgsMapLayerRegistry.instance().addMapLayer(datos)

# set extent to the extent of our layer
canvas.setExtent(mapa.extent())

# set the map canvas layer set
canvas.setLayerSet([QgsMapCanvasLayer(mapa)])
canvas.show()


##Haciendo el Join 
info = QgsVectorJoinInfo()
info.joinFieldName = "X"
info.joinLayerId =  idDatos
info.targetFieldName = "DEPARTAMEN"
info.memoryCache = False
QgsMapLayerRegistry.instance().mapLayer(idMapa).addJoin(info) 

## Aplicando el pintado con cierta graduacion
fieldName = "_Y"
fieldIndex = mapa.fieldNameIndex( fieldName )
provider = mapa.dataProvider()
numberOfClasses = 4
color1 =  QColor ( 93, 152, 202, 255 )
color2 = QColor("blue")
color3 = QColor("white")
ramp = QgsVectorGradientColorRampV2(color1, color2)
props = { 'color_border' : '255,255,255,255', 'style' : 'solid', 'style_border' : 'solid' , 'width_border':'0.4'}
symbol =  QgsFillSymbolV2.createSimple(props)
renderer = QgsGraduatedSymbolRendererV2.createRenderer(mapa, fieldName, numberOfClasses, QgsGraduatedSymbolRendererV2.Quantile, symbol, ramp)

mapa.setRendererV2( renderer )
QgsMapLayerRegistry.instance().addMapLayer( mapa )



## Haciendo el composer 
mapRenderer = iface.mapCanvas().mapRenderer()
lst = [idMapa] 
mapRenderer.setLayerSet(lst)
print "El layer set es: "
print mapRenderer.layerSet()
c = QgsComposition(mapRenderer)
c.setPlotStyle(QgsComposition.Print)


##Agregando el mapa al composer
x, y = 0.5, 0.5
w, h = c.paperWidth(), c.paperHeight()
composerMap = QgsComposerMap(c, x ,y, w, h)
#composerMap.setItemPosition(-,-450)
c.addComposerMap(composerMap)




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








    