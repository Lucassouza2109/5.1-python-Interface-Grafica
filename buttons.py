import math
# MODULO PARA TRABALHAR COM QUESTOES MATEMATICAS.

from typing import TYPE_CHECKING
# EVITA A IMPORTACAO CIRCULAR DOS MODULOS. 

from PySide6.QtCore import Slot

from PySide6.QtWidgets import QGridLayout, QPushButton
# IMPORTO DE PYSIDE - CLASSE :  LAYOUT | BUTTON. 

from utils import converToNumber, isEmpty, isNumOrDot, isValidNumber

from variables import MEDIUM_FONT_SIZE

# ----------------------------------

if TYPE_CHECKING:
    from display import Display
    from info import Info
    from main_window import MainWindow

# ----------------------------------

class Button(QPushButton):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.configStyle()

    def configStyle(self):
        font = self.font() # FONTE ATUAL
        font.setPixelSize(MEDIUM_FONT_SIZE) # REDEFINO A FONTE ATUAL 
        self.setFont(font) # APLICO A FONTE MODIFICADA
        self.setMinimumSize(75, 75) # TAMANHO MINIMO = LARGURA | ALTURA
        # self.setProperty('cssClass', 'specialButton')
        # DEFINO UMA PROPRIEDADE PERSONALIZADA
        # self.setCheckable(True)
        

# ----------------------------------

class ButtonsGrid(QGridLayout):
    def __init__(
            self, display: 'Display', info: 'Info', window: 'MainWindow',
            *args, **kwargs
    ) -> None:
        super().__init__(*args, **kwargs)

        # ABAIXO MASCARA UTILIZADA PARA CONFIGURAR A GRID DA CALCULADORA
        self._gridMask = [ 
            ['C', 'D', '^', '/'],
            ['7', '8', '9', '*'],
            ['4', '5', '6', '-'],
            ['1', '2', '3', '+'],
            ['N',  '0', '.', '='],
        ]

        self.display = display
        self.info = info
        self.window = window
        self._equation = ''
        self._equationInitialValue = 'Sua conta'
        self._left = None
        self._right = None
        self._op = None

        self.equation = self._equationInitialValue
        self._makeGrid()

    @property
    def equation(self):
        return self._equation

    @equation.setter
    def equation(self, value):
        self._equation = value
        self.info.setText(value)

  
# ----------------------------------

    def _makeGrid(self):
        # CONECTANDO SIGNAL EMITIDO EM DISPLAY.
        self.display.eqPressed.connect(self._eq)
        self.display.delPressed.connect(self._backspace)
        self.display.clearPressed.connect(self._clear)
        self.display.inputPressed.connect(self._insertToDisplay)
        self.display.operatorPressed.connect(self._configLeftOp)

        for rowNumber, rowData in enumerate(self._gridMask):
            # PARA NUMERO DA LINHA | CONTEUDO DA LINHA ...
            for colNumber, buttonText in enumerate(rowData):
            # VOU PERCORRER CADA INDICE | CONTEUDO DE CADA LINHA (ROWDATA)
                    button = Button(buttonText)
                    # CRIO UM BOTAO PASSANDO O CONTEUDO = buttonText

                    if not isNumOrDot(buttonText) and not isEmpty(buttonText):
                    # SE NAO FOR NUMERO OU PONTO E NAO FOR BOTAO VAZIO 
                    # CONFIGURA O BOTAO CONFORME PERSONALIZACAO ABAIXO :
                        button.setProperty('cssClass', 'specialButton')
                        self._configSpecialButton(button)

                    self.addWidget(button, rowNumber, colNumber)
                    # ADICIONA O BOTAO AO LAYOUT - RESPEITANDO rowNumber | colNumber.
                    
                # Chama o método _makeSlot para criar um slot (função) que chama _insertButtonTextToDisplay com o button como argumento. button é o argumento que será passado para self._insertButtonTextToDisplay (FUNCAO).
                    slot = self._makeSlot(self._insertToDisplay, buttonText)
                    self._connectButtonClicked(button, slot)

# ----------------------------------

    # ABAIXO ESTOU CONECTANDO O CLICK DO BOTAO A UMA FUNCAO. 
    def _connectButtonClicked(self, button, slot):
        button.clicked.connect(slot)  # type: ignore
        # Conecta o sinal clicked do botão ao buttonSlot.

# ----------------------------------

    # CONFIG. BOTOES ESPECIAIS 
    def _configSpecialButton(self, button):
        text = button.text()

        if text == 'C':
            self._connectButtonClicked(button, self._clear)

        # D = Delete.
        if text == 'D':
            self._connectButtonClicked(button, self.display.backspace)

        if text == 'N':
            self._connectButtonClicked(button, self._invertNumber)

        if text in '+-/*^':
            self._connectButtonClicked(
                button,
                self._makeSlot(self._configLeftOp, text)
            )

        if text == '=':
            self._connectButtonClicked(button, self._eq)

    @Slot()
    def _makeSlot(self, func, *args, **kwargs):
        @ Slot(bool)
        def realSlot(_):
            func(*args, **kwargs)
        return realSlot

    @Slot()
    def _invertNumber(self):
        displayText = self.display.text()

        if not isValidNumber(displayText):
            return

        number = converToNumber(displayText) * -1
        self.display.setText(str(number))


# ----------------------------------

    # EXIBINDO CONTEUDO DO BOTAO CLICADO NO DISPLAY.
    @Slot()
    def _insertToDisplay(self, text):
        newDisplayValue = self.display.text() + text

        if not isValidNumber(newDisplayValue):
            return

        self.display.insert(text)
        self.display.setFocus()

# ----------------------------------

    # METODO CRIADO PARA LIMPAR DISPLAY.
    @Slot()
    def _clear(self): 
        self._left = None
        self._right = None
        self._op = None
        self.equation = self._equationInitialValue
        self.display.clear()
        self.display.setFocus()
        
# ----------------------------------

    # METODO PARA QUANDO DEFINIR O OPERADOR - LADO DIREITO DO CALCULO
    @Slot()
    def _configLeftOp(self, text): 
        displayText = self.display.text()  # Deverá ser meu número _left
        self.display.clear()  # Limpa o display
        self.display.setFocus()

        # Se a pessoa clicou no operador sem configurar qualquer número ANTES.
        if not isValidNumber(displayText) and self._left is None:
            self._showError('Você não digitou nada.')
            return

        # Se houver algo no número da esquerda,não fazemos nada. 
        # Aguardaremos o número da direita.
        if self._left is None:
            self._left = converToNumber(displayText)

        self._op = text
        self.equation = f'{self._left} {self._op} ??'

# ------------------------------------

    # METODO PARA SINAL DE =
    @Slot()
    def _eq(self):
        displayText = self.display.text()

        if not isValidNumber(displayText) or self._left is None:
            self._showError('Conta incompleta.')
            return

        self._right = converToNumber(displayText)
        self.equation = f'{self._left} {self._op} {self._right}'
        result = 'error'

        try:
            if '^' in self.equation and isinstance(self._left, (float, int)):
                result = math.pow(self._left, self._right)
                result = converToNumber(str(result))
            else:
                result = eval(self.equation)
                # EVAL = Avalia uma string como codigo Python.

        except ZeroDivisionError:
            self._showError('Divisão por zero.')

        except OverflowError:
            self._showError('Essa conta não pode ser realizada.')

        self.display.clear()
        self.info.setText(f'{self.equation} = {result}')
        self._left = result
        self._right = None
        self.display.setFocus()


        if result == 'error':
            self._left = None

 #-----------------------------------

    # DEFININDO FOCO NO DISPLAY.
    @Slot()
    def _backspace(self):
        self.display.backspace()
        self.display.setFocus()

# -----------------------------------

    def _makeDialog(self, text):
        msgBox = self.window.makeMsgBox()
        msgBox.setText(text)
        return msgBox

    def _showError(self, text):
        msgBox = self._makeDialog(text)
        msgBox.setIcon(msgBox.Icon.Critical)
        msgBox.exec()
        self.display.setFocus()

    def _showInfo(self, text):
        msgBox = self._makeDialog(text)
        msgBox.setIcon(msgBox.Icon.Information)
        msgBox.exec()
        self.display.setFocus()