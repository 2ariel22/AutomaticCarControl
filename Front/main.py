from flet import *

from Views.Inicio import Inicio

def main(page: Page):
    vista = Inicio(page).getInicioView()
    page.views.append(vista)
    page.update()

    

#app(target=main)
app(target=main, view=AppView.WEB_BROWSER)