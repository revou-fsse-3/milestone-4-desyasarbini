from models.transaction import Transaction
from connector.mysql_connector import engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import func, select, or_
from flask import jsonify, request
from flask_login import login_required, current_user
from utils.api_response import api_response

def get_all_transaction():
    response_data = dict()
    connection = engine.connect()
    Session = sessionmaker(connection)
    session = Session()
    try:
        transaction_query = session.query(Transaction)

        if request.args.get('query') != None:
            search_query = request.args.get('query')
            transaction_query = transaction_query.filter(Transaction.from_account_id.like(f"%{search_query}%"))

        transactions = transaction_query.all()
        response_data['transactions'] = [account.serialize(full=False) for account in transactions]
        return jsonify(response_data)

    except Exception as e:
        return api_response(
            status_code = 500,
            message = str(e),
            data = {}
        )

def create_transaction_deposit():
    from_account_id = request.form['from_account_id']
    to_account_id = request.form['to_account_id']
    amount = request.form['amount']
    type = request.form['type']
    description = request.form['description']

    if not to_account_id or not amount:
        raise ValueError("Please fill in 'to_account_id' and 'amount'")
        
    deposit_transaction = Transaction(
        from_account_id = from_account_id,  
        to_account_id = to_account_id,
        amount = amount,
        type = type,
        description = description
    )
    
    connection = engine.connect()
    Session = sessionmaker(connection)
    session = Session()

    session.begin()
    try:
        session.add(deposit_transaction)
        session.commit()
    except Exception as e:
        print(f"Error during registration: {e}")
        session.rollback()
        return {"message": "Deposit transaction failed"}
    return api_response(
        status_code = 201, 
        message = "Deposit success!", 
        data = {
            "id": deposit_transaction.id, 
            "from_account_id": deposit_transaction.from_account_id, 
            "to_account_id": deposit_transaction.to_account_id,
            "amount": deposit_transaction.amount,
            "type": deposit_transaction.type,
            "description": deposit_transaction.description
        }
    )

def create_transaction_transfer():
    from_account_id = request.form['from_account_id']
    to_account_id = request.form['to_account_id']
    amount = request.form['amount']
    type = request.form['type']
    description = request.form['description']

    if not to_account_id or not amount:
        raise ValueError("Please fill in 'to_account_id' and 'amount'")
        
    transfer_transaction = Transaction(
        from_account_id = from_account_id,  
        to_account_id = to_account_id,
        amount = amount,
        type = type,
        description = description
    )
    
    connection = engine.connect()
    Session = sessionmaker(connection)
    session = Session()

    session.begin()
    try:
        session.add(transfer_transaction)
        session.commit()
    except Exception as e:
        print(f"Error during registration: {e}")
        session.rollback()
        return {"message": "Transfer transaction failed"}
    return api_response(
        status_code = 201, 
        message = "Transfer success!", 
        data = {
            "id": transfer_transaction.id, 
            "from_account_id": transfer_transaction.from_account_id, 
            "to_account_id": transfer_transaction.to_account_id,
            "amount": transfer_transaction.amount,
            "type": transfer_transaction.type,
            "description": transfer_transaction.description
        }
    )

def create_transaction_withdrawal():
    from_account_id = request.form['from_account_id']
    to_account_id = request.form['to_account_id']
    amount = request.form['amount']
    type = request.form['type']
    description = request.form['description']

    if not to_account_id or not amount:
        raise ValueError("Please fill in 'to_account_id' and 'amount'")
        
    withdrawal_transaction = Transaction(
        from_account_id = from_account_id,  
        to_account_id = to_account_id,
        amount = amount,
        type = type,
        description = description
    )
    
    connection = engine.connect()
    Session = sessionmaker(connection)
    session = Session()

    session.begin()
    try:
        session.add(withdrawal_transaction)
        session.commit()
    except Exception as e:
        print(f"Error during registration: {e}")
        session.rollback()
        return {"message": "Withdrawal transaction failed"}
    return api_response(
        status_code = 201, 
        message = "Withdrawal success!", 
        data = {
            "id": withdrawal_transaction.id, 
            "from_account_id": withdrawal_transaction.from_account_id, 
            "to_account_id": withdrawal_transaction.to_account_id,
            "amount": withdrawal_transaction.amount,
            "type": withdrawal_transaction.type,
            "description": withdrawal_transaction.description
        }
    )

def detail_transaction(id):
    connection = engine.connect()
    Session = sessionmaker(connection)
    session = Session()

    session.begin()
    try:
        transaction = session.query(Transaction).filter((Transaction.id==id)).first()

        if transaction:
            return jsonify(transaction.serialize(full=True))
        else:
            return jsonify({
                'message': 'Transaction is not created yet'
            })

    except Exception as e:
        print(f"Error during registration: {e}")
        session.rollback()
        return {"message": "Transaction not found"}