from app import app
from app.controllers import users, recipes

if __name__ == "__main__":
    app.run(debug=True)