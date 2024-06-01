# type: ignore

import sys

from buttons import ButtonsGrid

from display import Display

from info import Info

from main_window import MainWindow
# IMPORTANDO DO MODULO = MAINWINDOW. 

from PySide6.QtWidgets import QApplication, QLabel
# QLabel = texto a ser exibido na Tela. 

from PySide6.QtGui import QIcon
# PARA CRIAR O ICONE. 
from PySide6.QtWidgets import QApplication

from styles import setupTheme

from variables import WINDOW_ICON_PATH
# CAMINHO PARA ACESSAR O ICONE - PUXANDO DE VARIABLES (ARQUIVO)


if __name__ == '__main__':
    # CRIA A APLICACAO:
    app = QApplication(sys.argv)
    setupTheme(app)
    window = MainWindow()

    # DEFINE O ICONE:
    icon = QIcon(str(WINDOW_ICON_PATH))
    window.setWindowIcon(icon) # DEFINO O ICONE PARA A JANELA
    app.setWindowIcon(icon) # DEFINO O ICONE PARA A APP. 

    # INFORMACOES:
    info = Info('Sua conta')
    window.addWidgetToVLayout(info)

    # DISPLAY:
    display = Display()
    window.addWidgetToVLayout(display)

    # GRID: JA ESTA CONFIGURANDO TODOS OS BOTOES
    # EXCLUINDO A NECESSIDADE DO BLOCO ABAIXO (BUTTON)
    buttonsGrid = ButtonsGrid(display, info, window)
    window.vLayout.addLayout(buttonsGrid)

    # # BUTTON:
    # button = Button('Texto do botão')
    # window.addToVLayout(button)

    # button2 = Button('Texto do botão')
    # window.addToVLayout(button)

    # EXECUTA TUDO:
    window.adjustFixedSize()
    window.show()
    app.exec()