from DAO.Login.ApiLogin import ApiLogin

api = ApiLogin()


payload= {
    "nit":"1234",
    "password":"1234",
    "name":"1234",
    "cedula":"1234",
    "telefono":"1234",
    "correo":"1234"

}

respomse = api.register(payload)

print(respomse)


