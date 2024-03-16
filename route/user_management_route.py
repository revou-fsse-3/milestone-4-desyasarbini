from flask import Blueprint
from controllers.user_controller import (
    create_user, 
    do_user_login,
    do_user_logout,
    get_user,
    update_user
    )

user_management_routes = Blueprint('user_management_endpoint', __name__)

user_management_routes.route("/user", methods=['POST'])(create_user)

user_management_routes.route("/login", methods=['POST'])(do_user_login)

user_management_routes.route("/logout", methods=['GET'])(do_user_logout)

user_management_routes.route("/user/<id>", methods=['GET'])(get_user)

user_management_routes.route("/user/<id>", methods=['PUT'])(update_user)

