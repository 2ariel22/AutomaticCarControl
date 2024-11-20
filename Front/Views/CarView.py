import flet as ft
from dataclasses import dataclass
from typing import Dict, List, Optional
from pymongo import MongoClient
from bson import ObjectId
from datetime import datetime

@dataclass
class Car:
    id: str
    name: str
    image_url: str
    model: str
    year: str
    placa: str
    operario: str
    num_motor: str
    km: str
    observaciones: str
    created_at: str

class CarDatabase:
    def __init__(self, db_uri="mongodb://localhost:27017/", db_name="vehicle_management"):
        self.client = MongoClient(db_uri)
        self.db = self.client[db_name]
        self.cars_collection = self.db["cars"]

    def get_all_cars(self):
        try:
            cars = self.cars_collection.find()
            return [{**car, "id": str(car["_id"])} for car in cars]
        except Exception as e:
            print(f"Error getting cars: {e}")
            return []

    def add_car(self, car_data):
        try:
            car_data["created_at"] = datetime.now().isoformat()
            result = self.cars_collection.insert_one(car_data)
            return str(result.inserted_id)
        except Exception as e:
            print(f"Error adding car: {e}")
            return None

    def update_car(self, car_id, car_data):
        try:
            result = self.cars_collection.update_one(
                {"_id": ObjectId(car_id)},
                {"$set": car_data}
            )
            return result.modified_count > 0
        except Exception as e:
            print(f"Error updating car: {e}")
            return False

    def delete_car(self, car_id):
        try:
            result = self.cars_collection.delete_one({"_id": ObjectId(car_id)})
            return result.deleted_count > 0
        except Exception as e:
            print(f"Error deleting car: {e}")
            return False

class CarView:
    def __init__(self, page: ft.Page):
        self.page = page
        self.car_list: List[Car] = []
        self.car_list_row: Optional[ft.Row] = None
        self.selected_car: Optional[Car] = None
        self.db = CarDatabase()
        self.entryList: Dict[str, ft.TextField] = {
            "name": ft.TextField(
                label="Nombre del carro",
                hint_text="Ingrese el nombre del carro"
            ),
            "img": ft.TextField(
                label="URL de la imagen",
                hint_text="Ingrese la URL de la imagen"
            ),
            "model": ft.TextField(
                label="Modelo del carro",
                hint_text="Ingrese el modelo"
            ),
            "year": ft.TextField(
                label="Año del carro",
                hint_text="Ingrese el año"
            ),
            "placa": ft.TextField(
                label="Placa del carro",
                hint_text="Ingrese la placa"
            ),
            "operario": ft.TextField(
                label="Operario del carro",
                hint_text="Ingrese el operario"
            ),
            "num_motor": ft.TextField(
                label="Número del motor",
                hint_text="Ingrese el número del motor"
            ),
            "km": ft.TextField(
                label="Kilometraje",
                hint_text="Ingrese el kilometraje"
            ),
            "observaciones": ft.TextField(
                label="observaciones",
                hint_text="Ingrese las observaciones",
                multiline=True,
                max_lines=3
            )
        }
        self.load_cars()

    def load_cars(self):
        """Load cars from MongoDB."""
        try:
            cars_data = self.db.get_all_cars()
            self.car_list = [
                Car(
                    id=car["id"],
                    name=car["name"],
                    image_url=car["image_url"],
                    model=car["model"],
                    year=car["year"],
                    placa=car["placa"],
                    operario=car["operario"],
                    num_motor=car["num_motor"],
                    km=car["km"],
                    observaciones=car["observaciones"],
                    created_at=car["created_at"]
                )
                for car in cars_data
            ]
            self.update_car_list()
            self.page.update()
        except Exception as e:
            self.show_error_dialog(f"Error loading cars: {str(e)}")

    def validate_inputs(self) -> tuple[bool, str]:
        """Validate all input fields."""
        for field_name, field in self.entryList.items():
            if not field .value or field.value.strip() == "":
                return False, f"El campo {field_name} es requerido"
        return True, ""

    def fill_form_with_car(self, car: Car):
        """Fill form fields with car data."""
        self.entryList["name"].value = car.name
        self.entryList["img"].value = car.image_url
        self.entryList["model"].value = car.model
        self.entryList["year"].value = car.year
        self.entryList["placa"].value = car.placa
        self.entryList["operario"].value = car.operario
        self.entryList["num_motor"].value = car.num_motor
        self.entryList["km"].value = car.km
        self.entryList["observaciones"].value = car.observaciones

    def clear_inputs(self):
        """Clear all input fields."""
        for entry in self.entryList.values():
            entry.value = ""
        self.selected_car = None

    def close_dialog(self, e):
        """Close the current dialog."""
        self.page.dialog.open = False
        self.page.update()

    def show_car_details(self, car: Car, e):
        """Show detailed information about a car."""
        self.page.dialog = ft.AlertDialog(
            modal=True,
            title=ft.Text("Detalles del Vehículo"),
            content=ft.Container(
                content=ft.Column([
                    ft.Image(
                        src=car.image_url,
                        width=200,
                        height=200,
                        fit=ft.ImageFit.CONTAIN,
                    ),
                    ft.Text(f"ID: {car.id}", size=14),
                    ft.Text(f"Nombre: {car.name}", size=16, weight="bold"),
                    ft.Text(f"Modelo: {car.model}"),
                    ft.Text(f"Año: {car.year}"),
                    ft.Text(f"Placa: {car.placa}"),
                    ft.Text(f"Operario: {car.operario}"),
                    ft.Text(f"Número de Motor: {car.num_motor}"),
                    ft.Text(f"Kilometraje: {car.km}"),
                    ft.Text(f"obeservaciones: {car.observaciones}"),
                    ft.Text(f"Creado: {car.created_at}", size=12, color=ft.colors.GREY_400),
                ],
                spacing=10,
                scroll="auto",
                ),
                padding=10,
            ),
            actions=[
                ft.TextButton("Cerrar", on_click=self.close_dialog)
            ]
        )
        self.page.dialog.open = True
        self.page.update()

    def add_or_update_car(self, e):
        """Add a new car or update existing car."""
        is_valid, error_message = self.validate_inputs()
        
        if not is_valid:
            self.show_error_dialog(error_message)
            return

        try:
            car_data = {
                "name": self.entryList["name"].value,
                "image_url": self.entryList["img"].value,
                "model": self.entryList["model"].value,
                "year": self.entryList["year"].value,
                "placa": self.entryList["placa"].value,
                "operario": self.entryList["operario"].value,
                "num_motor": self.entryList["num_motor"].value,
                "km": self.entryList["km"].value,
                "observaciones":self.entryList["observaciones"].value
            }

            if self.selected_car:
                # Update existing car
                success = self.db.update_car(self.selected_car.id, car_data)
                message = "Car updated successfully" if success else "Error updating car"
            else:
                # Create new car
                car_id = self.db.add_car(car_data)
                success = car_id is not None
                message = "Car added successfully" if success else "Error adding car"

            if success:
                self.load_cars()
                self.clear_inputs()
                self.page.dialog.open = False
                self.page.update()
            else:
                self.show_error_dialog(message)
                
        except Exception as ex:
            self.show_error_dialog(f"Error: {str(ex)}")
    def delete_car(self, car: Car):
        """Delete a car."""
        try:
            success = self.db.delete_car(car.id)
            if success:
                self.load_cars()
                self.page.dialog.open = False
                self.page.update()
            else:
                self.show_error_dialog("Error al eliminar el carro")
        except Exception as ex:
            self.show_error_dialog(f"Error: {str(ex)}")

    def show_delete_confirmation(self, car: Car):
        """Show delete confirmation dialog."""
        self.page.dialog = ft.AlertDialog(
            modal=True,
            title=ft.Text("Confirmar eliminación"),
            content=ft.Text(f"¿Está seguro que desea eliminar el carro {car.name}?"),
            actions=[
                ft.TextButton("Cancelar", on_click=self.close_dialog),
                ft.ElevatedButton(
                    "Eliminar",
                    color="error",
                    on_click=lambda e: self.delete_car(car)
                )
            ]
        )
        self.page.dialog.open = True
        self.page.update()

    def show_error_dialog(self, message: str):
        """Show error dialog with custom message."""
        self.page.dialog = ft.AlertDialog(
            modal=True,
            title=ft.Text("Error"),
            content=ft.Text(message),
            actions=[
                ft.TextButton("Cerrar", on_click=self.close_dialog)
            ]
        )
        self.page.dialog.open = True
        self.page.update()

    def create_car_card(self, car: Car) -> ft.Card:
        """Create a card widget for a car."""
        return ft.Card(
            content=ft.Container(
                padding=10,
                content=ft.Column([
                    ft.Text(f"Nombre: {car.name}", 
                            weight="bold", 
                            size=16,
                            expand=True
                        ),
                    ft.Text(f"Modelo: {car.model}"),
                    ft.Text(f"Año: {car.year}"),
                    ft.Text(f"Placa: {car.placa}"),
                    ft.Row([
                        ft.IconButton(
                            icon=ft.icons.INFO,
                            icon_color="blue",
                            tooltip="Ver detalles",
                            on_click=lambda e: self.show_car_details(car, e)
                        ),
                        ft.IconButton(
                            icon=ft.icons.EDIT,
                            icon_color="green",
                            tooltip="Editar",
                            on_click=lambda e: self.edit_car(car)
                        ),
                        ft.IconButton(
                            icon=ft.icons.DELETE,
                            icon_color="red",
                            tooltip="Eliminar",
                            on_click=lambda e: self.show_delete_confirmation(car)
                        )
                    ]),
                    ft.Image(
                        src=car.image_url,
                        width=100,
                        height=100,
                        fit=ft.ImageFit.CONTAIN,
                        repeat=ft.ImageRepeat.NO_REPEAT
                    ),
                    
                ],
                alignment=ft.MainAxisAlignment.START,
                spacing=10
                )
            ),
            width=200,
            height=300
        )

    def edit_car(self, car: Car):
        """Open dialog for editing a car."""
        self.selected_car = car
        self.fill_form_with_car(car)
        self.open_dialog(None)

    def update_car_list(self):
        """Update the car list display."""
        if not self.car_list_row:
            return
            
        car_controls = [self.create_car_card(car) for car in self.car_list]
        self.car_list_row.controls = car_controls

    def open_dialog(self, e):
        """Open dialog for adding/editing a car."""
        title = "Editar carro" if self.selected_car else "Agregar nuevo carro"
        self.page.dialog = ft.AlertDialog(
            modal=True,
            title=ft.Text(title),
            content=ft.Column(
                controls=list(self.entryList.values()),
                tight=True,
                scroll=True,
                height=400
            ),
            actions=[
                ft.TextButton("Cancelar", on_click=self.close_dialog),
                ft.ElevatedButton(
                    "Guardar", 
                    on_click=self.add_or_update_car
                )
            ]
        )
        self.page.dialog.open = True
        self.page.update()
    def back(self, e):
        """Go back to the previous view."""
        self.page.views.pop()
        self.page.update()
    def getCarView(self) -> ft.View:
        """Get the main view of the car management system."""
        self.car_list_row = ft.Row(
            wrap=True,
            spacing=10,
            scroll="auto"
        )
        self.load_cars()
        
        return ft.View(
            route="/",
            controls=[
                ft.AppBar(
                    title=ft.Text("Sistema de Gestión de Vehículos"),
                    center_title=True,
                    bgcolor=ft.colors.SURFACE_VARIANT,
                    leading=ft.IconButton(
                        icon=ft.icons.ARROW_BACK,
                        on_click=self.back
                    )
                ),
                ft.Container(
                    content=ft.Column([
                        ft.ElevatedButton(
                            text="Agregar Carro",
                            on_click=self.open_dialog,
                            icon=ft.icons.ADD
                        ),
                        self.car_list_row
                    ]),
                    padding=20
                )
            ],
            padding=20,
            spacing=20
        )