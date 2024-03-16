from flask import Blueprint, request, jsonify, sessions
from connectors.mysql_connectors import Session, engine

from models.user import User
from sqlalchemy.orm import sessionmaker
from flask_login import login_required, login_user, logout_user, current_user
from flask_jwt_extended import create_access_token, jwt_required

user_management_routes = Blueprint('user_management_routes',__name__)

# create user
@user_management_routes.route("/user", methods=['POST'])
def do_user_register():
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
            # gagal
            session.rollback()
            return {"message": "Gagal register"}
        return {"message": "Sukses register"}

# login user
@user_management_routes.route("/login", methods=['POST'])
def do_user_login():
    connection = engine.connect()
    Session = sessionmaker(connection)
    session = Session()

    try:
        user = session.query(User).filter(User.email==request.form['email']).first()

        if user == None:
            return jsonify({"message": "email belum terdaftar"}), 404
        
        # check password 
        if not user.check_password(request.form['password']):
            return {"message": "password salah"}, 401
        
        # u/ menyimpan data user yg berhasil login ke session 
        # lalu dibuatkan session id yg akan dikembalikan ke browser dan disimpan dalam cookie 
        login_user(user, remember = False)
        return {"message": "user berhasil login"}, 200

    except Exception as e:
        return {"message": "user gagal login"}, 500

# retrive the current auth user
@user_management_routes.route("/user/<id>", methods=['GET'])
@login_required()
def user_detail(id):
    response_data = dict()
    session = Session()

    try:
        user = session.query(User).filter((User.id==id)).first()
        if (user == None):
            return "User not found"
        response_data['user'] = user
    except Exception as e:
        print(e)
        return jsonify({"message": "error getting data user"})
    return jsonify(response_data)

# update the user
@user_management_routes.route("/user/<id>", methods=['PUT'])
@login_required()
def user_update(id):
    session = Session()
    session.begin()

    try:
        user = session.query(User).filter(User.id==id).first()
        
        user.username = request.form['username']
        user.email = request.form['email']
        session.commit()
    except Exception as e:
        session.rollback()
        return {"message": "fail to update data"}
    return {"message": "success update data user"}

@user_management_routes.route("/logout", methods=['GET'])
def do_user_logout():
    logout_user()
    return {"message": "berhasil logout"}