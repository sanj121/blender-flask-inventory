Python Developer Assessment - DCC Integration

This project demonstrates my ability to integrate Blender with a Flask server and a PyQt/PySide UI to manage object transforms and a simple inventory system. The project consists of three main components:

1.Blender Plugin: Sends object transform data (position, rotation, scale) to the Flask server.

2.Flask Server: Acts as the backend, handling requests from the Blender plugin and the PyQt/PySide UI.

3.PyQt/PySide UI: Manages the inventory stored in a SQLite database.


Table of Contents:
    1.Project Structure

    2.Prerequisites

    3.Setup Instructions
        Blender Plugin
        Flask Server
        PyQt/PySide UI

    4.Usage
        Blender Plugin
        PyQt/PySide UI

    5.Testing

    6.Troubleshooting

    7.Contact



Project Structure:-


PROJECT/
│
├── blender_plugin/               # Blender plugin code
│   └── transform_sender.py        # Blender plugin script
│
├── server/                       # Flask server code
│   ├── app.py                    # Flask server script
│   └── setup_db.py         # Database setup script
│   └── inventory.db              # Database file
│
├── ui/                           # PyQt/PySide UI code
│   └── inventory_ui.py           # PyQt/PySide UI script
│
└── README.md                     # Project documentation



Prerequisites
Before setting up the project, ensure you have the following installed:

1.Blender (version 3.0 or higher)

2.Python (version 3.7 or higher)

3.Flask (pip install flask)

4.PyQt5 or PySide6 (pip install PyQt5 or pip install PySide6)

5.SQLite (usually comes pre-installed with Python)


Setup Instructions
Blender Plugin

1.Copy the transform_sender.py file to your Blender add-ons folder or install it directly in Blender:
Open Blender.

    Go to Edit > Preferences > Add-ons.

    Click Install... and select transform_sender.py.

    Enable the plugin by checking the checkbox next to it.


Flask Server:
1.Navigate to the flask_server folder:
cd path/to/your_project_folder/flask_server

2.Set up the database:
  python setup_db.py

3.Start the Flask server:
  python app.py
  The server will run at http://127.0.0.1:5000

PyQt/PySide UI:

1.Navigate to the ui folder:
    cd path/to/your_project_folder/ui

2.Run the UI script:
    python inventory_ui.py


Usage
Blender Plugin Usage:
1.Open Blender and select an object in the 3D Viewport.
2.In the Transform Sender panel (found in the sidebar under the Transform tab):

        Choose an endpoint (/transform, /translation, /rotation, /scale).

        Click Submit Transform to send the object's transform data to the Flask server.


PyQt/PySide UI Usage
1.Open the UI by running inventory_ui.py.
2.Use the UI to:

          View Inventory: The table displays the current inventory.

          Add Item: Enter the item name and quantity, then click Add Item.

          Remove Item: Enter the item name, then click Remove Item.

          Update Quantity: Enter the item name and new quantity, then click Update Quantity.


Testing:

1.Blender Plugin:

      Send transform data from Blender and verify it is logged by the Flask server.

2.PyQt/PySide UI:

      Add, remove, and update items in the inventory, and verify the changes in the SQLite database.

3.Flask Server:

      Check the server logs to ensure all requests are processed correctly.



Troubleshooting
Blender Plugin Not Showing Up
      Ensure the plugin is installed and enabled in Blender's Add-ons tab.

      Check the Blender System Console for errors.

Flask Server Not Responding
      Ensure the server is running at http://127.0.0.1:5000.

      Check the Flask server logs for errors.

UI Freezing
      Use threading or asynchronous programming to keep the UI responsive.

Database Not Updating
      Verify the SQLite database file (inventory.db) is in the correct location.
      Check the Flask server logs for errors.




Contact
For any questions or feedback, feel free to reach out:
SANJEET KUMAR
Email:sanjeetkumar121121@gmail.com
GitHub:https://github.com/sanj121
