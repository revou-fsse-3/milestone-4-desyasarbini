from flask import Blueprint, render_template, request, jsonify
from connectors.mysql_connectors import Session

from models.user import User
from sqlalchemy import select, or_
from sqlalchemy.orm import sessionmaker
from flask_login import login_user, logout_user
from flask_jwt_extended import create_access_token

user_routes = Blueprint('user_routes',__name__)