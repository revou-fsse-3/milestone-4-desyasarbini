from models.user import User
from connector.mysql_connector import engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import func
from flask import jsonify, request
from flask_login import login_required, login_user, logout_user
from utils.api_response import api_response

def create_user():
    username = request.form['username']
    email = request.form['email']
    password = request.form['password']

    # Membuat user baru
    new_user = User(username=username, email=email)
    new_user.set_password(password)

    connection = engine.connect()
    Session = sessionmaker(connection)
    session = Session()

    session.begin()
    try:
        session.add(new_user)
        session.commit()
    except Exception as e:
        print(f"Error during registration: {e}")
        session.rollback()
        return {"message": "Create user failed"}
    return api_response(
        status_code = 201, 
        message = "Create user success!", 
        data = {"id": new_user.id, "username": new_user.username, "email": new_user.email}
    )

def do_user_login():
    email = request.form['email']
    password = request.form['password']

    connection = engine.connect()
    Session = sessionmaker(connection)
    session = Session()

    session.begin()
    try:
        user = session.query(User).filter(User.email==email).first()

        if user == None:
            return api_response(
                status_code = 404,
                message = "e-mail not found",
                data = {}
            )
        
        # check password 
        if not user.check_password(password):
            return api_response(
                status_code = 404,
                message = "password incorrect, pllease check again",
                data = {}
            )
        
        login_user(user, remember = False)
        return api_response(
            status_code = 200,
            message = "Login Successfully",
            data = {"user": user.serialize(full=False)}
        )
        
    except Exception as e:
        print(f"Error during login: {e}")
        session.rollback()
        return {"message": "Login failed"}
    

def get_user(id):
    connection = engine.connect()
    Session = sessionmaker(connection)
    session = Session()

    session.begin()
    try:
        user = session.query(User).filter((User.id==id)).first()

        if user:
            return jsonify(user.serialize(full=True))
        else:
            return jsonify({
                'message': 'User is not registered yet'
            })

    except Exception as e:
        print(f"Error during registration: {e}")
        session.rollback()
        return {"message": "User not found"}


def update_user(id):
    connection = engine.connect()
    Session = sessionmaker(connection)
    session = Session()

    session.begin()
    try:
        user = session.query(User).filter((User.id==id)).first()
        if not user:
            return api_response(
                status_code = 404,
                message = "User not found",
                data = {}
            )
        
        user.username = request.form.get('username', user.username)
        user.email = request.form.get('email', user.email)
        new_password = request.form.get('password')
        if new_password:
            user.set_password(new_password)
            user.updated_at = func.now()

        session.commit()
        
        return api_response(
            status_code = 201,
            message = "User data has been updated successfully",
            data = {
                "username": user.username,
                "email": user.email,
                "password": new_password
            }
        )    
    except Exception as e:
        print(f"Error during registration: {e}")
        session.rollback()
        return {"message": "Update data user failed"}

def do_user_logout():
    logout_user()
    return api_response(
        status_code = 200,
        message = "Logout Successfully",
        data = {}
    )

