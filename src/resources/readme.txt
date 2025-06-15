put all resource path into *.qrc file

compile into python package:
pyrcc5 resources/resources.qrc -o resources/resources_rc.py

use:
from PyQt5.QtGui import QIcon
icon = QIcon(":/images/app_icon.png")