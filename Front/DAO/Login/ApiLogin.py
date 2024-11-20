from pymongo import MongoClient

class ApiLogin:
    def __init__(self, db_uri="mongodb://localhost:27017/", db_name="vehicle_management"):
        self.client = MongoClient(db_uri)
        self.db = self.client[db_name]
        self.users_collection = self.db["users"]  # Asegúrate de que esta colección exista en tu base de datos

    def login(self, nit, passw):
        try:
            # Busca un usuario con el NIT y contraseña proporcionados
            user = self.users_collection.find_one({"nit": nit, "password": passw})
            return True if user else False
        except Exception as e:
            print(f"Error al realizar el login: {e}")
            return False

    def register(self, payload_register):
        try:
            # Inserta un nuevo usuario en la base de datos
            result = self.users_collection.insert_one(payload_register)
            return {"success": True, "inserted_id": str(result.inserted_id)}
        except Exception as e:
            print(f"Error al registrar el usuario: {e}")
            return {"success": False, "error": str(e)}

# Ejemplo de uso
if __name__ == "__main__":
    api = ApiLogin()
    # Intentar login
    print(api.login("123456789", "password123"))
    # Registrar un usuario
    #new_user = {"nit": "123456789", "password": "password123", "name": "Juan Pérez"}
    #print(api.register(new_user))
