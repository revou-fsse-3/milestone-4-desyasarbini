from flask import Blueprint, render_template, request, redirect, jsonify, url_for
from connectors.mysql_connectors import engine
from models.transactions import Transactions
from sqlalchemy import select
from sqlalchemy import func

from flask_login import current_user, login_required
from sqlalchemy.orm import sessionmaker
from flask_login import login_user, logout_user
from flask_jwt_extended import jwt_required

# Definisikan Blueprint untuk rute-rute terkait produk
transaction_management_routes = Blueprint('transaction_management_routes', __name__)

@transaction_management_routes.route("/transactions", methods=['POST'])
@jwt_required
def create_new_transaction():
    new_transaction = Transactions(
        
    )