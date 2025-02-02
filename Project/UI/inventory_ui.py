import sys
import requests
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QTableWidget, QTableWidgetItem, QVBoxLayout, QWidget, QPushButton, QLineEdit, QMessageBox
)


class InventoryApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Inventory Management")
        self.setGeometry(100, 100, 600, 400)

        # Main widget and layout
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)

        # Table to display inventory
        self.table = QTableWidget()
        self.table.setColumnCount(2)
        self.table.setHorizontalHeaderLabels(["Item", "Quantity"])
        self.layout.addWidget(self.table)

        # Input fields for adding/updating items
        self.item_name_input = QLineEdit()
        self.item_name_input.setPlaceholderText("Item Name")
        self.layout.addWidget(self.item_name_input)

        self.item_quantity_input = QLineEdit()
        self.item_quantity_input.setPlaceholderText("Quantity")
        self.layout.addWidget(self.item_quantity_input)

        # Buttons
        self.add_button = QPushButton("Add Item")
        self.add_button.clicked.connect(self.add_item)
        self.layout.addWidget(self.add_button)

        self.remove_button = QPushButton("Remove Item")
        self.remove_button.clicked.connect(self.remove_item)
        self.layout.addWidget(self.remove_button)

        self.update_button = QPushButton("Update Quantity")
        self.update_button.clicked.connect(self.update_quantity)
        self.layout.addWidget(self.update_button)

        # Buy and Return Buttons
        self.buy_button = QPushButton("Buy Item")
        self.buy_button.clicked.connect(self.buy_item)
        self.layout.addWidget(self.buy_button)

        self.return_button = QPushButton("Return Item")
        self.return_button.clicked.connect(self.return_item)
        self.layout.addWidget(self.return_button)

        # Load inventory on startup
        self.load_inventory()

    def load_inventory(self):
        """Fetch and display inventory from the server."""
        try:
            response = requests.get("http://127.0.0.1:5000/get-inventory")
            if response.status_code == 200:
                inventory = response.json()
                self.table.setRowCount(len(inventory))
                for i, item in enumerate(inventory):
                    self.table.setItem(i, 0, QTableWidgetItem(item["name"]))
                    self.table.setItem(i, 1, QTableWidgetItem(str(item["quantity"])))
            else:
                QMessageBox.warning(self, "Error", "Failed to fetch inventory.")
        except requests.exceptions.RequestException as e:
            QMessageBox.critical(self, "Error", f"Failed to connect to server: {e}")

    def add_item(self):
        """Add a new item to the inventory."""
        name = self.item_name_input.text()
        quantity = self.item_quantity_input.text()

        if not name or not quantity:
            QMessageBox.warning(self, "Error", "Item name and quantity are required.")
            return

        try:
            quantity = int(quantity)
        except ValueError:
            QMessageBox.warning(self, "Error", "Quantity must be a valid number.")
            return

        try:
            response = requests.post(
                "http://127.0.0.1:5000/add-item",
                json={"name": name, "quantity": quantity},
            )
            if response.status_code == 200:
                self.load_inventory()  # Refresh the inventory table
                QMessageBox.information(self, "Success", "Item added successfully!")
            else:
                QMessageBox.warning(self, "Error", f"Server error: {response.text}")
        except requests.exceptions.RequestException as e:
            QMessageBox.critical(self, "Error", f"Failed to connect to server: {e}")

    def remove_item(self):
        """Remove an item from the inventory."""
        name = self.item_name_input.text()

        if not name:
            QMessageBox.warning(self, "Error", "Item name is required.")
            return

        try:
            response = requests.post(
                "http://127.0.0.1:5000/remove-item",
                json={"name": name},
            )
            if response.status_code == 200:
                self.load_inventory()  # Refresh the inventory table
                QMessageBox.information(self, "Success", "Item removed successfully!")
            else:
                QMessageBox.warning(self, "Error", f"Server error: {response.text}")
        except requests.exceptions.RequestException as e:
            QMessageBox.critical(self, "Error", f"Failed to connect to server: {e}")

    def update_quantity(self):
        """Update the quantity of an item in the inventory."""
        name = self.item_name_input.text()
        quantity = self.item_quantity_input.text()

        if not name or not quantity:
            QMessageBox.warning(self, "Error", "Item name and quantity are required.")
            return

        try:
            quantity = int(quantity)
        except ValueError:
            QMessageBox.warning(self, "Error", "Quantity must be a valid number.")
            return

        try:
            response = requests.post(
                "http://127.0.0.1:5000/update-quantity",
                json={"name": name, "new_quantity": quantity},
            )
            if response.status_code == 200:
                self.load_inventory()  # Refresh the inventory table
                QMessageBox.information(self, "Success", "Quantity updated successfully!")
            else:
                QMessageBox.warning(self, "Error", f"Server error: {response.text}")
        except requests.exceptions.RequestException as e:
            QMessageBox.critical(self, "Error", f"Failed to connect to server: {e}")

    def buy_item(self):
        """Buy an item (decrease quantity by 1)."""
        name = self.item_name_input.text()

        if not name:
            QMessageBox.warning(self, "Error", "Item name is required.")
            return

        try:
            response = requests.post(
                "http://127.0.0.1:5000/buy-item",
                json={"name": name},
            )
            if response.status_code == 200:
                self.load_inventory()  # Refresh the inventory table
                QMessageBox.information(self, "Success", "Item purchased successfully!")
            else:
                QMessageBox.warning(self, "Error", f"Server error: {response.text}")
        except requests.exceptions.RequestException as e:
            QMessageBox.critical(self, "Error", f"Failed to connect to server: {e}")

    def return_item(self):
        """Return an item (increase quantity by 1)."""
        name = self.item_name_input.text()

        if not name:
            QMessageBox.warning(self, "Error", "Item name is required.")
            return

        try:
            response = requests.post(
                "http://127.0.0.1:5000/return-item",
                json={"name": name},
            )
            if response.status_code == 200:
                self.load_inventory()  # Refresh the inventory table
                QMessageBox.information(self, "Success", "Item returned successfully!")
            else:
                QMessageBox.warning(self, "Error", f"Server error: {response.text}")
        except requests.exceptions.RequestException as e:
            QMessageBox.critical(self, "Error", f"Failed to connect to server: {e}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = InventoryApp()
    window.show()
    sys.exit(app.exec_())