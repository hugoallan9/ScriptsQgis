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
        self.mapa.crear_layer_datos(x= 'Código Departamento',y='Continuo')
        print(self.mapa.proyecto.mapLayers())

    def test_join(self):
        self.test_crear_layer_datos()
        self.mapa.join(x= 'Código Departamento')

    def test_pintar_mapa_intervalos(self):
        self.test_join()
        self.mapa.pintar_mapa_intervalos(fieldName = "datos_Continuo",color1=self.mapa.colorCyan,
                              color2=self.mapa.colorBlanco, numeroClases=4)
        #self.mapa.exportarMapa()

    def test_exportar_mapa(self):
        self.test_cambiarBorde()
        self.mapa.exportarMapa()

    def test_cambiarBorde(self):
        self.test_pintar_mapa_intervalos()
        self.mapa.cambiarBorde(color="#808080",grosor=0.4)


