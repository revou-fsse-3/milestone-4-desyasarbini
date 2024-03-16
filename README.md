[![Review Assignment Due Date](https://classroom.github.com/assets/deadline-readme-button-24ddc0f5d75046c5622901739e7c5dd533143b0c8e959d652212380cedb1ea36.svg)](https://classroom.github.com/a/TId9PLV9)

# Documentation for api

| Tool                            | Documentation                                                                     |
| ------------------------------- | --------------------------------------------------------------------------------- |
| [PostMAN](https://postman.com/) | [Banking Application](https://documenter.getpostman.com/view/32144902/2sA2xnwUv7) |

### User Management

- POST /users: Create a new user account.
- GET /users/me: Retrieve the profile of the currently authenticated user.
- PUT /users/me: Update the profile information of the currently authenticated user.

### Account Management

- GET /accounts: Retrieve a list of all accounts belonging to the currently authenticated user.
- GET /accounts/:id: Retrieve details of a specific account by its ID. (Authorization required for account owner)
- POST /accounts: Create a new account for the currently authenticated user.
- PUT /accounts/:id: Update details of an existing account. (Authorization required for account owner)
- DELETE /accounts/:id: Delete an account. (Authorization required for account owner)

### Transaction Management

- GET /transactions: Retrieve a list of all transactions for the currently authenticated user's accounts. (Optional: filter by account ID, date range)
- GET /transactions/:id: Retrieve details of a specific transaction by its ID. (Authorization required for related account owner)
- POST /transactions: Initiate a new transaction (deposit, withdrawal, or transfer). (Authorization required for related account owner)
