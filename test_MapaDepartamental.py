from unittest import TestCase
from MapaDepartamental import MapaDepartamental

class TestMapaDepartamental(TestCase):
    def setUp(self) -> None:
        self.mapa = MapaDepartamental()

    def test_cargar_shape(self):
        self.mapa.cargar_shape()
        print(self.mapa.proyecto.mapLayers())

    def test_cargar_datos(self):
        columnas = self.mapa.cargar_datos()
        print(columnas)

    def test_crear_layer_datos(self):
        self.test_cargar_shape()
        self.test_cargar_datos()
        self.mapa.crear_layer_datos(x= 'Código Departamento',y='Educación')
        print(self.mapa.proyecto.mapLayers())

    def test_join(self):
        self.test_crear_layer_datos()
        self.mapa.join(x= 'Código Departamento')