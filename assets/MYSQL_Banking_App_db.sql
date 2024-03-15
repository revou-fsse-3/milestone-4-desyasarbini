CREATE DATABASE banking_application;

DROP DATABASE banking_application;

USE banking_application;

CREATE TABLE user (
    id INT PRIMARY KEY AUTO_INCREMENT, username VARCHAR(255) UNIQUE NOT NULL, email VARCHAR(255) UNIQUE NOT NULL, password VARCHAR(255) NOT NULL, created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP, updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

CREATE TABLE accounts (
    id INT PRIMARY KEY AUTO_INCREMENT, user_id INT, account_type VARCHAR(255) NOT NULL, account_number VARCHAR(255) UNIQUE NOT NULL, balance DECIMAL(10, 2) DEFAULT 0.00, created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP, updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP, FOREIGN KEY (user_id) REFERENCES user (id)
);

CREATE TABLE transactions (
    id INT PRIMARY KEY AUTO_INCREMENT, from_account_id INT, to_account_id INT, amount DECIMAL(10, 2) DEFAULT 0.00, type VARCHAR(255) NOT NULL, description VARCHAR(255), created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP, FOREIGN KEY (from_account_id) REFERENCES accounts (id), FOREIGN KEY (to_account_id) REFERENCES accounts (id)
);

INSERT INTO
    user (username, email, password)
VALUES (
        'annie', 'annie@test.com', '12345'
    ),
    (
        'kuroko', 'kuroko@space.com', 'qwerty'
    );

SELECT * FROM user;

INSERT INTO
    accounts (
        user_id, account_type, account_number, balance
    )
VALUES (
        1, 'saving', '10190990', 5000000.00
    );

-- Insert a saving account
INSERT INTO
    accounts (
        user_id, account_type, account_number, balance
    )
VALUES (
        1, 'saving', '10190990', 50.00
    );

-- Insert a checking account for the same account number
INSERT INTO
    accounts (
        user_id, account_type, account_number, balance
    )
VALUES (
        1, 'checking', '10190990', 50.00
    );

SELECT * FROM accounts;