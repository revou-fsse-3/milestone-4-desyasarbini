from flask import Blueprint
from controllers.transaction_controller import (
    get_all_transaction,
    create_transaction_deposit,
    create_transaction_transfer,
    create_transaction_withdrawal,
    detail_transaction
)

transaction_management_routes = Blueprint('transaction_management_endpoint', __name__)

transaction_management_routes.route("/transactions", methods=['GET'])(get_all_transaction)

transaction_management_routes.route("/transactions/deposit", methods=['POST'])(create_transaction_deposit)

transaction_management_routes.route("/transactions/transfer", methods=['POST'])(create_transaction_transfer)

transaction_management_routes.route("/transactions/withdrawal", methods=['POST'])(create_transaction_withdrawal)

transaction_management_routes.route("/transactions/<id>", methods=['GET'])(detail_transaction)