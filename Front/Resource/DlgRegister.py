from flet import *
from DAO.Login.ApiLogin import ApiLogin
class DlgRegister:
    def __init__(self, page: Page):
        self.page = page
        self.api = ApiLogin()

    def getDlgRegister(self):
        entryNit = TextField(label="NIT", helper_text="Por favor ingrese su NIT")
        entryPassword = TextField(label="Contraseña", password=True, helper_text="Por favor ingrese su contraseña")
        entryName = TextField(label="Nombre", helper_text="Por favor ingrese su nombre")
        entryCedula = TextField(label="Cédula", helper_text="Por favor ingrese su cédula")
        entryTelefono = TextField(label="Teléfono", helper_text="Por favor ingrese su teléfono")
        entryCorreo = TextField(label="Correo", helper_text="Por favor ingrese su correo")

        def register_user(e):
            payload = {
                "nit": entryNit.value,
                "password": entryPassword.value,
                "name": entryName.value,
                "cedula": entryCedula.value,
                "telefono": entryTelefono.value,
                "correo": entryCorreo.value,
            }
            result = self.api.register(payload)
            if result["success"]:
                self.page.snack_bar = SnackBar(Text("Usuario registrado exitosamente"), bgcolor="green", open=True)
                
            else:
                self.page.snack_bar = SnackBar(Text(f"Error: {result['error']}"), bgcolor="red", open=True)
            self.page.update()

        dlg = AlertDialog(
            title=Text("Registrar Usuario", size=20, weight="bold"),
            content=Column(
                controls=[
                    entryNit,
                    entryPassword,
                    entryName,
                    entryCedula,
                    entryTelefono,
                    entryCorreo,
                ],
                tight=True,
                spacing=10,
            ),
            actions=[
                
                ElevatedButton("Registrar", on_click=register_user),
            ],
            actions_alignment="end",
        )
        return dlg
