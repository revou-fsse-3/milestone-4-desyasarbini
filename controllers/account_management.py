from flask import Blueprint, request, jsonify
from connectors.mysql_connectors import engine, Session
from models.accounts import Accounts
from models.transactions import Transactions
from sqlalchemy import select, or_

from flask_login import current_user, login_required
from sqlalchemy.orm import sessionmaker
from flask_jwt_extended import jwt_required

# Definisikan Blueprint untuk rute-rute terkait produk
account_management_routes = Blueprint('account_management_routes', __name__)

@account_management_routes.route("/accounts", methods=['POST'])
@login_required
def create_account():
    new_account = Accounts(
        account_type = request.form['account_type'],
        account_number = request.form['account_number'],
        balance = request.form['balance']
    )

    session = Session()
    session.begin()
    try:
        session.add(new_account)
        session.commit()
    except Exception as e:
        session.rollback()
        return{"message": "fail to create account"}
    return {"message": "create account success"}
    

@account_management_routes.route("/accounts", methods=['GET'])
@login_required
def account_home():
    response_data = dict()
    connection = engine.connect()
    Session = sessionmaker(connection)
    session = Session()

    try:
        account_query = select(Accounts)
        if request.arg.get('query') != None:
            search_query = request.args.get('query')
            account_query = account_query.where(or_(Accounts.account_type.like(f'%{search_query}%')))
        
        accounts = session.execute(account_query)
        accounts = accounts.scalars()
        response_data['accounts'] = accounts

    except Exception as e:
        return jsonify({"message": e})

    response_data['name'] = current_user.name
    return jsonify(response_data)

@account_management_routes.route("/accounts/<id>", methods=['GET'])
@jwt_required()
def account_detail(id):
    response_data = dict()
    session = Session()

    try:
        account = session.query(Accounts).filter((Accounts.id==id)).first()
        if (account == None):
            return "Account not found"
        response_data['account'] = account
    except Exception as e:
        print(e)
        return "error processing data"
    return jsonify({"message": "berhasil melihat data account"})

@account_management_routes.route("/accounts/<id>", methods=['PUT'])
@jwt_required()
def account_update(id):

    connection = engine.connect()
    Session = sessionmaker(connection)
    session = Session()
    session.begin()

    try:
        account = session.query(Accounts).filter(Accounts.id==id).first()

        account.account_type = request.form['account_type']
        account.account_number = request.form['account_number']
        account.balance = request.form['balance']

        session.commit()
    except Exception as e:
        session.rollback()
        return { "message": "Fail to Update data account"}
    
    return { "message": "Success updating data account"}