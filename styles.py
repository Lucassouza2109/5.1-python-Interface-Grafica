# QSS - Estilos do QT for Python
# https://doc.qt.io/qtforpython/tutorials/basictutorial/widgetstyling.html
# Dark Theme
# https://pyqtdarktheme.readthedocs.io/en/latest/how_to_use.html


import qdarktheme 
# print (dir(qdarktheme))
from variables import (DARKER_PRIMARY_COLOR, DARKEST_PRIMARY_COLOR,
                       PRIMARY_COLOR)

qss = f"""
    QPushButton[cssClass="specialButton"] {{
        color: #fff;
        background: {PRIMARY_COLOR};
    }}
    QPushButton[cssClass="specialButton"]:hover {{
        color: #fff;
        background: {DARKER_PRIMARY_COLOR};
    }}
    QPushButton[cssClass="specialButton"]:pressed {{
        color: #fff;
        background: {DARKEST_PRIMARY_COLOR};
    }}
"""

def setupTheme(app):
    # Carregar o tema padrão do qdarktheme
    app.setStyleSheet(qdarktheme.load_stylesheet("dark"))
    # Adicionar o QSS customizado
    app.setStyleSheet(app.styleSheet() + qss)


# def setupTheme():
#     qdarktheme.setup_theme( #type: ignore
#         theme='dark', # TEMA = DARK
#         corner_shape='rounded', # CANTO ARRENDONDADO
#         custom_colors={ # CONFIGURACAO DE COR
#             "[dark]": {
#                 "primary": f"{PRIMARY_COLOR}",
#             },
#             "[light]": {
#                 "primary": f"{PRIMARY_COLOR}",
#             },
#         },
#         additional_qss=qss
#     )