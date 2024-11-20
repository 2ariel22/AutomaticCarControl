from DAO.Login.ApiLogin import ApiLogin

api = ApiLogin()

response = api.login("1234","1234")
print(response)