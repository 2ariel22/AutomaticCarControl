from flet import *
from Resource.DlgRegister import DlgRegister
from Views.CarView import CarView
from DAO.Login.ApiLogin import ApiLogin

class Inicio():
    def __init__(self, page: Page):
        self.page = page
        self.dlgRegister = DlgRegister(page)
        self.carView = CarView(page)
        self.entryPass = None
        self.entryNit = None
        self.apiLogin = ApiLogin()

    def registerButton(self,e):
        alert = self.dlgRegister.getDlgRegister()
        self.page.open(alert)
    
    def loginButton(self, e):
        data = self.apiLogin.login(self.entryNit.value,self.entryPass.value)
        print(data)
        if(data):
            print("Bienvenido")
            vista = self.carView.getCarView()
            self.page.views.append(vista)
            self.page.update()
       

    def getInicioView(self):
        
        title = Text(value="Automatic Maintenance")
        buttonRegister = ElevatedButton(text="Register",on_click= self.registerButton)
        navBar = Row(
            controls=[
                Container(padding=10),
                title,
                buttonRegister
            ],
            alignment= MainAxisAlignment.SPACE_BETWEEN
        )   

        about = Container(content=Text(value="Nuestra aplicación está diseñada para identificar y notificar automáticamente sobre los mantenimientos necesarios del automóvil. Además, envía alertas preventivas cuando una pieza está cerca de fallar o requiere ser reemplazada, brindando seguridad y eficiencia a tus trayectos.")
                          ,expand=2)
        
        self.entryNit = TextField(
            #value="admin",
            label="NIT",
            helper_text="por favor ingrese su NIT"
        )

        self.entryPass = TextField(
            #value="1234",
            label="Pass",
            helper_text="por favor ingrese su Pass",

        )

        buttonSend = ElevatedButton(text="Send" ,on_click=self.loginButton)

        login = Row(
            controls=[
                Container(padding=10,expand=1),
                Column(
                    controls=[
                        Text(value="Login"),
                        self.entryNit,
                        self.entryPass,
                        buttonSend
                    ],
                    expand=1
                ),
                Container(padding=10,expand=1)
            ]
        )

        main = Row(
            controls=[
                Container(padding=10,expand=1),
                about,
                Container(padding=10,expand=1)
            ],
            alignment=MainAxisAlignment.SPACE_BETWEEN
        
        )

        return View(
            controls=[
                navBar,
                main,
                Container(padding=20),
                login
            ],
            vertical_alignment=MainAxisAlignment.START,
            horizontal_alignment=CrossAxisAlignment.CENTER
        )

