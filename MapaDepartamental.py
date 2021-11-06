import os.path

from Mapa import Mapa
from qgis.core import QgsVectorLayer, QgsField, QgsFeature, QgsVectorLayerJoinInfo
from PyQt5.QtCore import QVariant
from pandas import read_excel
import os

class MapaDepartamental(Mapa):
    def __init__(self):
        super().__init__()

    def cargar_shape(self):
        self.mapa = QgsVectorLayer(os.path.join(os.getcwd(),
                                                'departamentos_gtm/departamentos_gtm.shp'), "", "ogr")
        if not self.mapa.isValid():
            print("ERROR: El mapa no pudo ser cargado.")
        else:
            self.IdMapa = self.mapa.id()
            self.proyecto.instance().addMapLayer(self.mapa)

    def cargar_datos(self, ruta = os.path.join(os.getcwd(),'Datos_pruebas/datos_deptos.xlsx')):
        self.datos = read_excel(ruta)
        self.datos.dropna(inplace=True)
        print(self.datos.columns)

    def crear_layer_datos(self, x,y):
        temp = QgsVectorLayer("none","result","memory")
        temp_data = temp.dataProvider()
        #Inicio de la edición
        temp.startEditing()

        #Creación de los campos en el layer temporal
        temp.addAttribute(QgsField(x, QVariant.Double ))
        temp.addAttribute(QgsField(y, QVariant.Double))
        #Actualización de los datos en el layer
        temp.updateFields()

        #Agregando los features
        for row in self.datos.loc[:,[x,y]].itertuples():
            f = QgsFeature()
            f.setAttributes([row[1],row[2]])
            temp.addFeature(f)

        #Empaquetando todo
        temp.commitChanges()
        self.IdDatos = temp.id()
        #Agregar el layer al proyecto
        self.proyecto.instance().addMapLayer(temp)


    def join(self,x):
        info = QgsVectorLayerJoinInfo()
        info.setJoinFieldName(x)
        info.setJoinLayerId(self.IdDatos)
        info.setJoinLayer(self.proyecto.instance().mapLayer(self.IdDatos))
        info.setTargetFieldName("departamen")
        info.setPrefix("datos_")
        self.proyecto.instance().mapLayer(self.IdMapa).addJoin(info)
        self.mapa.updateFields()
