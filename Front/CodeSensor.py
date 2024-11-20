import flet as ft
from pymongo import MongoClient

# Conexión a la base de datos MongoDB
class SensorApp:
    def __init__(self, db_uri="mongodb://localhost:27017/", db_name="vehicle_management"):
        self.client = MongoClient(db_uri)
        self.db = self.client[db_name]
        self.sensors_collection = self.db["Sensors"]  # Asegúrate de que esta colección exista en tu base de datos

    def save_sensor_data(self, sensor_data):
        self.sensors_collection.insert_one(sensor_data)

    def build(self, page):
        # Vista de la aplicación Flet
        page.title = "Sensor Data Collection"
        page.vertical_alignment = ft.MainAxisAlignment.START

        # Entradas para los datos de los sensores
        sensor_inputs = {
            "Sensor de temperatura": ft.TextField(label="Sensor de temperatura"),
            "Sensor de vibración": ft.TextField(label="Sensor de vibración"),
            "Sensor de presión": ft.TextField(label="Sensor de presión"),
            "Sensor de nivel": ft.TextField(label="Sensor de nivel"),
            "Sensor de corriente y voltaje": ft.TextField(label="Sensor de corriente y voltaje"),
            "Sensores de desgaste": ft.TextField(label="Sensores de desgaste"),
            "Sensores de rotación": ft.TextField(label="Sensores de rotación"),
            "Sensor de diagnóstico": ft.TextField(label="Sensor de diagnóstico")
        }

        # Función que se ejecuta al presionar el botón "Enviar"
        def on_send_click(e):
            sensor_data = {}
            for sensor_name, input_field in sensor_inputs.items():
                sensor_data[sensor_name] = input_field.value
            self.save_sensor_data(sensor_data)
            page.add(ft.Text("Datos enviados exitosamente."))

        # Crear un botón para enviar los datos
        send_button = ft.ElevatedButton("Enviar", on_click=on_send_click)

        # Agregar los campos de entrada y el botón a la página
        page.add(*sensor_inputs.values(), send_button)

# Ejecutar la aplicación
if __name__ == "__main__":
    app = SensorApp()
    ft.app(target=app.build)
