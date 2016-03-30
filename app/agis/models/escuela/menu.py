from agiscore.gui.mic import Accion
from agiscore.gui.escuela import escuela_menu

if not request.ajax:
    response.menu += escuela_menu()
