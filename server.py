from flask_app import app
from flask_app.controllers import members_controller, vehicles_controller

if __name__ == "__main__":
    app.run(debug=True)