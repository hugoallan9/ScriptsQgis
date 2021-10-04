import sys
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from qgis.core import *
from qgis.gui import *

qgis_prefix = "/usr"
app = QgsApplication([], True) 
QgsApplication.setPrefixPath(qgis_prefix, True)

#print QgsApplication.showSettings()

QgsApplication.initQgis()
#mapinstance = QgsMapLayerRegistry.instance()

##Canvas
canvas = QgsMapCanvas()
canvas.setCanvasColor(Qt.white)
canvas.enableAntiAliasing(True)



##Agregando el mapa de la Republica como un layer
mapa = QgsVectorLayer("/home/hugog/Insync/hugoallangm@gmail.com/Google Drive/Consultorias/UNICEF/Mapas/departamentos_gtm/departamentos_gtm.shp","","ogr")
if not mapa.isValid():
	print("El mapa no se pudo cargar")
else:
	print("El mapa ha sido cargado exitosamente")
idMapa = mapa.id()
print(idMapa)
##Agregando el CSV como una capa vectorial
uri = "file:///C:/Users/INE/Documents/pruebaDatos.csv?delimiter=%s&x=%s&y=%s" % (";","X","Y")
datos = QgsVectorLayer(uri, "", "delimitedtext")
if not datos.isValid():
	print ("La capa de los csv no se pudo cargar")
else:
	print ("Se cargo el csv exitosamente")
idDatos = datos.id()
print(idDatos)

##Agregando el mapa a la region activa para poder ser renderizado
layerset = []
mapinstance.addMapLayer(mapa)
mapinstance.addMapLayer(datos)
layerset.append(mapa.id() )


# set extent to the extent of our layer
canvas.setExtent(mapa.extent())
canvas.setLayerSet([QgsMapCanvasLayer(mapa)])
canvas.show()
canvas.freeze(True)

##Haciendo el Join 
info = QgsVectorJoinInfo()
info.joinFieldName = "X"
info.joinLayerId =  idDatos
info.targetFieldName = "DEPARTAMEN"
info.memoryCache = False
mapinstance.mapLayer(idMapa).addJoin(info) 

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
mapinstance.addMapLayer( mapa )
layerset = [idMapa]
print(mapinstance.mapLayers())

## Haciendo el composer 
print("Los settings del canvas son")
print(canvas.mapSettings().extent().toString())
mapRenderer = QgsMapRenderer()
mapRectangle = QgsRectangle(350000,1600000,800000,2000000)
lst = [idMapa]
mapRenderer.setLayerSet(lst)
print(mapRenderer.setExtent(mapRectangle))
print("El extent del mapa es: ")
print(mapRenderer.extent().yMaximum ())
c = QgsComposition(canvas.mapSettings())
print("El layer set es: ")
print(mapRenderer.layerSet()[0])
mapRenderer.updateScale ()
c.setPlotStyle(QgsComposition.Print)


##Agregando el mapa al composer
x, y = 0.5, 0.5
w, h = c.paperWidth(), c.paperHeight()
composerMap = QgsComposerMap(c, x ,y, w, h)
#composerMap.setItemPosition(,100)
c.addItem(composerMap)




##Agregando la leyenda
legend = QgsComposerLegend(c)
legend.model().setLayerSet(mapRenderer.layerSet())
legend.setItemPosition(0,0,False)
legend.setTitle("")
c.addItem(legend)




##Exportando a pdf
printer = QPrinter()
printer.setOutputFormat(QPrinter.PdfFormat)
printer.setOutputFileName("C:/Users/INE/Documents/MapaRepublica/mapa.pdf")
printer.setPaperSize(QSizeF(c.paperWidth(), c.paperHeight()), QPrinter.Millimeter)
printer.setFullPage(True)
printer.setColorMode(QPrinter.Color)
printer.setResolution(c.printResolution())

pdfPainter = QPainter(printer)
paperRectMM = printer.pageRect(QPrinter.Millimeter)
paperRectPixel = printer.pageRect(QPrinter.DevicePixel)
c.render(pdfPainter, paperRectPixel, paperRectMM)
pdfPainter.end()

# create image
img = QImage(QSize(800,600), QImage.Format_ARGB32_Premultiplied)
# set image background color
color = QColor(255,255,255)
img.fill(color.rgb())
# create painter
p = QPainter()
p.begin(img)
p.setRenderHint(QPainter.Antialiasing)
render = QgsMapRenderer()
# set layer set
lst = [ idMapa ] # add ID of every layer
render.setLayerSet(lst)
# set extent
rect = QgsRectangle(render.fullExtent())
#rect.scale(1.39800703)
rect.scale(1.1)
render.setExtent(rect)
# set output size
render.setOutputSize(img.size(), img.logicalDpiX())
# do the rendering
render.render(p)
p.end()

# save image
img.save('C:/Users/INE/Documents/MapaRepublica/mapa.png',"png")    
app.exec_()
##Cerrando la aplicacion
#QgsApplication.exitQgis() 



