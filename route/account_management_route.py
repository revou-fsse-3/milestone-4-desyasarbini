from flask import Blueprint
from controllers.account_controller import (
    create_account,
    get_all_account,
    detail_account,
    update_account,
    delete_account
)

account_management_routes = Blueprint('account_management_endpoint', __name__)

account_management_routes.route("/account", methods=['POST'])(create_account)

account_management_routes.route("/accounts", methods=['GET'])(get_all_account)

account_management_routes.route("/accounts/<id>", methods=['GET'])(detail_account)

account_management_routes.route("/accounts/<id>", methods=['PUT'])(update_account)

account_management_routes.route("/accounts/<id>", methods=['DELETE'])(delete_account)