from flask import Blueprint, render_template, request, jsonify
from connectors.mysql_connectors import engine

from models.user import User
from sqlalchemy import select, or_
from sqlalchemy.orm import sessionmaker
from flask_login import login_required, login_user, logout_user, current_user
from flask_jwt_extended import create_access_token, jwt_required

user_management_routes = Blueprint('user_management_routes',__name__)

# create user
@user_management_routes.route("/user", methods=['POST'])
def do_user_register():
        # Menerima data dari formulir HTML
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']

        # Membuat objek user baru
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
            return jsonify({"message": "password salah"}), 401
        
        # using token jwt
        # access_token = create_access_token(identify=user.id, additional_claims={"username": user.username})
        # return jsonify({'access_token': access_token})
        # u/ menyimpan data user yg berhasil login ke session 
        # lalu dibuatkan session id yg akan dikembalikan ke browser dan disimpan dalam cookie 
        login_user(user, remember = False)
        return jsonify({"message": "user berhasil login"}), 200

    except Exception as e:
        return jsonify({"message": "user gagal login"}), 500

# retrive the current auth user
@user_management_routes.route("/user", methods=['GET'])
@login_required
def user_home():
    response_data = dict()
    connection = engine.connect()
    Session = sessionmaker(connection)
    session = Session()

    try:
        user_query = session.query(User)

        if request.args.get('query') != None:
            search_query = request.args.get('query')
            user_query = user_query.filter(User.username.like(f'%{search_query}%'))
        users = session.execute(user_query)
        users = users.scalars()
        response_data['users'] = users
    except Exception as e:
        return jsonify({"message": e})

    response_data['username'] = current_user.username
    return jsonify(response_data)

# update the user
@user_management_routes.route("/user/<id>", methods=['PUT'])
@jwt_required()
def user_update(id):
    session = Session()
    session.begin()

    try:
        user = session.query(User).filter(User.id==id).first()
        
        user.username = request.form['username']
        user.email = request.form['email']
        session.commit()
    except Exception as e:
        sessio.rollback()
        return jsonify({"message": "fail to update data"})
    return {"message": "success update data user"}