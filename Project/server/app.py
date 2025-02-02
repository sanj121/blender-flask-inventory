from flask import Flask, request, jsonify
import sqlite3
import time

app = Flask(__name__)

# Helper function to simulate delay
def simulate_delay():
    time.sleep(10)

# Initialize the SQLite database
def init_db():
    conn = sqlite3.connect('inventory.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS inventory (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name TEXT UNIQUE NOT NULL,
                        quantity INTEGER NOT NULL)''')
    conn.commit()
    conn.close()

# Call the init_db function when the app starts
init_db()

@app.route('/')
def home():
    return "Hello, Flask is working!"

@app.route('/transform', methods=['POST'])
def transform():
    # Receive transform data from Blender (position, rotation, scale)
    data = request.json
    print("Transform Data:", data)
    simulate_delay()
    return jsonify({"message": "Transform data received successfully!"}), 200

@app.route('/translation', methods=['POST'])
def translation():
    # Receive only position data
    data = request.json
    print("Translation Data:", data)
    simulate_delay()
    return jsonify({"message": "Translation data received successfully!"}), 200

@app.route('/rotation', methods=['POST'])
def rotation():
    # Receive only rotation data
    data = request.json
    print("Rotation Data:", data)
    simulate_delay()
    return jsonify({"message": "Rotation data received successfully!"}), 200

@app.route('/scale', methods=['POST'])
def scale():
    # Receive only scale data
    data = request.json
    print("Scale Data:", data)
    simulate_delay()
    return jsonify({"message": "Scale data received successfully!"}), 200

@app.route('/file-path', methods=['GET'])
def file_path():
    # Return the DCC file path (dummy path for now)
    return jsonify({"file_path": "/path/to/your/blender/file.blend"}), 200

@app.route('/add-item', methods=['POST'])
def add_item():
    data = request.json
    name = data.get("name")
    quantity = data.get("quantity", 1)

    # Input validation
    if not name or not isinstance(quantity, int):
        return jsonify({"error": "Invalid input. 'name' and 'quantity' are required."}), 400

    try:
        conn = sqlite3.connect('inventory.db')
        cursor = conn.cursor()
        cursor.execute("INSERT INTO inventory (name, quantity) VALUES (?, ?)", (name, quantity))
        conn.commit()
    except sqlite3.IntegrityError:
        return jsonify({"error": f"Item '{name}' already exists."}), 400
    except sqlite3.Error as e:
        return jsonify({"error": f"Database error: {str(e)}"}), 500
    finally:
        conn.close()

    simulate_delay()
    return jsonify({"message": f"Item '{name}' added with quantity {quantity}."}), 200

@app.route('/remove-item', methods=['POST'])
def remove_item():
    data = request.json
    name = data.get("name")

    # Input validation
    if not name:
        return jsonify({"error": "Invalid input. 'name' is required."}), 400

    try:
        conn = sqlite3.connect('inventory.db')
        cursor = conn.cursor()
        cursor.execute("DELETE FROM inventory WHERE name = ?", (name,))
        conn.commit()

        # Check if the item was found and deleted
        if cursor.rowcount == 0:
            return jsonify({"error": f"Item '{name}' not found."}), 404
    except sqlite3.Error as e:
        return jsonify({"error": f"Database error: {str(e)}"}), 500
    finally:
        conn.close()

    simulate_delay()
    return jsonify({"message": f"Item '{name}' removed."}), 200

@app.route('/buy-item', methods=['POST'])
def buy_item():
    data = request.json
    name = data.get("name")

    if not name:
        return jsonify({"error": "Item name is required."}), 400

    try:
        conn = sqlite3.connect('inventory.db')  # Use the correct path
        cursor = conn.cursor()

        # Check if the item exists and has sufficient quantity
        cursor.execute("SELECT quantity FROM inventory WHERE name = ?", (name,))
        item = cursor.fetchone()

        if not item:
            return jsonify({"error": f"Item '{name}' not found."}), 404

        current_quantity = item[0]
        if current_quantity <= 0:
            return jsonify({"error": f"Item '{name}' is out of stock."}), 400

        # Decrease the quantity by 1
        cursor.execute("UPDATE inventory SET quantity = quantity - 1 WHERE name = ?", (name,))
        conn.commit()

        simulate_delay()  # Simulate 10-second delay
        return jsonify({"message": f"Item '{name}' purchased successfully!"}), 200
    except sqlite3.Error as e:
        return jsonify({"error": f"Database error: {str(e)}"}), 500
    finally:
        conn.close()

@app.route('/return-item', methods=['POST'])
def return_item():
    data = request.json
    name = data.get("name")

    if not name:
        return jsonify({"error": "Item name is required."}), 400

    try:
        conn = sqlite3.connect('inventory.db')  # Use the correct path
        cursor = conn.cursor()

        # Check if the item exists
        cursor.execute("SELECT quantity FROM inventory WHERE name = ?", (name,))
        item = cursor.fetchone()

        if not item:
            return jsonify({"error": f"Item '{name}' not found."}), 404

        # Increase the quantity by 1
        cursor.execute("UPDATE inventory SET quantity = quantity + 1 WHERE name = ?", (name,))
        conn.commit()

        simulate_delay()  # Simulate 10-second delay
        return jsonify({"message": f"Item '{name}' returned successfully!"}), 200
    except sqlite3.Error as e:
        return jsonify({"error": f"Database error: {str(e)}"}), 500
    finally:
        conn.close()

@app.route('/update-quantity', methods=['POST'])
def update_quantity():
    data = request.json
    name = data.get("name")
    new_quantity = data.get("new_quantity")

    # Input validation
    if not name or not isinstance(new_quantity, int):
        return jsonify({"error": "Invalid input. 'name' and 'new_quantity' are required."}), 400

    try:
        conn = sqlite3.connect('inventory.db')
        cursor = conn.cursor()
        cursor.execute("UPDATE inventory SET quantity = ? WHERE name = ?", (new_quantity, name))
        conn.commit()

        # Check if the item was found and updated
        if cursor.rowcount == 0:
            return jsonify({"error": f"Item '{name}' not found."}), 404
    except sqlite3.Error as e:
        return jsonify({"error": f"Database error: {str(e)}"}), 500
    finally:
        conn.close()

    simulate_delay()
    return jsonify({"message": f"Item '{name}' quantity updated to {new_quantity}."}), 200

@app.route('/get-inventory', methods=['GET'])
def get_inventory():
    try:
        conn = sqlite3.connect('inventory.db')
        cursor = conn.cursor()
        cursor.execute("SELECT name, quantity FROM inventory")
        items = cursor.fetchall()
        conn.close()

        # Format the inventory data as a list of dictionaries
        inventory_list = [{"name": item[0], "quantity": item[1]} for item in items]
        return jsonify(inventory_list), 200
    except sqlite3.Error as e:
        return jsonify({"error": f"Database error: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)