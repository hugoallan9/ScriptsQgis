#from PyQt4.QtGui import *
#from PyQt4.QtCore import *

from qgis.utils import iface
from qgis.core import QgsProject, QgsApplication


class Mapa:
    def __init__(self):
        self.mapa = None
        self.qgs = QgsApplication([],True)
        self.qgs.initQgis()
        self.proyecto = QgsProject()
