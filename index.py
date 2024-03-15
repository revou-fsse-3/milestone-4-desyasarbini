from flask import Flask
from dotenv import load_dotenv
from connectors.mysql_connector import engine
from sqlalchemy import text, select
from sqlalchemy.orm import sessionmaker

# Authentication token
from flask_login import LoginManager
from flask_jwt_extended import JWTManager

import os

app = Flask(__name__)