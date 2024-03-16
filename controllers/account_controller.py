from models.account import Account
from connector.mysql_connector import engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import func, select, or_
from flask import jsonify, request
from flask_login import login_required, current_user
from utils.api_response import api_response


def get_all_account():
    response_data = dict()
    connection = engine.connect()
    Session = sessionmaker(connection)
    session = Session()
    try:
        account_query = session.query(Account)

        if request.args.get('query') != None:
            search_query = request.args.get('query')
            account_query = account_query.filter(Account.account_type.like(f"%{search_query}%"))

        accounts = account_query.all()
        response_data['accounts'] = [account.serialize(full=False) for account in accounts]
        return jsonify(response_data)

    except Exception as e:
        return api_response(
            status_code=500,
            message=str(e),
            data={}
        )


def create_account():
    account_type = request.form['account_type']
    account_number = request.form['account_number']
    balance = request.form['balance']

    if not account_type or not account_number or not balance:
        raise ValueError("Data tidak lengkap")
    
    new_account = Account(
        user_id = current_user.id, 
        account_type = account_type,
        account_number = account_number,
        balance = balance
    )

    connection = engine.connect()
    Session = sessionmaker(connection)
    session = Session()

    session.begin()
    try:
        session.add(new_account)
        session.commit()
    except Exception as e:
        print(f"Error during registration: {e}")
        session.rollback()
        return {"message": "Create account failed"}
    return api_response(
        status_code = 201, 
        message = "Create account success!", 
        data = {
            "id": new_account.id, 
            "user_id": new_account.user_id, 
            "account_type": new_account.account_type,
            "account_number": new_account.account_number,
            "balance": new_account.balance
        }
    )


def detail_account(id):
    connection = engine.connect()
    Session = sessionmaker(connection)
    session = Session()

    session.begin()
    try:
        account = session.query(Account).filter((Account.id==id)).first()

        if account:
            return jsonify(account.serialize(full=True))
        else:
            return jsonify({
                'message': 'Account is not created yet'
            })

    except Exception as e:
        print(f"Error during registration: {e}")
        session.rollback()
        return {"message": "Account not found"}


def update_account(id):
    connection = engine.connect()
    Session = sessionmaker(connection)
    session = Session()

    session.begin()
    try:
        account = session.query(Account).filter(Account.id==id).first()

        account.account_type = request.form.get('account_type', account.account_type)
        account.account_number = request.form.get('account_number', account.account_number)
        account.balance = request.form.get('balance', account.balance)
        account.updated_at = func.now()

        session.commit()
            
        return api_response(
            status_code = 201,
            message = "Account data updated successfully",
            data = {
                    "account_type": account.account_type,
                    "account_number": account.account_number,
                    "balance": account.balance,
                    "updated_at": account.updated_at
                }
            )
    
    except Exception as e:
        session.rollback()
        return api_response(
            status_code=500,
            message=str(e),
            data={}
        )


def delete_account(id):
    connection = engine.connect()
    Session = sessionmaker(connection)
    session = Session()

    session.begin()
    try:
        account = session.query(Account).filter(Account.id==id).first()
        session.delete(account)
        session.commit()

    except Exception as e:
        session.rollback()
        return api_response(
            status_code=500,
            message=str(e),
            data={}
        )
    return api_response(
        status_code = 201, 
        message = "Delete data account success!", 
        data = {}
    )