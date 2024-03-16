from flask import Flask
from dotenv import load_dotenv
from sqlalchemy import select
from sqlalchemy.orm import sessionmaker
import os

from connector.mysql_connector import engine
from models.user import User

# Authentication token
from flask_login import LoginManager
from flask_jwt_extended import JWTManager

# Route files
from route.user_management_route import user_management_routes
from route.account_management_route import account_management_routes
from route.transaction_management_route import transaction_management_routes

load_dotenv()

app = Flask(__name__)

# Login Manager
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
login_manager = LoginManager()
login_manager.init_app(app)

# JWT Manager
app.config['JWT_SECRET_KEY'] = os.getenv('SECRET_KEY')
jwt = JWTManager(app)

# u/ cek data cookie
# u/ mengetahui siapa yg login
@login_manager.user_loader
def load_user(user_id):
    connection = engine.connect()
    Session = sessionmaker(connection)
    session = Session()

    return session.query(User).get(int(user_id))

app.register_blueprint(user_management_routes)
app.register_blueprint(account_management_routes)
app.register_blueprint(transaction_management_routes)

@app.route("/")
def hello_world():
    return "Berhasil terhubung ke database"