#--- Load a csv file and set CRS
#---1 Reference library
from PyQt4.QtGui import *
from PyQt4.QtCore import * 
from qgis.core import *
from qgis.utils import iface


##Agregando el mapa de la Republica como un layer
mapa = QgsVectorLayer("C:/Users/INE/Documents/MapaRepublica/22_DEPARTAMENTOS.shp","","ogr")
if not mapa.isValid():
    print "ERROR: El mapa no pudo ser cargado."
idMapa = mapa.id()
print(idMapa)


##Agregando el CSV como una capa vectorial
uri = "file:///C:/Users/INE/Documents/pruebaDatos.csv?delimiter=%s&x=%s&y=%s" % (";","x","y")
datos = QgsVectorLayer(uri, "", "delimitedtext")
idDatos = datos.id()
print idDatos

##Agregando el mapa a la region activa para poder ser renderizado
QgsMapLayerRegistry.instance().addMapLayer(mapa)
QgsMapLayerRegistry.instance().addMapLayer(datos)


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







    