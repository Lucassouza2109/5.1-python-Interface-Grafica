
from PySide6.QtWidgets import QMainWindow, QMessageBox, QVBoxLayout, QWidget


class MainWindow(QMainWindow):
    def __init__(self, parent: QWidget | None = None, *args, **kwargs) -> None:
        super().__init__(parent, *args, **kwargs)

        # CONFIGURANDO O LAYOUT BASICO.
        self.cw = QWidget() # CRIO UMA JANELA
        self.vLayout = QVBoxLayout() # DEFINO O LAYOUT 
        self.cw.setLayout(self.vLayout) 
        # QUALQUER WIDGET ADD - SERA ORG. CONFORME LAYOUT DEFINIDO.
        self.setCentralWidget(self.cw)
        # QUALQUER WIDGET ADICIONADO SERA EXIBIDO NA JANELA PRINCIPAL. 
        # MAS, SELF.CW E MEU WIDGET PRINCIPAL. 

        # TITULO DA JANELA. 
        self.setWindowTitle('Calculadora')

    def adjustFixedSize(self):
        # ULTIMA COISA A SER FEITA. 
        self.adjustSize()
        self.setFixedSize(self.width(), self.height())


    def addWidgetToVLayout(self, widget: QWidget):
        self.vLayout.addWidget(widget)

    def makeMsgBox(self):
        return QMessageBox(self)